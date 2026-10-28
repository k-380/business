from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

rng=np.random.default_rng(1705)
n=800;t=np.arange(n,dtype=float);common=rng.normal(size=n)
a=10+common+rng.normal(0,.03,n);b=20+2*common+rng.normal(0,.04,n)
b[600:610]+=1.0
data=np.column_stack([a,b]);train=data[:400];mu=train.mean(axis=0);cov=np.cov(train,rowvar=False)
inverse=np.linalg.inv(cov);delta=data-mu
d2=np.einsum('ij,jk,ik->i',delta,inverse,delta)
train_d2=d2[:400];threshold=np.quantile(train_d2,.99)
flag=d2>threshold
print('学習内99%分位（普遍閾値ではない）:',threshold)
print('注入区間検出:',int(flag[600:610].sum()),'/10','それ以外の検証区間候補:',int(flag[400:600].sum()+flag[610:].sum()))
print('2列の相関:',np.corrcoef(train,rowvar=False)[0,1],'共分散の条件数:',np.linalg.cond(cov))
assert flag[600:610].all()
folder=ROOT/'datasets/supplementary';folder.mkdir(exist_ok=True)
pd.DataFrame({'t_s':t,'a':a,'b':b,'injected_relation_error':(t>=600)&(t<610),'seed':1705}).to_csv(folder/'multivariate.csv',index=False)
plot(29,t,{'距離二乗':d2,'学習内99%分位':np.full(n,threshold)},'Mahalanobis距離二乗 [1]',xlabel='測定記録番号',title='補講5図1　二系列の関係を検査')
