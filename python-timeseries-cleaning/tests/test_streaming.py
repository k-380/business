import numpy as np
import pandas as pd
import pytest
from tsclean.core import hampel
from tsclean.streaming import chunked_hampel,stream_interpolate

@pytest.mark.parametrize('chunk_size',[1,3,17,100])
def test_overlap_exact_with_missing_and_boundary_outliers(chunk_size):
    x=np.sin(np.arange(100)*.03);x[[16,17,34]]=20;x[70:72]=np.nan
    pd.testing.assert_frame_equal(chunked_hampel(x,chunk_size,11),hampel(x,11))

def records(x,g=None,t=None):
    times=pd.date_range('2026-01-01',periods=len(x),freq='s') if t is None else t
    return zip(times,x,g if g is not None else [0]*len(x))

def test_no_edge_extrapolation_or_partial_long_gap():
    out=list(stream_interpolate(records([np.nan,0,np.nan,np.nan,np.nan,4,np.nan,6,np.nan]),3))
    assert [r[3] for r in out]==[False]*6+[True,False,False]
    assert out[6][1]==5 and np.isnan(out[0][1]) and np.isnan(out[-1][1])

def test_mode_boundaries_prevent_bridge_including_return():
    out=list(stream_interpolate(records([0,np.nan,2],[0,1,0]),3))
    assert np.isnan(out[1][1]) and not out[1][3]

@pytest.mark.parametrize('offsets',[[0,0],[1,0]])
def test_invalid_order_rejected(offsets):
    t=pd.Timestamp('2026-01-01')+pd.to_timedelta(offsets,unit='s')
    with pytest.raises(ValueError):list(stream_interpolate(records([0,1],t=t),3))

def test_empty_and_invalid_limits():
    assert list(stream_interpolate([],1))==[]
    pd.testing.assert_frame_equal(chunked_hampel([]),hampel([]))
    for limit in [0,-1,np.nan,np.inf]:
        with pytest.raises(ValueError):list(stream_interpolate([],limit))

def test_irregular_weights_and_missing_value_identity():
    t=pd.Timestamp('2026-01-01')+pd.to_timedelta([0,1,10],unit='s')
    out=list(stream_interpolate(records([0,np.nan,10],t=t),10))
    assert out[1][1]==1 and out[1][3]
