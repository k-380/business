from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('07_modes');segment=df['mode'].ne(df['mode'].shift()).cumsum()
print(df.assign(segment=segment).groupby(['segment','mode'])['測定値'].agg(['count','mean','max']).to_string())
dt=10;rate=df['測定値'].diff()/dt
steady=rate.abs().rolling(12,min_periods=12).max().lt(.03)&df['mode'].eq('run')
print('演習基準の定常候補点数:',int(steady.sum()))
plot(18,seconds(df),{'温度':df['測定値'],'定常候補':df['測定値'].where(steady)},'温度 [°C]')
