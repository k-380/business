from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from scipy.signal import resample_poly
df=load('03_vibration');x=df['測定値'].to_numpy()
y=resample_poly(x,1,4);naive=x[::4]
f=np.fft.rfftfreq(len(y),d=.004)
amp=lambda z:2*np.abs(np.fft.rfft(z))/len(z)
print('入力/出力行数:',len(x),len(y),'出力fs:',250)
print('130 Hz成分は新Nyquist 125 Hzを超えるため保存できない。')
plot(7,f,{'単純間引き':amp(naive),'低域通過後に間引き':amp(y)},'片側振幅 [m/s²]',xlabel='周波数 [Hz]')
