from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parents[1]
results=[]
for script in sorted((ROOT/'examples').glob('chapter*/run.py'))+sorted((ROOT/'examples').glob('lab*/run.py')):
    r=subprocess.run([sys.executable,str(script)],cwd=ROOT,capture_output=True,text=True)
    (script.parent/'output.txt').write_text(r.stdout,encoding='utf-8')
    results.append({'chapter':script.parent.name,'returncode':r.returncode})
    print(script.parent.name,'PASS' if r.returncode==0 else 'FAIL',flush=True)
    if r.returncode: print(r.stderr);sys.exit(r.returncode)
(ROOT/'examples/verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
