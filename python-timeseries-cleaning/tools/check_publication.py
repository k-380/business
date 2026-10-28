"""Verify the deployed static site against local files; URL must be confirmed first."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
from urllib.parse import urljoin
from zipfile import ZipFile
from io import BytesIO
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
base=sys.argv[1].rstrip('/')+'/'
book=urljoin(base,'python-timeseries-cleaning/')
paths=['index.html','getting-started.html','labs.html','downloads.html','glossary.html','datasets.html','implementation.html','verification.html','single-file.html','references/bibliography.html']+[f'chapters/chapter{i:02d}.html' for i in range(1,25)]+['assets/css/book.css','assets/js/book.js','assets/js/search-index.js']+[f'assets/images/chapter{i:02d}.svg' for i in range(1,31)]+['python-timeseries-cleaning.zip']
def read(url):
    with urlopen(Request(url,headers={'Cache-Control':'no-cache'}),timeout=40) as r:return r.status,r.read()
def verify(path):
    status,b=read(urljoin(book,path));local=(ROOT/path).read_bytes()
    assert status==200 and hashlib.sha256(b).digest()==hashlib.sha256(local).digest(),path
    if path.endswith('.zip'):
        with ZipFile(BytesIO(b)) as z:assert z.testzip() is None
    return {'path':path,'http_status':status,'bytes':len(b),'sha256_matches_local':True}
with ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(verify,paths))
status,top=read(urljoin(base,'index.html'))
assert status==200 and b'./python-timeseries-cleaning/index.html' in top
assert top==ROOT.parent.joinpath('index.html').read_bytes()
result={'base_url':base,'book_url':urljoin(book,'index.html'),'checked_files':len(results),'root_index_link':'pass','all_bytes_match_local':True,'zip_crc':'pass','files':results}
(ROOT/'tests/publication-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='files'},ensure_ascii=False,indent=2))
