from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('04_current');x=df['測定値'];y=truth('04_current').latent_signal
sat=x.abs().ge(12)
q=24/4096
print('飽和候補数:',int(sat.sum()),'12bit量子化幅 [A]:',q,'一様誤差モデルu [A]:',q/np.sqrt(12))
print('記録ピーク:',x.abs().max(),'模擬真値ピーク:',y.abs().max())
plot(14,seconds(df)[:300],{'クリップした観測':x[:300],'模擬真値':y[:300]},'電流 [A]')
