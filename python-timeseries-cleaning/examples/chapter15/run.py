from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('09_prototypes');x=df['測定値'];f=freeze_candidates(x,8)
print('フリーズ候補範囲:',np.flatnonzero(f)[[0,-1]].tolist(),'候補数:',int(f.sum()))
a=pd.read_csv(ROOT/'datasets/raw/prototype_part1.csv');b=pd.read_csv(ROOT/'datasets/raw/prototype_part2.csv')
joined=pd.concat([a.assign(source='part1'),b.assign(source='part2')],ignore_index=True)
print('結合行数:',len(joined),'重複時刻に属する行:',int(joined['時刻'].duplicated(keep=False).sum()))
plot(15,seconds(df),{'観測値':x,'固定値候補':x.where(f)},'温度 [°C]')
