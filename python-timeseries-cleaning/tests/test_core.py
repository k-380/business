import copy
from pathlib import Path
import tempfile
import numpy as np
import pandas as pd
import pytest
from tsclean.core import numeric,timestamps,time_flags,hampel,freeze_candidates,interpolate_short,compare
from tsclean.app import process_frame,validate_config,excel_safe,read_input,main

def cfg():
    return {'version':'test-1','time':{'column':'time'},'columns':{'x':{'source':'x','floor':.01,'window':5}},'expected_dt':1,'interpolation':{'enabled':False}}

def times(n):return pd.Series(pd.date_range('2026-01-01',periods=n,freq='s',tz='UTC'))

def test_empty_rejected():
    with pytest.raises(ValueError,match='empty'):process_frame(pd.DataFrame(columns=['time','x']),cfg())

def test_all_missing_not_pass():
    _,f,_,s=process_frame(pd.DataFrame({'time':times(20),'x':['']*20}),cfg())
    assert f.x__missing.sum()==20 and 'NO_VALID_VALUES' in str(s['warnings'])
    assert s['status']=='REVIEW_REQUIRED'

def test_duplicate_all_members():
    t=times(4);t.iloc[2]=t.iloc[1]
    assert time_flags(t).time_duplicate.tolist()==[False,True,True,False]

def test_reverse_preserved():
    t=times(4).iloc[[0,2,1,3]].reset_index(drop=True)
    o,f,_,_=process_frame(pd.DataFrame({'time':t,'x':[1,2,3,4]}),cfg())
    assert f.time_reverse.tolist()==[False,False,True,False]
    assert o.x__raw.tolist()==[1,2,3,4]

def test_irregular():
    t=times(4);t.iloc[2:]+=pd.Timedelta(seconds=.2)
    assert time_flags(t,1).interval_irregular.sum()==1

def test_no_outlier_and_edge_unassessed():
    h=hampel(np.ones(11),5)
    assert not h.candidate.any() and h.assessed.sum()==7

def test_extreme_outlier_zero_mad():
    x=np.ones(21);x[10]=1e8
    assert hampel(x,5).candidate.sum()==1

def test_mad_about_one_window_median():
    x=[0,1,2,40,4,5,6]
    h=hampel(x,7,floor=.001)
    assert h.loc[3,'median']==4
    assert h.loc[3,'scale']==pytest.approx(1.482602218505602*2)

def test_numeric_strict_units_locale():
    v,m,b=numeric(['12.5 MPa','oops','---','0','12 Pa'],unit='MPa')
    assert v.iloc[0]==12.5 and v.iloc[3]==0 and m.iloc[2] and b.iloc[1] and b.iloc[4]
    v,_,b=numeric(['1.234,5','1.23,4'],decimal=',',thousands='.')
    assert v.iloc[0]==1234.5 and b.iloc[1]

def test_nonfinite_is_invalid():
    v,m,b=numeric(['inf','-inf','1e999'])
    assert b.all() and v.isna().all() and not m.any()

def test_excel_epoch():
    assert timestamps([61],excel_epoch='1900').iloc[0]==pd.Timestamp('1900-03-01',tz='Asia/Tokyo').tz_convert('UTC')
    assert pd.isna(timestamps([60],excel_epoch='1900').iloc[0])
    assert pd.isna(timestamps([45000]).iloc[0])
    assert timestamps([1],excel_epoch='1904').iloc[0]==pd.Timestamp('1904-01-02',tz='Asia/Tokyo').tz_convert('UTC')

def test_short_gap_elapsed_not_count():
    y,f=interpolate_short(times(5),[0,np.nan,np.nan,3,4],max_gap_seconds=3)
    assert y.tolist()==[0,1,2,3,4] and f.sum()==2

def test_no_partial_long_gap():
    y,f=interpolate_short(times(6),[0,np.nan,np.nan,np.nan,4,5],max_gap_seconds=3)
    assert f.sum()==0 and y.isna().sum()==3

def test_no_extrapolation():
    y,f=interpolate_short(times(4),[np.nan,1,2,np.nan],max_gap_seconds=10)
    assert f.sum()==0 and y.isna().sum()==2

def test_mode_barrier():
    _,f=interpolate_short(times(5),[0,np.nan,np.nan,3,4],max_gap_seconds=4,groups=['run','run','stop','run','run'])
    assert not f.any()

def test_bad_anchor():
    _,f=interpolate_short(times(3),[0,np.nan,2],max_gap_seconds=3,anchors_ok=[False,True,True])
    assert not f.any()

@pytest.mark.parametrize('kind',['duplicate','reverse','invalid'])
def test_bad_time_rejects_interpolation(kind):
    t=times(4)
    if kind=='duplicate':t.iloc[2]=t.iloc[1]
    if kind=='reverse':t.iloc[2]=t.iloc[0]
    if kind=='invalid':t.iloc[2]=pd.NaT
    with pytest.raises(ValueError):interpolate_short(t,[0,np.nan,2,3],max_gap_seconds=5)

def test_length_mismatch():
    with pytest.raises(ValueError):interpolate_short(times(4),[1,2],max_gap_seconds=5)

def test_default_does_not_change_values():
    a=[1,2,'',100,2,2,2,2,2,2,2,2]
    o,_,logs,_=process_frame(pd.DataFrame({'time':times(len(a)),'x':a}),cfg())
    pd.testing.assert_series_equal(o.x__numeric,o.x__analysis,check_names=False)
    assert not logs and o.x__raw.tolist()==a

def test_invalid_token_never_interpolated():
    c=cfg();c['interpolation']={'enabled':True,'max_gap_seconds':3,'reason':'test','approved_by':'test'}
    o,f,logs,_=process_frame(pd.DataFrame({'time':times(5),'x':[1,'broken',3,'',5]}),c)
    assert pd.isna(o.x__analysis.iloc[1]) and o.x__analysis.iloc[3]==4 and len(logs)==1

def test_freeze_whole_run_and_nan():
    f=freeze_candidates([1,2,2,2,2,np.nan,np.nan],4)
    assert f.tolist()==[False,True,True,True,True,False,False]

def test_settings_fail_closed():
    c=cfg();c['interpolation']={'enabled':True,'max_gap_seconds':3}
    with pytest.raises(ValueError):validate_config(c)
    c=cfg();c['silently_remove']=True
    with pytest.raises(ValueError):validate_config(c)

def test_excel_mixed_and_formula_literal(tmp_path):
    from openpyxl import load_workbook
    p=tmp_path/'mixed.xlsx'
    df=pd.DataFrame({'time':times(4).astype(str),'x':['1','故障','=1+1','']})
    excel_safe(df,p)
    assert load_workbook(p)['data']['B4'].data_type=='s'
    f=read_input(p,cfg())['0'];o,flags,_,_=process_frame(f,cfg())
    assert flags.x__invalid_token.sum()==2 and o.x__raw.iloc[2]=='=1+1'

def test_large_chunk_count(tmp_path):
    p=tmp_path/'large.csv';n=250_000
    pd.DataFrame({'id':np.arange(n),'x':np.arange(n)%17}).to_csv(p,index=False)
    total=sum(len(c) for c in pd.read_csv(p,chunksize=8192))
    assert total==n
    c=cfg();c['max_rows']=100
    with pytest.raises(ValueError,match='max_rows'):read_input(p,c)

def test_merge_different_lengths_tolerance():
    a=pd.DataFrame({'t':times(5)})
    b=pd.DataFrame({'tb':times(5).iloc[[0,3]].reset_index(drop=True),'b':[10,20]})
    m=pd.merge_asof(a,b,left_on='t',right_on='tb',direction='backward',tolerance=pd.Timedelta(seconds=1))
    assert len(m)==5 and pd.isna(m.b.iloc[2]) and m.b.iloc[4]==20

def test_resample_alias_suppressed():
    from scipy.signal import resample_poly
    t=np.arange(4000)/1000
    x=np.sin(2*np.pi*370*t)
    filtered=resample_poly(x,1,4)
    assert np.std(filtered[50:-50])<.01
    assert np.std(x[::4])>.6

def test_filter_amplitude_phase():
    from scipy.signal import butter,sosfiltfilt
    t=np.arange(10000)/1000;x=np.sin(2*np.pi*20*t)
    y=sosfiltfilt(butter(4,100,fs=1000,output='sos'),x)
    assert np.max(np.abs(y[1000:-1000]-x[1000:-1000]))<.001

def test_truth_spikes_and_real_pulse():
    root=Path(__file__).resolve().parents[1]
    df=pd.read_csv(root/'datasets/raw/02_pressure.csv')
    import yaml
    c=yaml.safe_load((root/'configs/02_pressure.yaml').read_text())
    o,f,_,_=process_frame(df,c)
    assert f.value__outlier_candidate.iloc[[90,270]].all()
    assert o.value__analysis.iloc[350]>1.8  # real pressure transient remains

def test_cli_outputs_hash_log_and_no_overwrite(tmp_path):
    import yaml,json
    p=tmp_path/'input.csv';pd.DataFrame({'time':times(12).astype(str),'x':range(12)}).to_csv(p,index=False)
    config=tmp_path/'rules.yaml';config.write_text(yaml.safe_dump(cfg()))
    args=['--input',str(p),'--config',str(config),'--output',str(tmp_path/'out')]
    assert main(args)==0
    d=tmp_path/'out/000_00_input'
    assert all((d/x).exists() for x in ['clean_data.xlsx','quality_flags.xlsx','quality_report.html','processing_log.csv','run_manifest.json'])
    assert len(json.loads((d/'run_manifest.json').read_text())['environment']['source_sha256'])==64
    with pytest.raises(ValueError,match='output'):main(args)
