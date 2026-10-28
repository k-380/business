from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare

values=['１,２３４.５ degC','---','故障','0','25.0 degC']
v,missing,invalid=numeric(values,unit='degC',thousands=',')
print(pd.DataFrame({'raw':values,'numeric':v,'missing':missing,'invalid':invalid}).to_string(index=False))
print('シリアル61（UTCとして解釈）:',timestamps([61],excel_epoch='1900',timezone='UTC').iloc[0])
print('20 °C =',20+273.15,'K')
plot(3,np.arange(len(v)),{'数値化した温度':v},'温度 [°C]',xlabel='記録番号')
