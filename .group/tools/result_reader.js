(() => {
 'use strict';
 const data=JSON.parse(document.getElementById('result-data').textContent), cards=[...document.querySelectorAll('.document-card')], search=document.getElementById('search');
 document.querySelectorAll('[data-asset]').forEach(e=>{const url=data.assets?.[e.dataset.asset];if(url){if(e.tagName==='A')e.href=url;else e.src=url;}});
 let chapter=[...document.querySelectorAll('.entry-action[data-chapter-link]')].find(link=>cards.some(card=>card.dataset.chapter===link.dataset.chapterLink))?.dataset.chapterLink || 'all';
 const open=card=>{const control=card.querySelector('.document-open');control.setAttribute('aria-expanded','true');card.querySelector('.document-body').hidden=false;};
 function filter(){
  const query=search.value.trim().toLocaleLowerCase();let count=0;
  cards.forEach((card,i)=>{card.hidden=(chapter!=='all' && card.dataset.chapter!==chapter)||!data.documents[i].text.toLocaleLowerCase().includes(query);if(!card.hidden)count++;});
  document.getElementById('status').textContent=`${count} of ${cards.length} sources${query?' matching “'+search.value+'”':''}. Open a choice to read its meaning, grounds and status.`;
  document.getElementById('empty').hidden=!!count;document.querySelectorAll('.candidate-pair').forEach(pair=>pair.hidden=![...pair.querySelectorAll('.document-card')].some(card=>!card.hidden));
  document.querySelectorAll('[data-chapter-link]').forEach(b=>{if(b.dataset.chapterLink===chapter)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
 }
 document.querySelectorAll('[data-chapter-link]').forEach(b=>b.onclick=e=>{e.preventDefault();chapter=b.dataset.chapterLink;filter();if(b.matches('a.entry-action')){history.pushState(null,'',b.hash);document.querySelector('.chapter-nav').scrollIntoView();document.querySelector('.document-card:not([hidden]) .document-open')?.focus({preventScroll:true});}});
 cards.forEach(card=>{
  const prose=card.querySelector('.prose'),toc=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Jump to a section or record';toc.append(summary);
  prose.querySelectorAll('h2,h3').forEach((h,i)=>{if(!h.id)h.id=card.id+'--section-'+i;const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;a.className='source-download';a.style.display='block';toc.append(a);});card.querySelector('.document-body').prepend(toc);
  card.querySelector('.document-open').onclick=()=>{const control=card.querySelector('.document-open'),isOpen=control.getAttribute('aria-expanded')==='true';control.setAttribute('aria-expanded',String(!isOpen));card.querySelector('.document-body').hidden=isOpen;if(!isOpen){history.pushState(null,'','#'+card.id);if(search.value){const q=search.value.toLocaleLowerCase(),target=[...card.querySelectorAll('.prose p,.prose dd,.prose h3')].find(n=>n.textContent.toLocaleLowerCase().includes(q));if(target){target.tabIndex=-1;target.focus();target.scrollIntoView({block:'center'});}}}};card.querySelector('.close-document').onclick=()=>{card.querySelector('.document-body').hidden=true;card.querySelector('.document-open').setAttribute('aria-expanded','false');card.querySelector('.document-open').focus();};});
 function follow(){const id=decodeURIComponent(location.hash.slice(1));if(id.startsWith('chapter=')){const key=id.slice(8);if(![...document.querySelectorAll('[data-chapter-link]')].some(b=>b.dataset.chapterLink===key))return;chapter=key;search.value='';filter();const target=document.querySelector('.document-card:not([hidden]) .document-open')||document.getElementById('reading-choices');target.tabIndex=-1;target.focus();target.scrollIntoView({block:'start'});return;}const target=document.getElementById(id);if(!target)return;chapter='all';search.value='';filter();const card=target.closest('.document-card');if(card)open(card);target.tabIndex=-1;target.scrollIntoView({block:'start'});target.focus({preventScroll:true});}
 search.oninput=filter;search.form.onsubmit=e=>e.preventDefault();search.form.onreset=()=>setTimeout(filter,0);window.addEventListener('hashchange',follow);window.addEventListener('popstate',follow);filter();follow();
})();
