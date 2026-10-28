from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('01_temperature');x=pd.to_numeric(df['測定値'],errors='coerce')
n=len(x);missing=x.isna().sum()
print(f'行数={n}, 欠損={missing}, 欠損率={missing/n:.6f}, 完全性={1-missing/n:.6f}')
hours=(seconds(df)//3600).astype(int)
rate=x.isna().groupby(hours).mean()
plot(4,rate.index,{'時間帯別欠損率':rate},'欠損率 [1]',xlabel='開始後 [h]')
