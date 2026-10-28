"""Offline link, fragment, dependency and chapter-content verification."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]

class Doc(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.external=[];self.tags={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags[tag]=self.tags.get(tag,0)+1
        if 'id' in a:self.ids.append(a['id'])
        for key in ['href','src']:
            if key in a:
                if urlsplit(a[key]).scheme in ['http','https']:
                    if tag in ['script','img','link']:self.external.append(a[key])
                else:self.refs.append((tag,a[key]))

def main():
    docs={};errors=[];links=0
    import xml.etree.ElementTree as ET
    for svg in (ROOT/'assets/images').glob('*.svg'):
        try:ET.parse(svg)
        except ET.ParseError as exc:errors.append(f'invalid SVG: {svg.name}: {exc}')
    for p in ROOT.rglob('*.html'):
        d=Doc();d.feed(p.read_text(encoding='utf-8'));docs[p.resolve()]=d
        if len(set(d.ids))!=len(d.ids):errors.append(f'duplicate ids: {p.relative_to(ROOT)}')
        if d.external:errors.append(f'external rendering dependencies: {p.relative_to(ROOT)}')
    for p,d in docs.items():
        for tag,ref in d.refs:
            u=urlsplit(ref)
            if u.scheme or ref.startswith('data:'):continue
            dest=(p.parent/unquote(u.path)).resolve() if u.path else p
            if not dest.exists():errors.append(f'missing: {p.relative_to(ROOT)} -> {ref}')
            elif u.fragment and dest in docs and unquote(u.fragment) not in docs[dest].ids:errors.append(f'fragment: {p.relative_to(ROOT)} -> {ref}')
            links+=1
    for n in range(1,25):
        p=(ROOT/f'chapters/chapter{n:02d}.html').resolve()
        if p not in docs:errors.append(f'missing chapter {n}');continue
        text=p.read_text()
        for required in ['学習目標','基礎演習','応用演習','実務演習','章末まとめ','class="answers"',f'id="fig{n:02d}"']:
            if required not in text:errors.append(f'chapter {n}: missing {required}')
        if docs[p].tags.get('pre',0)<2:errors.append(f'chapter {n}: missing code/output')
    result={'html_files':len(docs),'local_links_checked':links,'errors':errors}
    (ROOT/'tests/html-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
