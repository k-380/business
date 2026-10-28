from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from scipy.signal import correlate,correlation_lags
df=load('05_sync');a=df.reference_trigger.to_numpy();b=np.r_[np.zeros(7),a[:-7]]
c=correlate(b-b.mean(),a-a.mean(),mode='full');lags=correlation_lags(len(b),len(a))
lag=int(lags[np.argmax(c)]);print('Bの遅れ [sample]:',lag,'遅れ [s]:',lag*.1)
recorded=seconds(df)+.7;corrected=(recorded-.7)/1.0002
print('トリガー校正式の最大残差 [s]:',np.max(np.abs(corrected-df.reference_time_s)))
plot(8,df.reference_time_s,{'補正前時刻誤差':recorded-df.reference_time_s,'補正後時刻誤差':corrected-df.reference_time_s},'同期誤差 [s]')
