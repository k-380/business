from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from tsclean.app import sha256
import json
p=ROOT/'datasets/raw/02_pressure.csv'
print('原本SHA-256:',sha256(p))
df=load('02_pressure');x=df['測定値'];candidate=hampel(x).candidate
ledger=pd.DataFrame({'source_row':np.arange(len(x))+2,'raw':x,'analysis':x,'candidate':candidate,'modified':False})
print(ledger[candidate].head().to_string(index=False))
assert ledger.raw.equals(ledger.analysis)
plot(20,seconds(df),{'観測値（改変なし）':x,'候補フラグ':x.where(candidate)},'圧力 [MPa]')
