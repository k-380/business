from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

rng=np.random.default_rng(802)
a=np.array([0.,30,60,90,120,150]);b=1.0002*a+.7+rng.normal(0,.001,len(a))
train=np.array([0,1,3,5]);hold=np.array([2,4])
X=np.column_stack([a[train],np.ones(len(train))]);beta=np.linalg.lstsq(X,b[train],rcond=None)[0]
res=b[train]-X@beta;s2=res@res/(len(train)-2);cov=s2*np.linalg.inv(X.T@X)
corrected=(b-beta[1])/beta[0];err=corrected-a
print('a,bの推定:',beta.tolist(),'傾き標準誤差:',float(np.sqrt(cov[0,0])))
print('未使用トリガー最大残差 [s]:',float(np.max(np.abs(err[hold]))))
assert np.max(np.abs(err[hold]))<.005
# Grid-only reindex drops actual off-grid anchors. Union preserves them.
t0=pd.Timestamp('2026-01-01',tz='UTC')
observed=pd.Series([0.,2.,5.],index=t0+pd.to_timedelta([0.,1.3,3.2],unit='s'))
grid=pd.date_range(t0,periods=4,freq='s')
union=observed.index.union(grid).sort_values()
aligned=observed.reindex(union).interpolate(method='time',limit_area='inside').reindex(grid)
print('元観測を残すunion補間:',aligned.tolist())
assert np.isclose(aligned.iloc[1],2/1.3)
plot(26,a,{'校正後時刻残差':err},'時刻残差 [s]',xlabel='基準時刻 [s]',title='補講2図1　未使用トリガーも残して検証')
