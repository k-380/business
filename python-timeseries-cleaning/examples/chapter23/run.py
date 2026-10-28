from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

import yaml,json
from tsclean.app import process_frame
c=yaml.safe_load((ROOT/'configs/01_temperature.yaml').read_text(encoding='utf-8'))
df=load('01_temperature');out,flags,logs,summary=process_frame(df,c)
print(json.dumps(summary,ensure_ascii=False,indent=2,default=str))
counts=summary['flag_counts'];names=list(counts);v=list(counts.values())
plot(23,np.arange(len(v)),{'フラグ件数':v},'件数 [点]',xlabel='フラグ番号（標準出力の順）')
