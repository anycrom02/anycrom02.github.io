"""Reproducible title-semantic analysis, independent map and cluster projections."""
from pathlib import Path
import os,sys,json,csv,re,collections,hashlib,importlib.metadata
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(OUT/'vendor'))
os.environ['NUMBA_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.metrics import adjusted_rand_score
from threadpoolctl import threadpool_limits
import umap,hdbscan

def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def writecsv(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def subcodes(record):return sorted(set(m.group() for c in record['ipc'] if (m:=re.match(r'[A-H]\d{2}[A-Z]',c))))
def main():
    manifest=json.loads((OUT/'run_manifest.json').read_text(encoding='utf-8'));assert manifest['status']=='complete'
    x=np.load(OUT/'embeddings.npy');records=json.loads((OUT/'patent_embedding_records.json').read_text(encoding='utf-8'))
    assert x.shape==(3621,4096) and np.isfinite(x).all() and len(records)==3621
    unit=normalize(x)
    pca=PCA(n_components=50,svd_solver='randomized',random_state=42,whiten=False)
    with threadpool_limits(limits=1):p=pca.fit_transform(unit)
    np.save(OUT/'pca50.npy',p)
    print(json.dumps({'stage':'PCA complete','explained_variance':float(pca.explained_variance_ratio_.sum())}),flush=True)
    def projection(d,seed,mindist):return umap.UMAP(n_components=d,n_neighbors=30,min_dist=mindist,metric='cosine',random_state=seed,n_jobs=1).fit_transform(p)
    latent=projection(10,42,0.0);np.save(OUT/'umap10.npy',latent)
    clustering=hdbscan.HDBSCAN(min_cluster_size=25,min_samples=10,metric='euclidean',cluster_selection_method='eom',core_dist_n_jobs=1)
    labels=clustering.fit_predict(latent)
    raw=sorted(set(labels)-{-1},key=lambda c:(-int((labels==c).sum()),int(c)))
    mapping={old:i for i,old in enumerate(raw)}
    labels=np.array([mapping.get(v,-1) for v in labels]);np.save(OUT/'cluster_labels.npy',labels)
    coords=projection(2,42,.15);np.save(OUT/'umap2.npy',coords)
    print(json.dumps({'stage':'clustering and map complete','clusters':len(raw),'noise':int((labels==-1).sum())}),flush=True)
    sensitivity=[]
    for minimum in [20,40]:
        alt=hdbscan.HDBSCAN(min_cluster_size=minimum,min_samples=10,metric='euclidean',cluster_selection_method='eom',core_dist_n_jobs=1).fit_predict(latent)
        overlap=(alt>=0)&(labels>=0)
        sensitivity.append({'variant':f'min_cluster_size={minimum}','clusters':len(set(alt)-{-1}),'noise':int((alt==-1).sum()),'ari_all_including_noise':float(adjusted_rand_score(labels,alt)),'common_assigned_n':int(overlap.sum()),'ari_common_assigned':float(adjusted_rand_score(labels[overlap],alt[overlap]))})
    altlatent=projection(10,7,0.0)
    alt=hdbscan.HDBSCAN(min_cluster_size=25,min_samples=10,metric='euclidean',cluster_selection_method='eom',core_dist_n_jobs=1).fit_predict(altlatent)
    overlap=(alt>=0)&(labels>=0)
    sensitivity.append({'variant':'UMAP seed=7','clusters':len(set(alt)-{-1}),'noise':int((alt==-1).sum()),'ari_all_including_noise':float(adjusted_rand_score(labels,alt)),'common_assigned_n':int(overlap.sum()),'ari_common_assigned':float(adjusted_rand_score(labels[overlap],alt[overlap]))})
    field=collections.defaultdict(collections.Counter);ipc=collections.defaultdict(collections.Counter)
    for i,r in enumerate(records):
        r.update(cluster=int(labels[i]),cluster_probability=float(clustering.probabilities_[i]),x=round(float(coords[i,0]),5),y=round(float(coords[i,1]),5),ipc_subclasses=subcodes(r))
        for m in r['memberships']:field[m['field']][int(labels[i])]+=1/len(r['memberships'])
        for c in r['ipc_subclasses']:ipc[c][int(labels[i])]+=1/len(r['ipc_subclasses'])
    assert abs(sum(sum(d.values()) for d in field.values())-3621)<1e-7
    assert abs(sum(sum(d.values()) for d in ipc.values())-3621)<1e-7
    profiles=[]
    for c in list(range(len(raw)))+[-1]:
        ids=np.where(labels==c)[0];center=normalize(unit[ids].mean(axis=0).reshape(1,-1))[0];sims=unit[ids]@center
        near=ids[np.argsort(-sims)[:8]];edge=ids[np.argsort(sims)[:3]]
        fc=collections.Counter();ic=collections.Counter();co=collections.Counter();years=collections.Counter()
        for i in ids:
            r=records[i];years[r['application_year']]+=1
            for m in r['memberships']:fc[m['field']]+=1/len(r['memberships']);co[m['company']]+=1
            for code in r['ipc_subclasses']:ic[code]+=1/len(r['ipc_subclasses'])
        profiles.append({'cluster':c,'n':len(ids),'share_pct':len(ids)/3621*100,'label':'혼합 기술군' if c>=0 else '미배정','representatives':[{'application_number':records[i]['application_number'],'title':records[i]['title'],'ipc':records[i]['ipc_subclasses'],'fields':sorted(set(m['field'] for m in records[i]['memberships'])),'cosine_to_centroid':float(unit[i]@center)} for i in near],'boundary_titles':[records[i]['title'] for i in edge],'top_ipc':dict(ic.most_common(5)),'top_fields':dict(fc.most_common(5)),'top_companies':dict(co.most_common(5)),'year_counts':dict(sorted(years.items())),'mean_cosine_to_centroid':float(sims.mean()),'cluster_persistence':float(clustering.cluster_persistence_[raw[c]]) if c>=0 else None})
    idsbycluster={c:np.where(labels==c)[0] for c in range(len(raw))}
    sameipc=[]
    for code,total in sorted(ipc.items(),key=lambda kv:-sum(kv[1].values())):
        top=[(c,v) for c,v in total.most_common() if c>=0 and v>=10]
        if len(top)<2:continue
        cases=[]
        for c,v in top[:3]:
            idx=[i for i in idsbycluster[c] if code in records[i]['ipc_subclasses']]
            center=normalize(unit[idsbycluster[c]].mean(axis=0).reshape(1,-1))[0]
            best=sorted(idx,key=lambda i:-float(unit[i]@center))[:3]
            cases.append({'cluster':c,'fractional_weight':v,'ipc_share_pct':v/sum(total.values())*100,'examples':[{'application_number':records[i]['application_number'],'title':records[i]['title'],'ipc':records[i]['ipc_subclasses']} for i in best]})
        sameipc.append({'ipc':code,'total_fractional_weight':sum(total.values()),'nonnoise_clusters':sum(v>0 and c>=0 for c,v in total.items()),'groups':cases})
    pairs=[]
    for c,idx in idsbycluster.items():
        sim=unit[idx]@unit[idx].T;np.fill_diagonal(sim,-2)
        order=np.argsort(sim.ravel())[::-1]
        for flat in order:
            a,b=divmod(int(flat),len(idx));i,j=int(idx[a]),int(idx[b])
            if i>=j:continue
            if set(records[i]['ipc_subclasses'])&set(records[j]['ipc_subclasses']):continue
            if records[i]['title']==records[j]['title']:continue
            pairs.append({'cluster':c,'cosine_similarity':float(sim[a,b]),'a':{k:records[i][k] for k in ['application_number','title','ipc_subclasses']},'b':{k:records[j][k] for k in ['application_number','title','ipc_subclasses']}});break
    pairs.sort(key=lambda r:-r['cosine_similarity'])
    field_rows=[{'field':f,'cluster':c,'fractional_patents':v,'field_share_pct':v/sum(counter.values())*100} for f,counter in field.items() for c,v in sorted(counter.items())]
    ipc_rows=[{'ipc':f,'cluster':c,'fractional_patents':v,'ipc_share_pct':v/sum(counter.values())*100} for f,counter in ipc.items() for c,v in sorted(counter.items())]
    writecsv('field_cluster_matrix.csv',field_rows);writecsv('ipc_cluster_matrix.csv',ipc_rows)
    save('cluster_profiles.json',profiles);save('semantic_patents.json',records);save('comparison_examples.json',{'same_ipc':sameipc,'different_ipc_near_pairs':pairs})
    versions={lib:importlib.metadata.version(lib) for lib in ['numpy','scipy','scikit-learn','umap-learn','hdbscan','matplotlib']}
    method={'model':'qwen/qwen3-embedding-8b','input':'title only; abstracts not available','n':3621,'dimension':4096,'normalization':'L2 unit vectors','pca':{'components':50,'svd_solver':'randomized','random_state':42,'whiten':False,'explained_variance_ratio':float(pca.explained_variance_ratio_.sum())},'cluster_projection':{'method':'UMAP','components':10,'n_neighbors':30,'min_dist':0.0,'metric':'cosine','random_state':42,'n_jobs':1},'clustering':{'method':'HDBSCAN','min_cluster_size':25,'min_samples':10,'metric':'euclidean','cluster_selection_method':'eom'},'map_projection':{'method':'UMAP','components':2,'n_neighbors':30,'min_dist':.15,'metric':'cosine','random_state':42,'n_jobs':1},'cluster_count':len(raw),'clustered_n':int((labels>=0).sum()),'noise_n':int((labels==-1).sum()),'noise_pct':float((labels==-1).mean()*100),'sensitivity':sensitivity,'versions':versions,'reason':'PCA speeds neighbor search; 10D manifold projection precedes density clustering without specifying cluster count; independent 2D projection is display only. min_cluster_size25 excludes tiny groups and min_samples10 reduces weak assignments. UMAP distorts density and global distance; all outputs exploratory and parameter-dependent.','matrix_counting':'Each unique application receives total1 across selection memberships and total1 across unique IPC subclasses; separate matrices both sum3621. Noise retained in denominators.'}
    save('analysis_methods.json',method)
    save('embedding_validation.json',{'shape':list(x.shape),'all_finite':bool(np.isfinite(x).all()),'all_nonzero':bool((np.linalg.norm(x,axis=1)>0).all()),'source_sha256_matches':hashlib.sha256((ROOT/'03_processed_data/patent_metadata_full.csv').read_bytes()).hexdigest()==manifest['source_sha256']})
    print(json.dumps(method,ensure_ascii=True),flush=True)
if __name__=='__main__':main()
