from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('02_pressure')
before=df.copy(deep=True)
raw=df['測定値']
candidate=raw.gt(2.5)|raw.lt(0)
view=df.assign(candidate=candidate)
assert df.equals(before)
print('原本行数:',len(df),'範囲外候補:',int(candidate.sum()))
print(view.loc[candidate].to_string(index=False))
plot(1,seconds(df),{'観測値':raw,'確認対象':raw.where(candidate)},'圧力 [MPa]')
