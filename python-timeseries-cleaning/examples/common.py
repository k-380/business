"""Shared plotting and fixture access; read alongside each chapter's run.py."""
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, font_manager
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.find_spec('japanize_matplotlib')
if spec:
    font=Path(spec.origin).parent/'fonts/ipaexg.ttf'
    font_manager.fontManager.addfont(str(font))
    plt.rcParams['font.family']='IPAexGothic'
plt.rcParams.update({'svg.fonttype':'path','axes.unicode_minus':False,'font.size':11})

def load(name):return pd.read_csv(ROOT/'datasets/raw'/f'{name}.csv')
def truth(name):return pd.read_csv(ROOT/'datasets/expected'/f'{name}_truth.csv')
def seconds(df):
    t=pd.to_datetime(df['時刻'],utc=True,format='ISO8601')
    return (t-t.iloc[0]).dt.total_seconds().to_numpy()
def plot(ch,x,series,ylabel,xlabel='経過時間 [s]',title=None):
    fig,ax=plt.subplots(figsize=(9,4))
    styles=['-','--',':','-.'];markers=[None,None,'x','o']
    for i,(label,y) in enumerate(series.items()):
        ax.plot(x,y,linestyle=styles[i%4],marker=markers[i%4],markevery=max(1,len(x)//30),label=label,lw=1.35)
    ax.set(xlabel=xlabel,ylabel=ylabel,title=title or f'図{ch}-1　処理結果の比較');ax.grid(alpha=.2);ax.legend();fig.tight_layout()
    dest=ROOT/'assets/images'/f'chapter{ch:02d}.svg'
    temporary=dest.with_suffix('.svg.tmp')
    fig.savefig(temporary,format='svg',metadata={'Date':None});plt.close(fig)
    temporary.replace(dest)
    return dest
