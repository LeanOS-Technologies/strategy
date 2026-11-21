(() => {
 const root=document.querySelector('.tool-content'),q=document.getElementById('tool-search'),status=document.getElementById('tool-status'),nav=document.getElementById('tool-nav');
 root.querySelectorAll(':scope>h2').forEach((h,i)=>{if(!h.id)h.id='tool-section-'+i;const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;nav.append(a);});
 root.querySelectorAll('.wrap').forEach(w=>{w.tabIndex=0;w.setAttribute('role','region');w.setAttribute('aria-label',w.querySelector('th')?.textContent+' table');});
 function filter(){
  if(root.querySelector('#catalog-records')){status.textContent='Choose a model and table below. Search narrows the selected table.';return;}
  const query=q.value.trim().toLocaleLowerCase(),records=[...root.querySelectorAll('.grid>.card,.layouts>.layout,tbody>tr'),...root.querySelectorAll(':scope>details')];let found=0;
  for(const e of records){const context=e.closest('details')?.querySelector(':scope>summary')?.textContent||'';e.hidden=!!query&&!(e.textContent+' '+context).toLocaleLowerCase().includes(query);if(!e.hidden)found++;}
  for(const detail of root.querySelectorAll('details')){if(query&&detail.textContent.toLocaleLowerCase().includes(query)){if(!('toolSearchOpen' in detail.dataset))detail.dataset.toolSearchOpen=String(detail.open);detail.open=true;}else if(!query&&'toolSearchOpen' in detail.dataset){detail.open=detail.dataset.toolSearchOpen==='true';delete detail.dataset.toolSearchOpen;}}
  status.textContent=query?(found?`${found} of ${records.length} entries match “${q.value}”.`:'No matches. Clear the search to explore the tool again.'):`${records.length} tool entries. Explore the definitions and how they connect.`;
 }
 q.addEventListener('input',filter);q.form.addEventListener('submit',e=>e.preventDefault());q.form.addEventListener('reset',()=>setTimeout(filter,0));
 for(const b of root.querySelectorAll('[data-geometry-view]'))b.onclick=()=>{root.dataset.geometryView=b.dataset.geometryView;for(const x of root.querySelectorAll('[data-geometry-view]'))x.setAttribute('aria-pressed',String(x===b));};
 document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;let target=document.getElementById(decodeURIComponent(a.hash.slice(1)));if(!target)return;for(let p=target.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;target.tabIndex=-1;target.focus({preventScroll:true});});
 filter();
})();
