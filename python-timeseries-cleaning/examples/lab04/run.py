from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

from scipy.signal import butter,sosfreqz
rng=np.random.default_rng(1304)
reference=np.linspace(0,3,9);z=1.02*reference+.02+rng.normal(0,.004,len(reference))
X=np.column_stack([reference,np.ones(len(reference))]);ab=np.linalg.lstsq(X,z,rcond=None)[0]
res=z-X@ab;cov=(res@res/(len(z)-2))*np.linalg.inv(X.T@X)
measurement=1.55;estimate=(measurement-ab[1])/ab[0]
grad=np.array([-(measurement-ab[1])/ab[0]**2,-1/ab[0]])
u_measure=.005;variance=grad@cov@grad+(u_measure/ab[0])**2
draw=rng.multivariate_normal(ab,cov,size=50000);meas=rng.normal(measurement,u_measure,len(draw));mc=(meas-draw[:,1])/draw[:,0]
print('推定圧力 [MPa]:',estimate,'一次伝播の標準不確かさ:',np.sqrt(variance),'MC標準偏差:',mc.std(ddof=1))
print('MC 2.5/97.5分位:',np.quantile(mc,[.025,.975]).tolist())
assert abs(mc.std(ddof=1)/np.sqrt(variance)-1)<.03
sos=butter(4,180,fs=1000,output='sos');f,h=sosfreqz(sos,worN=2048,fs=1000)
at=np.argmin(np.abs(f-180));print('180Hz付近 一方向/往復 [dB]:',20*np.log10(abs(h[at])),40*np.log10(abs(h[at])))
plot(28,f,{'一方向':20*np.log10(np.maximum(abs(h),1e-8)),'往復':40*np.log10(np.maximum(abs(h),1e-8))},'振幅利得 [dB]',xlabel='周波数 [Hz]',title='補講4図1　ゼロ位相化で振幅応答も変わる')
