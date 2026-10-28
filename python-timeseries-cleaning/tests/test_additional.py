import numpy as np
import pandas as pd
import pytest
from tsclean.core import timestamps,interpolate_short
from tsclean.app import process_frame,json_text,validate_config

def settings():return {'version':'test','time':{'column':'t'},'columns':{'x':{'source':'x','window':5}}}

def test_dst_ambiguous_and_nonexistent_are_flagged():
    t=timestamps(['2026-11-01 01:30:00','2026-03-08 02:30:00'],timezone='America/New_York',format='%Y-%m-%d %H:%M:%S')
    assert t.isna().all()

def test_unknown_timezone_rejected():
    c=settings();c['time']['timezone']='Not/A/Zone'
    with pytest.raises(ValueError,match='timezone'):validate_config(c)

def test_short_series_unassessed_not_clear():
    out,f,logs,s=process_frame(pd.DataFrame({'t':['2026-01-01','2026-01-02'],'x':[1,2]}),settings())
    assert s['status']=='REVIEW_REQUIRED' and 'HAMPEL_NOT_ASSESSED' in str(s['warnings'])

def test_strict_json_null():
    import json
    value=json_text({'x':np.nan,'y':np.float64(3),'z':np.inf})
    assert json.loads(value)=={'x':None,'y':3,'z':None}

def test_scaling_overflow_invalid():
    c=settings();c['columns']['x']['scale']=1e308
    out,f,_,_=process_frame(pd.DataFrame({'t':['2026-01-01'],'x':['1e308']}),c)
    assert f.x__invalid_token.iloc[0] and pd.isna(out.x__analysis.iloc[0])

def test_missing_gap_irregular_time_exact_weights():
    t=pd.Series(pd.to_datetime(['2026-01-01T00:00:00Z','2026-01-01T00:00:01Z','2026-01-01T00:00:10Z']))
    y,f=interpolate_short(t,[0,np.nan,10],max_gap_seconds=10)
    assert y.tolist()==[0,1,10] and f.sum()==1

def test_sync_lag_sign_and_clock_model():
    from scipy.signal import correlate,correlation_lags
    a=np.zeros(100);a[[10,60]]=[1,2];b=np.r_[np.zeros(7),a[:-7]]
    lag=correlation_lags(100,100)[np.argmax(correlate(b,a))]
    assert lag==7
    t=np.arange(100)*.1;clock=t*1.0002+.7
    np.testing.assert_allclose((clock-.7)/1.0002,t,atol=1e-12)


def test_comparison_pairs_by_row_not_series_labels():
    from tsclean.core import compare
    result=compare(pd.Series([1.,2.],index=[8,9]),pd.Series([1.,3.],index=[0,1]))
    assert result['paired_n']==2 and result['paired_max_abs_change']==1


def test_csv_blank_records_and_quoted_newline_provenance(tmp_path):
    from tsclean.app import read_input
    p=tmp_path/'a.csv';p.write_text('t,x\n2026-01-01,1\n\n2026-01-03,"bad\ntext"\n',encoding='utf-8')
    frame=read_input(p,settings())['CSV'];assert len(frame)==3
    out,flags,_,_=process_frame(frame,settings(),str(p),'CSV')
    assert out.source_row.tolist()==[2,3,4]
    assert out.source_row_kind.eq('logical_csv_record').all()
    assert flags.x__missing.iloc[1] and flags.x__invalid_token.iloc[2]


def test_duplicate_input_headers_rejected(tmp_path):
    from tsclean.app import read_input
    from openpyxl import Workbook
    csv=tmp_path/'duplicate.csv';csv.write_text('t,x,x\n2026-01-01,1,9\n')
    with pytest.raises(ValueError,match='duplicate column'):read_input(csv,settings())
    xlsx=tmp_path/'duplicate.xlsx';w=Workbook();w.active.append(['t','x','x']);w.active.append(['2026-01-01',1,9]);w.save(xlsx)
    with pytest.raises(ValueError,match='duplicate column'):read_input(xlsx,settings())
