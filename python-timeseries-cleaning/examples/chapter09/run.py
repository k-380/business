from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('01_temperature');missing=df['測定値'].isna()
group=missing.ne(missing.shift()).cumsum()
runs=[len(g) for _,g in missing.groupby(group) if g.iloc[0]]
print('連続欠損の長さ:',runs,'最長 [記録]:',max(runs))
print('欠損原因は値だけでは確定しない。manifestは模擬データの出題情報。')
plot(9,seconds(df)/3600,{'欠損=1':missing.astype(int)},'欠損フラグ [0/1]',xlabel='経過時間 [h]')
