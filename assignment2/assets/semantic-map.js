'use strict';
(() => {
  const dataset=window.SEMANTIC_DATA;
  const canvas=document.querySelector('#semantic-canvas');
  if(!dataset || !canvas) return;
  const ctx=canvas.getContext('2d');
  const el=id=>document.getElementById(id);
  const controls=['sem-field','sem-company','sem-cohort','sem-year','sem-cluster','sem-color'].map(el);
  const colors=['#27356f','#b06b24','#317e82','#9467a3','#cc6460','#5c843d','#6b79b8','#a04978','#4e6e95','#80764b','#2c8eae','#a66f85'];
  const clusterColor=c=>c<0?'#b9bcc4':colors[c%colors.length];
  const name=c=>c<0?'미배정':`C${String(c+1).padStart(2,'0')} · ${dataset.clusters.find(s=>s.cluster===c).label}`;
  function options(id,values) { values.forEach(v=>{const o=document.createElement('option');o.value=String(v);o.textContent=String(v);el(id).append(o);}); }
  options('sem-field',[...new Set(dataset.patents.flatMap(r=>r.memberships.map(m=>m.field)))].sort());
  options('sem-company',[...new Set(dataset.patents.flatMap(r=>r.memberships.map(m=>m.company)))].sort((a,b)=>a.localeCompare(b,'ko')));
  options('sem-cohort',[1,2,3,4]);options('sem-year',[...new Set(dataset.patents.map(r=>r.application_year))].sort());
  dataset.clusters.forEach(c=>{const o=document.createElement('option');o.value=c.cluster;o.textContent=`${name(c.cluster)} (${c.n}건)`;el('sem-cluster').append(o);});
  let selected=[],drawn=[],width=0,height=0,zoom=1,limit=20;
  const bounds={xmin:Math.min(...dataset.patents.map(r=>r.x)),xmax:Math.max(...dataset.patents.map(r=>r.x)),ymin:Math.min(...dataset.patents.map(r=>r.y)),ymax:Math.max(...dataset.patents.map(r=>r.y))};
  function matches(r) {
    const f=el('sem-field').value,co=el('sem-company').value,c=el('sem-cohort').value,y=el('sem-year').value,cl=el('sem-cluster').value;
    return (y==='all'||String(r.application_year)===y)&&(cl==='all'||String(r.cluster)===cl)&&r.memberships.some(m=>(f==='all'||m.field===f)&&(co==='all'||m.company===co)&&(c==='all'||String(m.cohort)===c));
  }
  function category(r) {
    const mode=el('sem-color').value;
    if(mode==='cluster')return r.cluster;
    if(mode==='year')return String(r.application_year);
    const key={field:'field',company:'company',cohort:'cohort'}[mode];
    const values=[...new Set(r.memberships.map(m=>String(m[key])))];return values.length===1?values[0]:'복수 선정기록';
  }
  function paint() {
    const rect=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;width=rect.width;height=rect.height;
    canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);
    const cats=[...new Set(selected.map(category))].sort((a,b)=>String(a).localeCompare(String(b),'ko'));
    const color=r=>el('sem-color').value==='cluster'?clusterColor(r.cluster):colors[cats.indexOf(category(r))%colors.length];
    const padding=30,sx=(width-2*padding)/(bounds.xmax-bounds.xmin),sy=(height-2*padding)/(bounds.ymax-bounds.ymin),scale=Math.min(sx,sy)*zoom;
    const mx=(bounds.xmin+bounds.xmax)/2,my=(bounds.ymin+bounds.ymax)/2;
    drawn=selected.map(r=>({r,px:width/2+(r.x-mx)*scale,py:height/2-(r.y-my)*scale}));
    drawn.sort((a,b)=>(a.r.cluster>=0)-(b.r.cluster>=0));
    drawn.forEach(p=>{ctx.beginPath();ctx.fillStyle=color(p.r);ctx.globalAlpha=p.r.cluster<0?.45:.8;ctx.arc(p.px,p.py,width<500?2.3:2.6,0,Math.PI*2);ctx.fill();});ctx.globalAlpha=1;
    ctx.fillStyle='#6d7480';ctx.font='11px "Noto Sans KR", sans-serif';ctx.fillText('UMAP 1 · 축의 절대값에는 기술적 단위가 없음',12,height-12);
    el('semantic-count').textContent=`${selected.length.toLocaleString('ko-KR')} / 3,621건 표시`;
    canvas.setAttribute('aria-label',`특허 제목 의미지도, ${selected.length}건 표시. 각 점은 고유 출원 1건.`);
    const legend=el('semantic-legend');legend.replaceChildren();cats.slice(0,12).forEach((c,i)=>{const item=document.createElement('span'),dot=document.createElement('i');dot.style.background=el('sem-color').value==='cluster'?clusterColor(c):colors[i%colors.length];item.append(dot,el('sem-color').value==='cluster'?name(c):String(c));legend.append(item);});
    if(cats.length>12){const more=document.createElement('span');more.textContent=`외 ${cats.length-12}개 · 전체는 군집 필터에서 확인`;legend.append(more);}
  }
  function rowList() {
    const body=el('semantic-result-rows');body.replaceChildren();selected.slice(0,limit).forEach(r=>{const row=document.createElement('tr');[r.application_number,r.title,r.memberships.map(m=>m.company).join(' · '),r.application_year,name(r.cluster)].forEach(v=>{const td=document.createElement('td');td.textContent=String(v);row.append(td);});body.append(row);});el('semantic-more').hidden=selected.length<=limit;
  }
  function refresh(){selected=dataset.patents.filter(matches);limit=20;paint();rowList();el('semantic-tooltip').hidden=true;}
  controls.forEach(c=>c.addEventListener('change',refresh));
  el('semantic-more').addEventListener('click',()=>{limit+=20;rowList();});
  el('semantic-reset').addEventListener('click',()=>{controls.slice(0,5).forEach(c=>c.value='all');el('sem-color').value='cluster';zoom=1;refresh();});
  el('semantic-zoom-in').addEventListener('click',()=>{zoom=Math.min(4,zoom*1.3);paint();});el('semantic-zoom-out').addEventListener('click',()=>{zoom=Math.max(.7,zoom/1.3);paint();});
  function showNearest(x,y) {
    let nearest=null,d=64;drawn.forEach(p=>{const z=(p.px-x)**2+(p.py-y)**2;if(z<d){d=z;nearest=p;}});
    const tip=el('semantic-tooltip');if(!nearest){tip.hidden=true;return;}
    const r=nearest.r;tip.hidden=false;tip.textContent=`${r.title}\n${r.memberships.map(m=>m.company).join(' · ')}\n출원 ${r.application_year} · ${r.application_number}\nIPC ${r.ipc_subclasses.map(c=>c+' · '+(dataset.ipcLabels[c]||'WIPO 세부 분류 원문 참조')).join('\n')}\n선정분야 ${[...new Set(r.memberships.map(m=>m.field))].join(' · ')}\n의미군집 ${name(r.cluster)}`;
    tip.style.left=`${Math.max(8,Math.min(x+12,width-Math.min(340,width-16)))}px`;tip.style.top=`${Math.max(8,Math.min(y+12,height-190))}px`;
    el('semantic-selected').textContent=tip.textContent;
  }
  canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();showNearest(e.clientX-r.left,e.clientY-r.top);});
  canvas.addEventListener('click',e=>{const r=canvas.getBoundingClientRect();showNearest(e.clientX-r.left,e.clientY-r.top);});canvas.addEventListener('pointerleave',()=>{el('semantic-tooltip').hidden=true;});
  new ResizeObserver(()=>paint()).observe(canvas);refresh();
})();
