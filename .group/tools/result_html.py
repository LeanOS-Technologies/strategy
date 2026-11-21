"""Build a self-contained reader from this product's current native Markdown state.

Usage: python3 .group/tools/result_html.py STATE [--out result.html] [--open]
No product execution, source revision, model change or acceptance is performed.
"""
import argparse
import base64
import hashlib
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import reader_support as support

PRODUCT = 'strategy'
CONFIG = {
 'strategy': ('Strategy', 'Understand the business choices', 'See how direction, customers and offers connect to the work to do next. Follow a decision to its grounds and recorded status.', [
  ('direction','Direction','What business are we building, and what matters?', ['venture','objectives','positioning-decision','category-definition','bet-portfolio']),
  ('customers','Who to serve','Understand the buying situations, needs and alternatives.', ['segments','target-segments','opportunities','differentiation']),
  ('offers','What to offer','Connect the promised outcome, delivery and commercial relationship.', ['offer-catalogue','revenue-model','price-book']),
  ('next','What happens next','Inspect recorded actions, dependencies and unresolved decisions.', ['focus-plan','open-questions'])]),
 'messaging': ('Messaging', 'Find what to say and why', 'Explore the ideas, the people they matter to and the material that supports them. Evidence stays at its recorded stage.', [
  ('messages','The message','Start with the organising argument and reusable explanations.', ['strategic-narrative','message-system']),
  ('audiences','Who it matters to','See how the explanation changes with the reader’s situation.', ['audience-messages']),
  ('value','What it makes possible','Connect a product’s value to its actual mechanism and conditions.', ['product-value-models']),
  ('support','What supports it','Inspect proof, its actual maturity and the language to reuse.', ['proof-system','lexicon','open-questions'])]),
 'brand': ('Brand', 'Put the character into practice', 'Understand the character, then see how it becomes voice, visual choices and usable material. Open the grounds behind each system.', [
  ('character','The character','What the venture believes, how it behaves and what it is called.', ['character','architecture-and-naming']),
  ('memory','When it comes to mind','The buying situations the venture should be remembered in.', ['entry-points']),
  ('voice','How it speaks','Voice, tone, words and rewrites with their actual examples.', ['voice']),
  ('assets','What stays the same','The few assets that must repeat everywhere, with the mark, colour and type they need.', ['distinctive-assets'])])
}
LABELS={'venture':'The business','objectives':'What matters','target-segments':'Who to serve','segments':'Buying situations','offer-catalogue':'What to offer','focus-plan':'What to do next','open-questions':'Unresolved decisions','message-system':'Reusable messages','proof-system':'Proof and its stage','strategic-narrative':'The organising argument','character':'The character','architecture-and-naming':'Names','entry-points':'Buying situations','voice':'The voice','distinctive-assets':'Distinctive assets'}
SAFE_ASSETS={'.svg','.png','.jpg','.jpeg','.webp','.wav','.mp3','.woff2','.css','.json'}
REF = re.compile(r'\b(?:MSG|ARG|ANS|DST|PRF|CON|CH|PRI|TGT|SEG|OPP|OFF|REV|BET|ACT|OBJ|ADV|ALT|POS|CAT|PRC|VO|VC|RULE|VAL|TRT|PRN|MEM|NR|NP|CEP|VA|TRM|PAT|RW|CUE|AST|SRF|PIL|OBN|ROL|PHR)-\d+\b')


DECLARATION = re.compile(r'^(?:###\s+|\|\s*)([A-Z][A-Z0-9]{0,8}-\d+)\b', re.M)
VALUE = re.compile(r'(?<![\w-])(?:([a-z0-9][a-z0-9-]*)/)?((?:SIT|MCH|CASE)-\d+)\b')
REFERENCE = re.compile(VALUE.pattern + '|' + REF.pattern)


def declared_identifiers(text):
    identifiers=re.findall(r'^###\s+([A-Z][A-Z0-9]{0,8}-\d+)\b',text,re.M)
    lines=text.splitlines()
    for i,line in enumerate(lines[:-1]):
        if not line.startswith('|') or not re.match(r'^\s*\|?[\s:|-]+\|\s*$',lines[i+1]):continue
        headers=cells(line)
        if 'ID' not in headers:continue
        column=headers.index('ID');j=i+2
        while j<len(lines) and lines[j].startswith('|'):
            row=cells(lines[j])
            if column<len(row) and re.fullmatch(r'[A-Z][A-Z0-9]{0,8}-\d+',plain(row[column])):identifiers.append(plain(row[column]))
            j+=1
    return list(dict.fromkeys(identifiers))


def references_for(files, root):
    """Keep global record links and product-scoped value links in one reader."""
    refs={}
    for index,path in enumerate(files):
        slug='doc-'+str(index);refs.setdefault('@doc:'+path.stem,slug)
        scope=path.stem if 'product-value-models' in path.parts else None
        records={};aliases={}
        for identifier in declared_identifiers(path.read_text()):
            if identifier in records:continue
            is_value=identifier.split('-')[0] in ['SIT','MCH','CASE'] and scope
            key=scope+'/'+identifier if is_value else identifier
            target=key if is_value and key not in refs else slug+'--'+identifier
            if key not in refs and not is_value:aliases[target]=identifier
            refs.setdefault(key,target);records[identifier]=target
        refs['@records:'+slug]=records;refs['@aliases:'+slug]=aliases;refs['@scope:'+slug]=scope
    return refs


def document_references(refs, slug):
    local=dict(refs);local.update(refs.get('@records:'+slug,{}));local['@scope']=refs.get('@scope:'+slug);local['@aliases']=refs.get('@aliases:'+slug,{})
    return local


class ReferenceLinker(HTMLParser):
    """Link text nodes only; existing source links never become nested anchors."""
    def __init__(self, refs):
        super().__init__(convert_charrefs=False);self.refs=refs;self.output=[];self.in_anchor=0

    def handle_starttag(self,tag,attrs):
        self.output.append(self.get_starttag_text())
        if tag=='a':self.in_anchor+=1

    def handle_endtag(self,tag):
        self.output.append('</'+tag+'>')
        if tag=='a':self.in_anchor=max(0,self.in_anchor-1)

    def handle_entityref(self,name):self.output.append('&'+name+';')
    def handle_charref(self,name):self.output.append('&#'+name+';')

    def handle_data(self,text):
        if self.in_anchor:self.output.append(text);return
        def linked(match):
            source=match[0];value=VALUE.fullmatch(source)
            if value:
                scope=value[1] or self.refs.get('@scope')
                target=self.refs.get(scope+'/'+value[2]) if scope else None
                if not value[1] and value[2] in self.refs:target=self.refs[value[2]]
            else:target=self.refs.get(source)
            return "<a href='#"+escape(target,quote=True)+"'>"+source+"</a>" if target else source
        self.output.append(REFERENCE.sub(linked,text))


def anchor_attributes(identifier, refs, used):
    anchor=refs.get(identifier)
    if not anchor or anchor in used:return '', ''
    used.add(anchor)
    alias=refs.get('@aliases',{}).get(anchor)
    prefix=("<span class='anchor-target' tabindex='-1' id='"+escape(alias,quote=True)+"'></span>") if alias else ''
    return prefix, " id='"+escape(anchor,quote=True)+"' tabindex='-1'"


def files_in(root):
    files=list(root.glob('*.md'))
    for folder in ['audience-messages','product-value-models','strategy-reviews','name-candidates']:
        files += list((root/folder).glob('*.md'))
    order = [name for _,_,_,names in CONFIG[PRODUCT][3] for name in names]
    return sorted(files, key=lambda p: (order.index(p.stem) if p.stem in order else order.index(p.relative_to(root).parts[0]) if p.relative_to(root).parts[0] in order else len(order), str(p)))


def chapter_for(path):
    for key, label, description, names in CONFIG[PRODUCT][3]:
        if path.stem in names or path.parts[0] in names:
            return key
    return 'other'


def plain(text):
    return re.sub(r'[`*]', '', re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',text)).strip()


def inline(text, refs):
    value=escape(text)
    # All source links become labels. Available record references are local links.
    value=re.sub(r'!?\[([^\]]+)\]\(([^)]+)\)',lambda m: '<a href="#'+refs['@doc:'+Path(m[2]).stem]+'">'+m[1]+'</a>' if '@doc:'+Path(m[2]).stem in refs else m[1],value)
    value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
    linker=ReferenceLinker(refs);linker.feed(value);return ''.join(linker.output)


def cells(line):
    return [x.strip().replace('\\|','|') for x in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def markdown(text, slug, refs):
    lines=text.splitlines(); out=[]; i=0; used=set()
    def render(value): return inline(value,refs)
    while i<len(lines):
        line=lines[i]
        if not line.strip(): i+=1;continue
        if line.startswith('|') and i+1<len(lines) and re.match(r'^\s*\|?[\s:|-]+\|\s*$',lines[i+1]):
            headers=cells(line);i+=2
            while i<len(lines) and lines[i].startswith('|'):
                values=cells(lines[i]);column=headers.index('ID') if 'ID' in headers else None
                identifier=plain(values[column]) if column is not None and column<len(values) else ''
                alias,attr=anchor_attributes(identifier,refs,used)
                out.append(alias)
                title=next((values[j] for j,h in enumerate(headers) if h in ['Offer','Action and output','Segment','Target','Point','Trait','Principle','Rule','Role','Job','Concept','Name'] and j<len(values)),values[0] if values else 'Record')
                out.append('<article class="record anchor-target"'+attr+'><h3>'+render(title)+'</h3>')
                status=[f'{h}: {v}' for h,v in zip(headers,values) if h.lower() in ['status','state','basis','source and status']]
                if status: out.append('<span class="status">'+render(' · '.join(status))+'</span>')
                important=[(h,v) for h,v in zip(headers,values) if h not in ['ID','SHA256','Path','Format','Derived from','Evidence']]
                extra=[(h,v) for h,v in zip(headers,values) if h in ['ID','SHA256','Path','Format','Derived from','Evidence']]
                out.append('<dl>'+''.join('<dt>'+render(h)+'</dt><dd>'+render(v)+'</dd>' for h,v in important)+'</dl>')
                if extra:out.append('<details><summary>Source and technical fields</summary><dl>'+''.join('<dt>'+render(h)+'</dt><dd>'+render(v)+'</dd>' for h,v in extra)+'</dl></details>')
                out.append('</article>');i+=1
            continue
        heading=re.match(r'^(#{1,6})\s+(.+)',line)
        if heading:
            title=heading[2];level=min(4,max(2,len(heading[1])));m=re.match(r'[A-Z][A-Z0-9]{0,8}-\d+',title)
            alias,attr=anchor_attributes(m[0] if m else '',refs,used);out.append(alias)
            out.append(f'<h{level} class="anchor-target"{attr}>'+escape(plain(title))+f'</h{level}>');i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if re.match(r'^\s*[-*]\s+',line):
            out.append('<ul>')
            while i<len(lines) and re.match(r'^\s*[-*]\s+',lines[i]):out.append('<li>'+render(re.sub(r'^\s*[-*]\s+','',lines[i]))+'</li>');i+=1
            out.append('</ul>');continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||```|[-*] )',lines[i]):para.append(lines[i]);i+=1
        out.append('<p>'+render('\n'.join(para))+'</p>')
    return '\n'.join(out)


def assets_for(text, path, root):
    assets=[];seen=set()
    # Preserve native resource paths and ordinary linked material. Metadata citations
    # are not an instruction to import unrelated evidence or owner documents.
    paths=[];lines=text.splitlines()
    for i,line in enumerate(lines[:-1]):
        if not line.startswith('|') or not re.match(r'^\s*\|?[\s:|-]+\|\s*$',lines[i+1]):continue
        headers=cells(line)
        if 'Path' not in headers:continue
        column=headers.index('Path');j=i+2
        while j<len(lines) and lines[j].startswith('|'):
            values=cells(lines[j])
            if column<len(values):paths.append(plain(values[column]))
            j+=1
    paths+=re.findall(r'\[[^\]]+\]\(([^)]+)\)',text)
    paths+=re.findall(r'[\w./-]+\.(?:svg|png|jpg|jpeg|webp|wav|mp3|ogg|woff2|css|json)\b',text)
    for raw in paths:
        candidates=[path.parent/raw,root/raw,root/(raw[len(PRODUCT)+1:] if raw.startswith(PRODUCT+'/') else raw)]
        target=next((p.resolve() for p in candidates if p.is_file() and root.resolve() in p.resolve().parents),None)
        if target is None or target in seen:continue
        seen.add(target);assets.append({'name':target.name,'type':target.suffix.lower(),'url':support.data_url(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    return assets


def render(root, *, include_candidates=False, candidate_mode=None):
    root=Path(root);files=files_in(root);docs=[];asset_sources={}
    mode=candidate_mode or ('overlay' if include_candidates else 'current')
    if mode=='overlay':
        working={str(p.relative_to(root)):p for p in files};working.update({str(p.relative_to(root/'candidate')):p for p in files_in(root/'candidate')});files=list(working.values())
    elif mode=='compare':
        files+=files_in(root/'candidate')
        def comparison_key(path):
            candidate=root/'candidate' in path.parents
            relative=path.relative_to(root/'candidate' if candidate else root)
            return (str(relative),candidate)
        files.sort(key=comparison_key)
    refs=references_for(files,root)
    for index,p in enumerate(files):
        raw=p.read_bytes().decode('utf-8');slug='doc-'+str(index);candidate=root/'candidate' in p.parents
        relative=p.relative_to(root/'candidate' if candidate else root)
        assets=assets_for(raw,p,root) if PRODUCT=='brand' else []
        if PRODUCT=='messaging' and p.stem=='proof-system':
            proof=p.parent/'proof-system'
            for file in sorted(proof.rglob('*')) if proof.is_dir() else []:
                if file.is_file() and root.resolve() in file.resolve().parents:
                    assets.append({'name':str(file.relative_to(proof)),'type':file.suffix.lower(),'url':support.data_url(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
        for asset in assets:
            key=asset['sha256']+asset['type'];asset_sources.setdefault(key,asset.pop('url'));asset['asset_key']=key
        change=re.search(r'^Change:\s*(.+)',raw,re.M)
        docs.append({'slug':slug,'file':str(p.relative_to(root)),'text':raw,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chapter':chapter_for(relative),'assets':assets,'variant':'candidate' if candidate else 'current','logical_file':str(relative),'change':change[1] if change else None})
    cards=[]
    for d in docs:
        local_refs=document_references(refs,d['slug'])
        raw=d['text'];title=re.search(r'^# (.+)',raw,re.M);title=plain(title[1]) if title else Path(d['file']).stem.replace('-',' ')
        d['title']=title;label=LABELS.get(Path(d['file']).stem,title)
        conclusion=re.search(r'^## Conclusion\s+(.+?)(?=\n## |\Z)',raw,re.M|re.S)
        excerpt=conclusion[1].strip().split('\n\n')[0] if conclusion else 'Open the current record to inspect its choices, grounds and unresolved work.'
        excerpt=re.split(r'(?<=[.!?])\s+(?=[A-Z])',excerpt)[0]
        if len(excerpt)>650:excerpt=excerpt[:650].rsplit(' ',1)[0]+'…'
        preview='<p class="choice-preview">'+escape(plain(excerpt))+'</p>'
        status=re.search(r'^Status:\s*(.+)',raw,re.M);status=status[1] if status else 'No document-level acceptance status recorded; inspect individual records.'
        # Metadata is retained exactly in the downloadable native source; start reading at Conclusion.
        body=re.split(r'^## ',raw,maxsplit=1,flags=re.M)
        body='## '+body[1] if len(body)>1 else raw
        asset_html=[]
        for a in d['assets']:
            asset_preview=('<img alt="'+escape(a['name'])+'" data-asset="'+escape(a['asset_key'],quote=True)+'">') if a['type'] in ['.svg','.png','.jpg','.jpeg','.webp'] else ('<audio controls preload="none" data-asset="'+escape(a['asset_key'],quote=True)+'"></audio>' if a['type'] in ['.wav','.mp3','.ogg'] else '')
            asset_html.append('<div class="asset">'+asset_preview+'<p><a class="source-download" download="'+escape(a['name'])+'" data-asset="'+escape(a['asset_key'],quote=True)+'">Download '+escape(a['name'])+'</a></p></div>')
        palette=''
        if PRODUCT=='brand' and Path(d['file']).stem=='distinctive-assets':
            colours=list(dict.fromkeys(re.findall(r'#[0-9a-fA-F]{6}\b',raw)))
            palette='<h2>Colours in this source</h2><p>Inspect each role and permitted combination in the source below.</p>'+''.join('<span class="swatch"><i style="background:'+c+'" aria-hidden="true"></i><code>'+c+'</code></span>' for c in colours)
        cards.append('<article id="'+d['slug']+'" class="document-card" data-variant="'+d['variant']+'" data-chapter="'+d['chapter']+'">'+(('<span class="status">'+('Candidate · '+escape(d['change'] or 'change unspecified') if d['variant']=='candidate' else 'Current')+'</span>') if mode=='compare' or d['variant']=='candidate' else '')+'<button type="button" class="document-open" aria-expanded="false" aria-controls="'+d['slug']+'--body"><span>'+escape(label)+'</span><span class="disclosure-chevron" aria-hidden="true"></span></button><p class="source-meta">'+escape(title)+'</p>'+preview+'<div id="'+d['slug']+'--body" class="document-body" hidden><span class="status">'+escape(status)+'</span>'+palette+'<div class="prose">'+markdown(body,d['slug'],local_refs)+'</div>'+('<h2>Available material</h2><div class="asset-list">'+''.join(asset_html)+'</div>' if asset_html else '')+'<details><summary>Exact native source and revision</summary><p class="source-meta">SHA256 '+d['sha256']+'</p><a class="source-download" href="data:text/markdown;base64,'+base64.b64encode(raw.encode()).decode()+'" download="'+escape(Path(d['file']).name)+'">Download native Markdown</a><pre>'+escape(raw)+'</pre></details><button class="quiet close-document" type="button">Back to choices</button></div></article>')
    if mode=='compare':
        pairs=[]
        for logical in dict.fromkeys(d['logical_file'] for d in docs):
            indices=[i for i,d in enumerate(docs) if d['logical_file']==logical]
            pairs.append('<section class="candidate-pair" aria-label="'+escape(logical,quote=True)+'">'+''.join(cards[i] for i in indices)+'</section>')
        card_html=''.join(pairs)
    else:card_html=''.join(cards)
    product,title,lead,chapters=CONFIG[PRODUCT]
    entries=''.join('<article class="entry-card"><span class="eyebrow">'+str(sum(d['chapter']==key for d in docs))+' sources</span><strong>'+label+'</strong><span>'+description+'</span><a class="entry-action" href="#chapter='+key+'" data-chapter-link="'+key+'">View '+label+'</a></article>' for key,label,description,_ in chapters)
    nav='<nav id="reading-choices" class="chapter-nav" aria-label="Reading paths"><button type="button" data-chapter-link="all" aria-current="page">All choices</button>'+''.join('<button type="button" data-chapter-link="'+key+'">'+label+'</button>' for key,label,_,_ in chapters)+'</nav>'
    body='<div class="entry-grid">'+entries+'</div>'+nav+'<form class="toolbar" role="search"><label>Find a decision, idea or condition<input id="search" type="search" placeholder="Search the complete native sources"></label><button type="reset" class="quiet">Clear search</button></form><p id="status" role="status"></p><div class="document-list">'+card_html+'</div><p id="empty" class="empty" hidden>No sources match. Clear the search or choose All choices.</p>'
    script=(Path(__file__).parent/'result_reader.js').read_text()
    notice=next((re.search(r'^Disclosure:\s*(.+)',d['text'],re.M)[1] for d in docs if re.search(r'^Disclosure:\s*(.+)',d['text'],re.M)), '')
    return support.shell(product,title,lead,body,{'product':PRODUCT,'documents':docs,'assets':asset_sources},script,note=notice)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('state',type=Path);parser.add_argument('--compare-candidates',action='store_true',help='show current and proposed native documents together');parser.add_argument('--candidate',action='store_true',help='explicitly overlay candidate native files on the current state for this delivery');parser.add_argument('--out',type=Path);parser.add_argument('--open',action='store_true');args=parser.parse_args()
    if not args.state.is_dir():parser.error('state must be the current native document directory')
    output=args.out or args.state/'result.html';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(render(args.state,include_candidates=args.candidate,candidate_mode='compare' if args.compare_candidates else None),encoding='utf-8');print(output.resolve())
    return 1 if args.open and not support.open_result(output) else 0

if __name__=='__main__':raise SystemExit(main())
