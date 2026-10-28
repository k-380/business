from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from scipy.signal import butter,sosfilt,sosfiltfilt
df=load('03_vibration');x=df['測定値'].to_numpy();t=seconds(df)
sos=butter(4,180,fs=1000,output='sos')
causal=sosfilt(sos,x);zero=sosfiltfilt(sos,x)
print('原波形RMS:',np.sqrt(np.mean(x*x)),'ゼロ位相後RMS:',np.sqrt(np.mean(zero*zero)))
impulse=np.r_[np.zeros(20),10.,np.zeros(20)]
print('孤立ピーク10の5点平均後:',np.convolve(impulse,np.ones(5)/5,'same').max())
plot(16,t[100:250],{'観測値':x[100:250],'因果フィルタ':causal[100:250],'往復フィルタ':zero[100:250]},'加速度 [m/s²]')
