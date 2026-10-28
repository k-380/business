from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('06_durability');h=seconds(df)/3600;x=df['測定値'];ref=df.reference
drift=x-ref
# 既知の定期校正点を模した100時間間隔の差分。製品の傾きは除去しない。
anchors=np.arange(0,len(x),100);estimate=np.interp(h,h[anchors],drift.iloc[anchors]);y=x-estimate
print('原観測の傾き:',np.polyfit(h,x,1)[0],'補正後:',np.polyfit(h,y,1)[0],'真の劣化傾き:0.0006 mm/s/h')
print('終端の校正点外は外挿相当の保持となるため別途確認が必要。')
plot(13,h,{'観測値':x,'基準計測':ref,'校正差による補正':y},'振動速度RMS [mm/s]',xlabel='運転時間 [h]')
