"""Resumable title-only embeddings. No key/log dump. Existing pilot vectors reused."""
from pathlib import Path
import csv,json,hashlib,datetime,urllib.request,urllib.error,time,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
MODEL='qwen/qwen3-embedding-8b';DIM=4096;BATCH=64
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(p)
def main():
    checkpoint=OUT/'checkpoints';checkpoint.mkdir(exist_ok=True)
    source=ROOT/'03_processed_data/patent_metadata_full.csv'
    with source.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==3621 and len({r['application_number'] for r in rows})==3621
    assert all(r['title'].strip() for r in rows)
    inputsha=sha(source)
    old=OUT/'run_manifest.json'
    if old.exists():assert json.loads(old.read_text(encoding='utf-8'))['source_sha256']==inputsha
    pilot=json.loads((ROOT/'04_analysis/embedding_pilot/five_patents_embeddings.json').read_text(encoding='utf-8'))
    assert pilot['request_parameters']['model']==MODEL
    reuse={r['application_number']:r for r in pilot['records']}
    vectors={k:np.array(v['embedding'],dtype=np.float32) for k,v in reuse.items()}
    for k,v in reuse.items():assert next(r for r in rows if r['application_number']==k)['title'].strip()==v['input_text']
    pilot_tokens=pilot['summary']['usage']['total_tokens'];pilot_cost=pilot['summary']['usage']['cost']
    tokens=0;cost=0.;calls=0
    for p in sorted(checkpoint.glob('batch_*.npz')):
        with np.load(p,allow_pickle=False) as z:
            assert str(z['model'])==MODEL and str(z['source_sha256'])==inputsha
            vectors.update(zip(z['ids'].tolist(),z['vectors']))
            tokens+=int(z['tokens']);cost+=float(z['cost']);calls+=1
    key=(ROOT/'openrouterkey.txt').read_text(encoding='utf-8-sig').strip()
    assert key and not any(c.isspace() for c in key)
    def redact(v):return json.loads(json.dumps(v,ensure_ascii=False).replace(key,'[REDACTED]'))
    def manifest(status,failures=0,error=None):
        m={'model':MODEL,'dimension':DIM,'input_columns':['title'],'abstract_available':False,'source_sha256':inputsha,'status':status,'successful_records':len(vectors),'failed_records':failures,'pending_records':3621-len(vectors),'new_requests':calls,'new_prompt_tokens':tokens,'new_api_cost_usd':cost,'reused_pilot_records':5,'pilot_prompt_tokens':pilot_tokens,'pilot_cost_usd':pilot_cost,'total_prompt_tokens_including_pilot':tokens+pilot_tokens,'total_api_cost_usd_including_pilot':cost+pilot_cost,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        if error:m['error']=error
        save(old,m);return m
    remaining=[r for r in rows if r['application_number'] not in vectors]
    for offset in range(0,len(remaining),BATCH):
        batch=remaining[offset:offset+BATCH]
        payload={'model':MODEL,'input':[r['title'].strip() for r in batch],'encoding_format':'float','provider':{'sort':'price','allow_fallbacks':False}}
        req=urllib.request.Request('https://openrouter.ai/api/v1/embeddings',data=json.dumps(payload,ensure_ascii=False).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=90) as response:result=redact(json.load(response));status=response.status
        except urllib.error.HTTPError as e:
            try:detail=redact(json.loads(e.read().decode()))
            except Exception:detail={'message':'Non-JSON error omitted'}
            print(json.dumps(manifest('stopped_api_error',len(batch),{'http_status':e.code,'detail':detail}),ensure_ascii=True));return 1
        except urllib.error.URLError as e:
            print(json.dumps(manifest('stopped_network_error',len(batch),{'type':type(e.reason).__name__}),ensure_ascii=True));return 2
        except Exception as e:
            print(json.dumps(manifest('stopped_response_error',len(batch),{'type':type(e).__name__}),ensure_ascii=True));return 1
        data=sorted(result.get('data',[]),key=lambda x:x['index'])
        arr=np.array([x['embedding'] for x in data],dtype=np.float32)
        if status!=200 or arr.shape!=(len(batch),DIM) or [x['index'] for x in data]!=list(range(len(batch))) or not np.isfinite(arr).all() or (np.linalg.norm(arr,axis=1)==0).any():
            print(json.dumps(manifest('stopped_invalid_vectors',len(batch),{'http_status':status}),ensure_ascii=True));return 1
        usage=result.get('usage',{})
        if 'cost' not in usage or 'prompt_tokens' not in usage:
            print(json.dumps(manifest('stopped_missing_usage',len(batch)),ensure_ascii=True));return 1
        bt=int(usage['prompt_tokens']);bc=float(usage['cost'])
        dest=checkpoint/f'batch_{calls+1:04d}.npz'
        np.savez_compressed(dest,ids=np.array([r['application_number'] for r in batch]),vectors=arr,tokens=bt,cost=bc,model=MODEL,source_sha256=inputsha)
        vectors.update(zip([r['application_number'] for r in batch],arr));tokens+=bt;cost+=bc;calls+=1
        manifest('running')
        print(json.dumps({'completed':len(vectors),'of':3621,'api_cost_usd_new':cost}),flush=True)
    arr=np.array([vectors[r['application_number']] for r in rows],dtype=np.float32)
    np.save(OUT/'embeddings.npy',arr)
    with (ROOT/'03_processed_data/patent_selection_links.csv').open(encoding='utf-8-sig',newline='') as f:links=list(csv.DictReader(f))
    with (ROOT/'04_analysis/eda/company_metrics.csv').open(encoding='utf-8-sig',newline='') as f:companies={r['selection_id']:r for r in csv.DictReader(f)}
    selections={}
    for link in links:selections.setdefault(link['application_number'],{})[link['selection_id']]=link
    records=[]
    for i,r in enumerate(rows):
        memberships=[]
        for sid in sorted(selections[r['application_number']]):
            c=companies[sid];memberships.append({'selection_id':sid,'company':c['company_name_official'],'cohort':int(c['cohort']),'selection_year':int(c['selection_year']),'field':c['field_official']})
        records.append({'index':i,'application_number':r['application_number'],'title':r['title'],'application_year':int(r['application_date'][:4]),'right_type':r['right_type'],'ipc':json.loads(r['ipc_json']),'memberships':memberships,'embedding_row':i})
    save(OUT/'patent_embedding_records.json',records)
    print(json.dumps(manifest('complete'),ensure_ascii=True),flush=True);return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print(json.dumps({'stopped':True,'error_type':type(e).__name__}));sys.exit(1)
