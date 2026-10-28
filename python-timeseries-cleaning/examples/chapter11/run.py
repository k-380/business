from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('02_pressure');x=df['測定値'];h=hampel(x,11,k=3.5,floor=.01)
z=(x-x.mean())/x.std(ddof=1)
q1,q3=x.quantile([.25,.75]);iqr=q3-q1
print('Z>3:',int(z.abs().gt(3).sum()),'IQR候補:',int(((x<q1-1.5*iqr)|(x>q3+1.5*iqr)).sum()),'Hampel候補:',int(h.candidate.sum()))
print('MAD未評価:',int((~h.assessed).sum()))
plot(11,seconds(df),{'観測値':x,'局所候補':x.where(h.candidate)},'圧力 [MPa]')
