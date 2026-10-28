"""Teaching extensions, separate from the workbook-oriented CLI."""
import numpy as np
import pandas as pd
from .core import hampel

def chunked_hampel(values,chunk_size=1024,window=11,k=3.5,floor=.01):
    """Overlap half a window; emit only rows owned by the current chunk.
    This array example verifies boundaries, not out-of-core file reading.
    """
    x=np.asarray(values,dtype=float)
    if type(chunk_size) is not int or chunk_size<1:raise ValueError('positive chunk_size')
    half=window//2;pieces=[]
    for start in range(0,len(x),chunk_size):
        end=min(len(x),start+chunk_size);lo=max(0,start-half);hi=min(len(x),end+half)
        h=hampel(x[lo:hi],window,k,floor)
        pieces.append(h.iloc[start-lo:end-lo])
    return pd.concat(pieces,ignore_index=True) if pieces else hampel([],window,k,floor)

def stream_interpolate(records,max_gap_seconds):
    """Input (time,value,segment); output adds was_filled; preserve order.
    Missing values here are all eligible. Caller excludes invalid tokens,
    stopped states and suspect anchors. Unresolved gaps require buffering.
    This is not a constant-memory promise for arbitrarily long missing runs.
    """
    if not np.isfinite(max_gap_seconds) or max_gap_seconds<=0:raise ValueError('positive finite max_gap_seconds')
    previous_time=None;anchor=None;pending=[]
    for t,x,g in records:
        t=pd.Timestamp(t);x=float(x)
        if pd.isna(t) or (previous_time is not None and t<=previous_time):raise ValueError('valid strictly increasing times required')
        previous_time=t
        if np.isinf(x):raise ValueError('infinite observation')
        if np.isnan(x):pending.append((t,x,g));continue
        if pending:
            fill=anchor is not None and (t-anchor[0]).total_seconds()<=max_gap_seconds and all(row[2]==g==anchor[2] for row in pending)
            for tm,missing,gm in pending:
                value=anchor[1]+(x-anchor[1])*(tm-anchor[0]).total_seconds()/(t-anchor[0]).total_seconds() if fill else missing
                yield tm,value,gm,fill
            pending=[]
        yield t,x,g,False
        anchor=(t,x,g)
    for t,x,g in pending:yield t,x,g,False
