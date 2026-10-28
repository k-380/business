from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('07_modes');t=pd.to_datetime(df['時刻'],utc=True,format='ISO8601');x=df['測定値']
segments=df['mode'].ne(df['mode'].shift()).cumsum()
y,filled=interpolate_short(t,x,max_gap_seconds=30,groups=segments,eligible=df['mode'].eq('run'))
target=truth('07_modes').latent_signal
print('補間数:',int(filled.sum()),'残欠損:',int(y.isna().sum()))
print('模擬真値に対する補間点RMSE:',float(np.sqrt(np.mean((y[filled]-target[filled])**2))))
plot(10,seconds(df),{'観測値':x,'条件付き補間':y,'補間点':y.where(filled)},'温度 [°C]')
