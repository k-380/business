from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

rng=np.random.default_rng(6)
nominal=.01
t=np.arange(1000)*nominal+rng.normal(0,.0001,1000)
t=np.delete(t,[200,201,600]);dt=np.diff(t)
estimated=np.maximum(np.rint(dt/nominal).astype(int)-1,0)
print('周期中央値 [s]:',round(float(np.median(dt)),6),'推定欠落数:',int(estimated.sum()))
print('設定fs [Hz]:',1/nominal,'Nyquist [Hz]:',1/(2*nominal))
hist,bins=np.histogram(dt,bins=30)
plot(6,(bins[:-1]+bins[1:])/2,{'間隔の件数':hist},'件数 [個]',xlabel='記録間隔 [s]')
