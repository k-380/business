from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from tempfile import TemporaryDirectory
from tsclean.app import main
with TemporaryDirectory() as folder:
    code=main(['--input',str(ROOT/'datasets/raw/02_pressure.csv'),'--config',str(ROOT/'configs/02_pressure.yaml'),'--output',str(Path(folder)/'result')])
    assert code==0
    p=Path(folder)/'result/000_00_02_pressure/clean_data.xlsx'
    df=pd.read_excel(p)
    assert df.value__numeric.equals(df.value__analysis)
    print('Excel再読込:',len(df),'行。初期設定で値の変更なし。')
    plot(24,np.arange(len(df)),{'数値化した元データ':df.value__numeric,'解析用データ':df.value__analysis},'圧力 [MPa]',xlabel='取得順序')
