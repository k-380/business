from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'python-timeseries-cleaning.zip'
temporary=ROOT/'python-timeseries-cleaning.zip.tmp'
with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p in (target,temporary):continue
        rel=p.relative_to(ROOT)
        if any(s in ('.venv','__pycache__','.pytest_cache','results') for s in rel.parts) or p.suffix=='.pyc':continue
        z.write(p,Path(ROOT.name)/rel)
with ZipFile(temporary) as z:
    if z.testzip() is not None:raise ValueError('archive integrity check failed')
temporary.replace(target)
print(target.name,target.stat().st_size,'bytes')
