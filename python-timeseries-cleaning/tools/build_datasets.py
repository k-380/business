from pathlib import Path
import json,sys
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tsclean.app import process_frame,read_input,json_text

def main():
    manifest=json.loads((ROOT/'datasets/manifest.json').read_text())
    (ROOT/'datasets/cleaners').mkdir(exist_ok=True)
    summary={}
    for d in manifest['datasets']:
        name=d['id'];c=yaml.safe_load((ROOT/'configs'/f'{name}.yaml').read_text())
        df=read_input(ROOT/'datasets/raw'/f'{name}.csv',c)['CSV']
        out,flags,logs,s=process_frame(df,c,f'datasets/raw/{name}.csv','CSV')
        assert len(out)==d['n']
        pd.testing.assert_series_equal(out.value__numeric,out.value__analysis,check_names=False)
        out.to_csv(ROOT/'datasets/expected'/f'{name}_inspection.csv',index=False,encoding='utf-8-sig')
        flags.to_csv(ROOT/'datasets/expected'/f'{name}_flags.csv',index=False,encoding='utf-8-sig')
        summary[name]=s
        script=f'''from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tsclean.app import main
if __name__=='__main__':
    output=sys.argv[1] if len(sys.argv)>1 else str(ROOT/'results/{name}')
    raise SystemExit(main(['--input',str(ROOT/'datasets/raw/{name}.csv'),'--config',str(ROOT/'configs/{name}.yaml'),'--output',output]))
'''
        (ROOT/'datasets/cleaners'/f'{name}.py').write_text(script,encoding='utf-8')
    # Independent invariants supplement implementation-generated expected snapshots.
    assert summary['01_temperature']['flag_counts']['value__missing']==33
    assert summary['02_pressure']['flag_counts']['value__bounds_candidate']==2
    assert summary['04_current']['flag_counts']['value__saturation_candidate']==35
    assert summary['07_modes']['flag_counts']['value__missing']==92
    assert summary['08_restart']['flag_counts']['time_reverse']==1
    assert summary['09_prototypes']['flag_counts']['value__freeze_candidate']==21
    (ROOT/'datasets/expected/inspection_summary.json').write_text(json_text(summary),encoding='utf-8')
    c=yaml.safe_load((ROOT/'configs/07_modes.yaml').read_text())
    c['interpolation']={'enabled':True,'max_gap_seconds':30,'reason':'演習用の承認規則：同一run区間の短い空欄','approved_by':'教材検証'}
    (ROOT/'configs/07_modes_interpolate.yaml').write_text(yaml.safe_dump(c,allow_unicode=True,sort_keys=False),encoding='utf-8')
    out,f,logs,s=process_frame(read_input(ROOT/'datasets/raw/07_modes.csv',c)['CSV'],c)
    assert f.value__interpolated.sum()==2 and out.value__analysis.isna().sum()==90
    out.to_csv(ROOT/'datasets/expected/07_modes_interpolated.csv',index=False,encoding='utf-8-sig')
    print('10 default outputs + approved interpolation output verified.')
if __name__=='__main__':main()
