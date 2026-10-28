from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

from scipy.interpolate import PchipInterpolator,CubicSpline
df=load('07_modes');t=seconds(df);x=df['測定値'].to_numpy();target=truth('07_modes').latent_signal.to_numpy()
valid=np.isfinite(x);mask=np.zeros(len(x),bool);mask[60:70]=True;mask[350:360]=True
train=valid & ~mask;known_t=t[train];known_x=x[train]
linear=np.interp(t,known_t,known_x)
ffill=pd.Series(x).mask(mask).ffill().to_numpy()
pchip=PchipInterpolator(known_t,known_x,extrapolate=False)(t)
cubic=CubicSpline(known_t,known_x,extrapolate=False)(t)
poly=np.full(len(x),np.nan)
for lo,hi in [(60,70),(350,360)]:
    idx=np.r_[np.arange(lo-5,lo),np.arange(hi,hi+5)]
    origin=t[lo];coef=np.polyfit((t[idx]-origin)/100,x[idx],3)
    poly[lo:hi]=np.polyval(coef,(t[lo:hi]-origin)/100)
for name,y in [('ffill',ffill),('linear',linear),('pchip',pchip),('cubic_spline',cubic),('local_cubic_polynomial',poly)]:
    err=y[mask]-target[mask]
    print(name,'RMSE [degC]=',round(float(np.sqrt(np.mean(err**2))),6),'max abs=',round(float(np.max(np.abs(err))),6))
print('この比較はrun区間の人工欠損のみ。停止中を橋渡しする推定は採用しない。')
plot(27,t[50:80],{'模擬真値':target[50:80],'線形':linear[50:80],'PCHIP':pchip[50:80],'前方補完':ffill[50:80]},'温度 [°C]',title='補講3図1　連続欠損を隠して補間を評価')
