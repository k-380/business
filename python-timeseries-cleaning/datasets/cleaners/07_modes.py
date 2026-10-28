from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tsclean.app import main
if __name__=='__main__':
    output=sys.argv[1] if len(sys.argv)>1 else str(ROOT/'results/07_modes')
    raise SystemExit(main(['--input',str(ROOT/'datasets/raw/07_modes.csv'),'--config',str(ROOT/'configs/07_modes.yaml'),'--output',output]))
