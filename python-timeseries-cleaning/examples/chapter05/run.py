from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

df=load('08_restart');t=pd.to_datetime(df['時刻'],utc=True,format='ISO8601')
flags=time_flags(t,1)
print(flags[['time_duplicate','time_reverse','time_invalid']].sum().to_string())
print('逆転位置:',np.flatnonzero(flags.time_reverse).tolist())
plot(5,df['sequence'],{'記録時計':seconds(df),'取得順序からの経過':df['sequence']},'時刻 [s]',xlabel='取得順序')
