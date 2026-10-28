from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('09_prototypes');a=pd.DataFrame({'t':pd.to_datetime(df['時刻'],utc=True,format='ISO8601'),'a':df['測定値']})
b=pd.DataFrame({'tb':a.t[::2]+pd.Timedelta(milliseconds=200),'b':df.prototype_B[::2]})
m=pd.merge_asof(a,b,left_on='t',right_on='tb',direction='nearest',tolerance=pd.Timedelta(milliseconds=400))
print('左行数保持:',len(m)==len(a),'未対応:',int(m.b.isna().sum()))
print('最大対応時刻差 [s]:',float((m.t-m.tb).dt.total_seconds().abs().max()))
plot(17,seconds(df),{'試作品A':m.a,'試作品B（対応点のみ）':m.b},'温度 [°C]')
