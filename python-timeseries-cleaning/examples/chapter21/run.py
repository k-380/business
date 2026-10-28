from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

from tempfile import TemporaryDirectory
with TemporaryDirectory() as folder:
    p=Path(folder)/'large.csv';n=250000
    pd.DataFrame({'id':np.arange(n),'value':np.arange(n)%100}).to_csv(p,index=False)
    count=0;total=0.;sizes=[]
    for chunk in pd.read_csv(p,chunksize=8192):
        count+=len(chunk);total+=chunk.value.sum();sizes.append(len(chunk))
    print('処理件数:',count,'平均:',total/count,'チャンク数:',len(sizes))
    assert count==n and total/count==49.5
plot(21,np.arange(len(sizes)),{'チャンク行数':sizes},'行数 [行]',xlabel='チャンク番号')
