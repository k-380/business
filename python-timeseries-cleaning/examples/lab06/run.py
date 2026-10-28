from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

from tsclean.streaming import chunked_hampel,stream_interpolate
rng=np.random.default_rng(2106);x=1+.001*rng.normal(size=5000);x[[1023,1024,2048]]=4
whole=hampel(x,11,k=3.5,floor=.01);chunks=chunked_hampel(x,1024,11,3.5,.01)
pd.testing.assert_frame_equal(whole,chunks)
print('全量と重なりチャンクのフラグ・中央値・尺度：全点一致')
t=pd.Series(pd.date_range('2026-01-01',periods=12,freq='s',tz='UTC'))
v=np.arange(12,dtype=float);v[3:7]=np.nan;v[9]=np.nan
records=((tm,value,0) for tm,value in zip(t,v))
rows=list(stream_interpolate(records,3));ys=np.array([row[1] for row in rows]);filled=np.array([row[3] for row in rows])
batch,mask=interpolate_short(t,v,max_gap_seconds=3)
np.testing.assert_allclose(ys,batch,equal_nan=True);assert filled.sum()==1
print('境界をまたぐ4点欠損は全体として残し、1点欠損だけ補間。')
plot(30,np.arange(len(v)),{'観測':v,'ストリーム補間':ys},'値 [1]',xlabel='記録番号',title='補講6図1　未完了の欠損区間を保留する')
