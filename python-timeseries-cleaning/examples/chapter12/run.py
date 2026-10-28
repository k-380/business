from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from scipy.ndimage import median_filter
df=load('02_pressure');x=df['測定値'];proposal=pd.Series(median_filter(x,size=5,mode='reflect'))
# この模擬問題ではmanifestで測定不具合と判明した2点だけを承認した。
approved=pd.Series(False,index=x.index);approved.iloc[[90,270]]=True
y=x.where(~approved,proposal)
print('承認修正数:',int(approved.sum()),'実現象のピーク保持:',bool(y.iloc[350]==x.iloc[350]))
plot(12,seconds(df),{'観測値':x,'承認した2点のみ修正':y},'圧力 [MPa]')
