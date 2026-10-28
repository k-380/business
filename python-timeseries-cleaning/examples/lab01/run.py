from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'examples'))
import numpy as np
import pandas as pd
from common import load,truth,seconds,plot
from tsclean.core import numeric,hampel,interpolate_short

from tempfile import TemporaryDirectory
from openpyxl import Workbook
df=pd.read_csv(ROOT/'datasets/raw/locale_cp932.csv',encoding='cp932',sep=';',dtype=str,keep_default_na=False)
v,missing,invalid=numeric(df['測定値'],decimal=',',thousands='.')
assert v.iloc[0]==1234.5
print('CP932 / セミコロン / 小数点カンマ:',v.iloc[0])
with TemporaryDirectory() as folder:
    p=Path(folder)/'two_headers.xlsx';wb=Workbook();ws=wb.active
    ws.append(['模擬：複数行見出し']);ws.append(['時刻','入口','出口']);ws.append(['s','degC','degC'])
    for i in range(10):ws.append([i,20+i*.1,22+i*.1])
    wb.save(p)
    preview=pd.read_excel(p,header=None,keep_default_na=False)
    candidates=[]
    for i,row in preview.iterrows():
        if {'時刻','入口','出口'}.issubset(set(row.astype(str))):candidates.append(i)
    if len(candidates)!=1:raise ValueError('ambiguous/missing header')
    data=pd.read_excel(p,header=[candidates[0],candidates[0]+1])
    data.columns=['_'.join(map(str,c)) for c in data.columns]
    assert data.columns.is_unique and len(data)==10
    print('採用したExcel見出し行:',candidates[0]+1,'列:',data.columns.tolist())
    plot(25,data['時刻_s'],{'入口':data['入口_degC'],'出口':data['出口_degC']},'温度 [°C]',title='補講1図1　複数行見出しを保持した読込')
