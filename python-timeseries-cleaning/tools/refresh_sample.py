"""Regenerate only the bundled, synthetic CLI demonstration outputs."""
from pathlib import Path
import tempfile,subprocess,sys,shutil
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    output=Path(d)/'report'
    subprocess.run([sys.executable,str(ROOT/'clean_timeseries.py'),'--input',str(ROOT/'datasets/raw/02_pressure.csv'),'--config',str(ROOT/'configs/02_pressure.yaml'),'--output',str(output)],check=True,cwd=ROOT)
    shutil.copytree(output,ROOT/'examples/chapter24/sample-results',dirs_exist_ok=True)
