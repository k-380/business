from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HEADER='''from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

'''
LABS={
1:'''from tempfile import TemporaryDirectory
from openpyxl import Workbook
df=pd.read_csv(ROOT/'datasets/raw/locale_cp932.csv',encoding='cp932',sep=';',dtype=str,keep_default_na=False)
v,missing,invalid=numeric(df['測定値'],decimal=',',thousands='.')
assert v.iloc[0]==1234.5
print('CP932 / セミコロン / 小数点カンマ:',v.iloc[0])
with TemporaryDirectory() as folder:
    p=Path(folder)/'two_headers.xlsx';wb=Workbook();ws=wb.active
    ws.append(['模擬：複数行見出し']);ws.append(['時刻','入口','出口']);ws.append(['s','degC','degC'])
    for i in range(10):ws.append([i,20+i*.1,22+i*.1])
    wb.save(p)
    preview=pd.read_excel(p,header=None,keep_default_na=False)
    candidates=[]
    for i,row in preview.iterrows():
        if {'時刻','入口','出口'}.issubset(set(row.astype(str))):candidates.append(i)
    if len(candidates)!=1:raise ValueError('ambiguous/missing header')
    data=pd.read_excel(p,header=[candidates[0],candidates[0]+1])
    data.columns=['_'.join(map(str,c)) for c in data.columns]
    assert data.columns.is_unique and len(data)==10
    print('採用したExcel見出し行:',candidates[0]+1,'列:',data.columns.tolist())
    plot(25,data['時刻_s'],{'入口':data['入口_degC'],'出口':data['出口_degC']},'温度 [°C]',title='補講1図1　複数行見出しを保持した読込')
''',
2:'''rng=np.random.default_rng(802)
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
''',
3:'''from scipy.interpolate import PchipInterpolator,CubicSpline
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
''',
4:'''from scipy.signal import butter,sosfreqz
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
''',
5:'''rng=np.random.default_rng(1705)
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
''',
6:'''from tsclean.streaming import chunked_hampel,stream_interpolate
rng=np.random.default_rng(2106);x=1+.001*rng.normal(size=5000);x[[1023,1024,2048]]=4
whole=hampel(x,11,k=3.5,floor=.01);chunks=chunked_hampel(x,1024,11,3.5,.01)
pd.testing.assert_frame_equal(whole,chunks)
print('全量と重なりチャンクのフラグ・中央値・尺度：全点一致')
t=pd.Series(pd.date_range('2026-01-01',periods=12,freq='s',tz='UTC'))
v=np.arange(12,dtype=float);v[3:7]=np.nan;v[9]=np.nan
records=((tm,value,0) for tm,value in zip(t,v))
rows=list(stream_interpolate(records,3));ys=np.array([row[1] for row in rows]);filled=np.array([row[3] for row in rows])
batch,mask=interpolate_short(t,v,max_gap_seconds=3)
np.testing.assert_allclose(ys,batch,equal_nan=True);assert filled.sum()==1
print('境界をまたぐ4点欠損は全体として残し、1点欠損だけ補間。')
plot(30,np.arange(len(v)),{'観測':v,'ストリーム補間':ys},'値 [1]',xlabel='記録番号',title='補講6図1　未完了の欠損区間を保留する')
'''
}
if __name__=='__main__':
    for n,body in LABS.items():
        folder=ROOT/'examples'/f'lab{n:02d}';folder.mkdir(exist_ok=True)
        (folder/'run.py').write_text(HEADER+body,encoding='utf-8')
