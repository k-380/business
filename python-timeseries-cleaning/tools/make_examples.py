"""Materialize complete chapter programs from reviewed source strings."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CODE={
1:'''df=load('02_pressure')
before=df.copy(deep=True)
raw=df['測定値']
candidate=raw.gt(2.5)|raw.lt(0)
view=df.assign(candidate=candidate)
assert df.equals(before)
print('原本行数:',len(df),'範囲外候補:',int(candidate.sum()))
print(view.loc[candidate].to_string(index=False))
plot(1,seconds(df),{'観測値':raw,'確認対象':raw.where(candidate)},'圧力 [MPa]')
''',
2:'''from openpyxl import load_workbook
p=ROOT/'datasets/raw/10_irregular_excel.xlsx'
wb=load_workbook(p,data_only=False)
print('シート:',wb.sheetnames,'結合:',list(wb['測定'].merged_cells.ranges),'基準日:',wb.epoch)
preview=pd.read_excel(p,sheet_name='測定',header=None,nrows=6)
print(preview.to_string(index=False,header=False))
df=pd.read_excel(p,sheet_name='測定',header=3,keep_default_na=False)
x,missing,bad=numeric(df['測定値'],unit='degC')
print('読み込み行数:',len(df),'完全空白行:',int(df.eq('').all(axis=1).sum()),'変換不能:',int(bad.sum()))
plot(2,np.arange(len(df))+5,{'数値化可能な値':x},'温度 [°C]',xlabel='Excelの行番号')
''',
3:'''values=['１,２３４.５ degC','---','故障','0','25.0 degC']
v,missing,invalid=numeric(values,unit='degC',thousands=',')
print(pd.DataFrame({'raw':values,'numeric':v,'missing':missing,'invalid':invalid}).to_string(index=False))
print('シリアル61（UTCとして解釈）:',timestamps([61],excel_epoch='1900',timezone='UTC').iloc[0])
print('20 °C =',20+273.15,'K')
plot(3,np.arange(len(v)),{'数値化した温度':v},'温度 [°C]',xlabel='記録番号')
''',
4:'''df=load('01_temperature');x=pd.to_numeric(df['測定値'],errors='coerce')
n=len(x);missing=x.isna().sum()
print(f'行数={n}, 欠損={missing}, 欠損率={missing/n:.6f}, 完全性={1-missing/n:.6f}')
hours=(seconds(df)//3600).astype(int)
rate=x.isna().groupby(hours).mean()
plot(4,rate.index,{'時間帯別欠損率':rate},'欠損率 [1]',xlabel='開始後 [h]')
''',
5:'''df=load('08_restart');t=pd.to_datetime(df['時刻'],utc=True,format='ISO8601')
flags=time_flags(t,1)
print(flags[['time_duplicate','time_reverse','time_invalid']].sum().to_string())
print('逆転位置:',np.flatnonzero(flags.time_reverse).tolist())
plot(5,df['sequence'],{'記録時計':seconds(df),'取得順序からの経過':df['sequence']},'時刻 [s]',xlabel='取得順序')
''',
6:'''rng=np.random.default_rng(6)
nominal=.01
t=np.arange(1000)*nominal+rng.normal(0,.0001,1000)
t=np.delete(t,[200,201,600]);dt=np.diff(t)
estimated=np.maximum(np.rint(dt/nominal).astype(int)-1,0)
print('周期中央値 [s]:',round(float(np.median(dt)),6),'推定欠落数:',int(estimated.sum()))
print('設定fs [Hz]:',1/nominal,'Nyquist [Hz]:',1/(2*nominal))
hist,bins=np.histogram(dt,bins=30)
plot(6,(bins[:-1]+bins[1:])/2,{'間隔の件数':hist},'件数 [個]',xlabel='記録間隔 [s]')
''',
7:'''from scipy.signal import resample_poly
df=load('03_vibration');x=df['測定値'].to_numpy()
y=resample_poly(x,1,4);naive=x[::4]
f=np.fft.rfftfreq(len(y),d=.004)
amp=lambda z:2*np.abs(np.fft.rfft(z))/len(z)
print('入力/出力行数:',len(x),len(y),'出力fs:',250)
print('130 Hz成分は新Nyquist 125 Hzを超えるため保存できない。')
plot(7,f,{'単純間引き':amp(naive),'低域通過後に間引き':amp(y)},'片側振幅 [m/s²]',xlabel='周波数 [Hz]')
''',
8:'''from scipy.signal import correlate,correlation_lags
df=load('05_sync');a=df.reference_trigger.to_numpy();b=np.r_[np.zeros(7),a[:-7]]
c=correlate(b-b.mean(),a-a.mean(),mode='full');lags=correlation_lags(len(b),len(a))
lag=int(lags[np.argmax(c)]);print('Bの遅れ [sample]:',lag,'遅れ [s]:',lag*.1)
recorded=seconds(df)+.7;corrected=(recorded-.7)/1.0002
print('トリガー校正式の最大残差 [s]:',np.max(np.abs(corrected-df.reference_time_s)))
plot(8,df.reference_time_s,{'補正前時刻誤差':recorded-df.reference_time_s,'補正後時刻誤差':corrected-df.reference_time_s},'同期誤差 [s]')
''',
9:'''df=load('01_temperature');missing=df['測定値'].isna()
group=missing.ne(missing.shift()).cumsum()
runs=[len(g) for _,g in missing.groupby(group) if g.iloc[0]]
print('連続欠損の長さ:',runs,'最長 [記録]:',max(runs))
print('欠損原因は値だけでは確定しない。manifestは模擬データの出題情報。')
plot(9,seconds(df)/3600,{'欠損=1':missing.astype(int)},'欠損フラグ [0/1]',xlabel='経過時間 [h]')
''',
10:'''df=load('07_modes');t=pd.to_datetime(df['時刻'],utc=True,format='ISO8601');x=df['測定値']
segments=df['mode'].ne(df['mode'].shift()).cumsum()
y,filled=interpolate_short(t,x,max_gap_seconds=30,groups=segments,eligible=df['mode'].eq('run'))
target=truth('07_modes').latent_signal
print('補間数:',int(filled.sum()),'残欠損:',int(y.isna().sum()))
print('模擬真値に対する補間点RMSE:',float(np.sqrt(np.mean((y[filled]-target[filled])**2))))
plot(10,seconds(df),{'観測値':x,'条件付き補間':y,'補間点':y.where(filled)},'温度 [°C]')
''',
11:'''df=load('02_pressure');x=df['測定値'];h=hampel(x,11,k=3.5,floor=.01)
z=(x-x.mean())/x.std(ddof=1)
q1,q3=x.quantile([.25,.75]);iqr=q3-q1
print('Z>3:',int(z.abs().gt(3).sum()),'IQR候補:',int(((x<q1-1.5*iqr)|(x>q3+1.5*iqr)).sum()),'Hampel候補:',int(h.candidate.sum()))
print('MAD未評価:',int((~h.assessed).sum()))
plot(11,seconds(df),{'観測値':x,'局所候補':x.where(h.candidate)},'圧力 [MPa]')
''',
12:'''from scipy.ndimage import median_filter
df=load('02_pressure');x=df['測定値'];proposal=pd.Series(median_filter(x,size=5,mode='reflect'))
# この模擬問題ではmanifestで測定不具合と判明した2点だけを承認した。
approved=pd.Series(False,index=x.index);approved.iloc[[90,270]]=True
y=x.where(~approved,proposal)
print('承認修正数:',int(approved.sum()),'実現象のピーク保持:',bool(y.iloc[350]==x.iloc[350]))
plot(12,seconds(df),{'観測値':x,'承認した2点のみ修正':y},'圧力 [MPa]')
''',
13:'''df=load('06_durability');h=seconds(df)/3600;x=df['測定値'];ref=df.reference
drift=x-ref
# 既知の定期校正点を模した100時間間隔の差分。製品の傾きは除去しない。
anchors=np.arange(0,len(x),100);estimate=np.interp(h,h[anchors],drift.iloc[anchors]);y=x-estimate
print('原観測の傾き:',np.polyfit(h,x,1)[0],'補正後:',np.polyfit(h,y,1)[0],'真の劣化傾き:0.0006 mm/s/h')
print('終端の校正点外は外挿相当の保持となるため別途確認が必要。')
plot(13,h,{'観測値':x,'基準計測':ref,'校正差による補正':y},'振動速度RMS [mm/s]',xlabel='運転時間 [h]')
''',
14:'''df=load('04_current');x=df['測定値'];y=truth('04_current').latent_signal
sat=x.abs().ge(12)
q=24/4096
print('飽和候補数:',int(sat.sum()),'12bit量子化幅 [A]:',q,'一様誤差モデルu [A]:',q/np.sqrt(12))
print('記録ピーク:',x.abs().max(),'模擬真値ピーク:',y.abs().max())
plot(14,seconds(df)[:300],{'クリップした観測':x[:300],'模擬真値':y[:300]},'電流 [A]')
''',
15:'''df=load('09_prototypes');x=df['測定値'];f=freeze_candidates(x,8)
print('フリーズ候補範囲:',np.flatnonzero(f)[[0,-1]].tolist(),'候補数:',int(f.sum()))
a=pd.read_csv(ROOT/'datasets/raw/prototype_part1.csv');b=pd.read_csv(ROOT/'datasets/raw/prototype_part2.csv')
joined=pd.concat([a.assign(source='part1'),b.assign(source='part2')],ignore_index=True)
print('結合行数:',len(joined),'重複時刻に属する行:',int(joined['時刻'].duplicated(keep=False).sum()))
plot(15,seconds(df),{'観測値':x,'固定値候補':x.where(f)},'温度 [°C]')
''',
16:'''from scipy.signal import butter,sosfilt,sosfiltfilt
df=load('03_vibration');x=df['測定値'].to_numpy();t=seconds(df)
sos=butter(4,180,fs=1000,output='sos')
causal=sosfilt(sos,x);zero=sosfiltfilt(sos,x)
print('原波形RMS:',np.sqrt(np.mean(x*x)),'ゼロ位相後RMS:',np.sqrt(np.mean(zero*zero)))
impulse=np.r_[np.zeros(20),10.,np.zeros(20)]
print('孤立ピーク10の5点平均後:',np.convolve(impulse,np.ones(5)/5,'same').max())
plot(16,t[100:250],{'観測値':x[100:250],'因果フィルタ':causal[100:250],'往復フィルタ':zero[100:250]},'加速度 [m/s²]')
''',
17:'''df=load('09_prototypes');a=pd.DataFrame({'t':pd.to_datetime(df['時刻'],utc=True,format='ISO8601'),'a':df['測定値']})
b=pd.DataFrame({'tb':a.t[::2]+pd.Timedelta(milliseconds=200),'b':df.prototype_B[::2]})
m=pd.merge_asof(a,b,left_on='t',right_on='tb',direction='nearest',tolerance=pd.Timedelta(milliseconds=400))
print('左行数保持:',len(m)==len(a),'未対応:',int(m.b.isna().sum()))
print('最大対応時刻差 [s]:',float((m.t-m.tb).dt.total_seconds().abs().max()))
plot(17,seconds(df),{'試作品A':m.a,'試作品B（対応点のみ）':m.b},'温度 [°C]')
''',
18:'''df=load('07_modes');segment=df['mode'].ne(df['mode'].shift()).cumsum()
print(df.assign(segment=segment).groupby(['segment','mode'])['測定値'].agg(['count','mean','max']).to_string())
dt=10;rate=df['測定値'].diff()/dt
steady=rate.abs().rolling(12,min_periods=12).max().lt(.03)&df['mode'].eq('run')
print('演習基準の定常候補点数:',int(steady.sum()))
plot(18,seconds(df),{'温度':df['測定値'],'定常候補':df['測定値'].where(steady)},'温度 [°C]')
''',
19:'''df=load('04_current');x=df['測定値'];y=x.rolling(21,center=True,min_periods=21).mean()
import json
print(json.dumps(compare(x,y),ensure_ascii=False,indent=2))
print('ピーク保持率:',y.abs().max()/x.abs().max())
plot(19,seconds(df)[:300],{'観測値':x[:300],'21点移動平均':y[:300]},'電流 [A]')
''',
20:'''from tsclean.app import sha256
import json
p=ROOT/'datasets/raw/02_pressure.csv'
print('原本SHA-256:',sha256(p))
df=load('02_pressure');x=df['測定値'];candidate=hampel(x).candidate
ledger=pd.DataFrame({'source_row':np.arange(len(x))+2,'raw':x,'analysis':x,'candidate':candidate,'modified':False})
print(ledger[candidate].head().to_string(index=False))
assert ledger.raw.equals(ledger.analysis)
plot(20,seconds(df),{'観測値（改変なし）':x,'候補フラグ':x.where(candidate)},'圧力 [MPa]')
''',
21:'''from tempfile import TemporaryDirectory
with TemporaryDirectory() as folder:
    p=Path(folder)/'large.csv';n=250000
    pd.DataFrame({'id':np.arange(n),'value':np.arange(n)%100}).to_csv(p,index=False)
    count=0;total=0.;sizes=[]
    for chunk in pd.read_csv(p,chunksize=8192):
        count+=len(chunk);total+=chunk.value.sum();sizes.append(len(chunk))
    print('処理件数:',count,'平均:',total/count,'チャンク数:',len(sizes))
    assert count==n and total/count==49.5
plot(21,np.arange(len(sizes)),{'チャンク行数':sizes},'行数 [行]',xlabel='チャンク番号')
''',
22:'''import yaml
from tsclean.app import validate_config,process_frame
c=yaml.safe_load((ROOT/'configs/02_pressure.yaml').read_text(encoding='utf-8'))
validate_config(c);df=load('02_pressure');counts=[]
for k in [2,3,3.5,5,10]:
    c['columns']['value']['k']=k
    _,f,_,_=process_frame(df,c);counts.append(int(f.value__outlier_candidate.sum()))
print('k=2,3,3.5,5,10 の候補数:',counts)
plot(22,[2,3,3.5,5,10],{'候補数':counts},'候補数 [点]',xlabel='Hampelのk [1]')
''',
23:'''import yaml,json
from tsclean.app import process_frame
c=yaml.safe_load((ROOT/'configs/01_temperature.yaml').read_text(encoding='utf-8'))
df=load('01_temperature');out,flags,logs,summary=process_frame(df,c)
print(json.dumps(summary,ensure_ascii=False,indent=2,default=str))
counts=summary['flag_counts'];names=list(counts);v=list(counts.values())
plot(23,np.arange(len(v)),{'フラグ件数':v},'件数 [点]',xlabel='フラグ番号（標準出力の順）')
''',
24:'''from tempfile import TemporaryDirectory
from tsclean.app import main
with TemporaryDirectory() as folder:
    code=main(['--input',str(ROOT/'datasets/raw/02_pressure.csv'),'--config',str(ROOT/'configs/02_pressure.yaml'),'--output',str(Path(folder)/'result')])
    assert code==0
    p=Path(folder)/'result/000_00_02_pressure/clean_data.xlsx'
    df=pd.read_excel(p)
    assert df.value__numeric.equals(df.value__analysis)
    print('Excel再読込:',len(df),'行。初期設定で値の変更なし。')
    plot(24,np.arange(len(df)),{'数値化した元データ':df.value__numeric,'解析用データ':df.value__analysis},'圧力 [MPa]',xlabel='取得順序')
'''
}

HEADER='''from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

'''
if __name__=='__main__':
    for n,code in CODE.items():
        d=ROOT/'examples'/f'chapter{n:02d}';d.mkdir(exist_ok=True)
        (d/'run.py').write_text(HEADER+code,encoding='utf-8')
