"""Run the complete chapter example as the foundation exercise."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[2]/'examples/chapter07/run.py'),run_name='__main__')
