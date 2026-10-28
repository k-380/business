from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

import yaml
from tsclean.app import validate_config,process_frame
c=yaml.safe_load((ROOT/'configs/02_pressure.yaml').read_text(encoding='utf-8'))
validate_config(c);df=load('02_pressure');counts=[]
for k in [2,3,3.5,5,10]:
    c['columns']['value']['k']=k
    _,f,_,_=process_frame(df,c);counts.append(int(f.value__outlier_candidate.sum()))
print('k=2,3,3.5,5,10 の候補数:',counts)
plot(22,[2,3,3.5,5,10],{'候補数':counts},'候補数 [点]',xlabel='Hampelのk [1]')
