from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('04_current');x=df['測定値'];y=x.rolling(21,center=True,min_periods=21).mean()
import json
print(json.dumps(compare(x,y),ensure_ascii=False,indent=2))
print('ピーク保持率:',y.abs().max()/x.abs().max())
plot(19,seconds(df)[:300],{'観測値':x[:300],'21点移動平均':y[:300]},'電流 [A]')
