"""Small, inspectable algorithms used by the book and CLI.

All thresholds are teaching settings. A flag is not a diagnosis.
Time checks always precede sorting; no function deletes observations.
"""
from __future__ import annotations
import re
import unicodedata
import numpy as np
import pandas as pd


def numeric(values, *, unit='', decimal='.', thousands='', missing=('', 'NA', '---', '欠測')):
    """Parse an explicitly declared format; unknown units stay invalid."""
    s = pd.Series(values, copy=True).reset_index(drop=True)
    text = s.map(lambda v: '' if pd.isna(v) else unicodedata.normalize('NFKC', str(v)).strip())
    absent = text.isin([unicodedata.normalize('NFKC', str(x)) for x in missing]) | s.isna()
    if unit:
        u = unicodedata.normalize('NFKC', unit)
        text = text.str.replace(r'\s*' + re.escape(u) + r'\s*$', '', regex=True)
    if thousands:
        # Reject malformed grouping rather than turning 1,23 into 123.
        sep, dec = re.escape(thousands), re.escape(decimal)
        grouped = text.str.contains(thousands, regex=False)
        good = text.str.fullmatch(r'[+-]?\d{1,3}(?:' + sep + r'\d{3})+(?:' + dec + r'\d+)?')
        text = text.mask(grouped & ~good)
        text = text.str.replace(thousands, '', regex=False)
    if decimal != '.':
        text = text.str.replace(decimal, '.', regex=False)
    v = pd.to_numeric(text.mask(absent), errors='coerce').astype(float)
    v = v.where(np.isfinite(v))
    return v, absent, (~absent & v.isna())


def timestamps(values, *, timezone='Asia/Tokyo', format='ISO8601', excel_epoch=None):
    """Localize naive times explicitly. Numeric serials require an epoch."""
    from openpyxl.utils.datetime import from_excel
    from datetime import datetime
    from pytz.exceptions import InvalidTimeError
    result = []
    for v in values:
        try:
            if pd.isna(v) or str(v).strip() == '':
                result.append(pd.NaT); continue
            if isinstance(v, (int, float, np.number)):
                if excel_epoch not in ('1900', '1904'):
                    raise ValueError('numeric time without epoch')
                if excel_epoch == '1900' and 60 <= float(v) < 61:
                    raise ValueError('fictitious 1900-02-29')
                v = from_excel(float(v), epoch=datetime(1899, 12, 30) if excel_epoch == '1900' else datetime(1904, 1, 1))
            t = pd.Timestamp(v) if not isinstance(v, str) else pd.Timestamp(pd.to_datetime(v, format=format, errors='raise'))
            t = t.tz_localize(timezone, ambiguous='raise', nonexistent='raise') if t.tzinfo is None else t
            result.append(t.tz_convert('UTC'))
        except (ValueError, TypeError, OverflowError, InvalidTimeError):
            result.append(pd.NaT)
    return pd.Series(pd.to_datetime(result, utc=True))


def time_flags(t, expected_dt=None, jitter_fraction=0.1):
    t = pd.Series(t).reset_index(drop=True)
    dt = t.diff().dt.total_seconds()
    return pd.DataFrame({
        'time_invalid': t.isna(),
        'time_duplicate': t.notna() & t.duplicated(keep=False),
        'time_reverse': dt.lt(0),
        'interval_irregular': (dt.sub(expected_dt).abs().gt(expected_dt*jitter_fraction) & dt.gt(0)) if expected_dt else False,
        'dt_seconds': dt,
    })


def hampel(values, window=11, k=3.5, floor=0.01):
    """Exact per-window MAD about that window's median. Full windows only."""
    x = pd.Series(values, dtype=float).reset_index(drop=True)
    if window < 3 or window % 2 != 1 or k <= 0 or floor <= 0:
        raise ValueError('odd window >=3, positive k and floor required')
    roll = x.rolling(window, center=True, min_periods=window)
    med = roll.median()
    mad = roll.apply(lambda a: np.median(np.abs(a - np.median(a))), raw=True)
    scale = (1.482602218505602 * mad).clip(lower=floor)
    assessed = med.notna() & scale.notna()
    candidate = assessed & (x-med).abs().gt(k*scale)
    return pd.DataFrame({'candidate': candidate, 'assessed': assessed, 'median': med, 'scale': scale})


def freeze_candidates(values, run_length=8):
    """Mark the complete exact-equality run, including its first observation."""
    x = pd.Series(values, dtype=float).reset_index(drop=True)
    if run_length < 2:
        raise ValueError('run_length >=2 required')
    groups = (x.ne(x.shift()) | x.isna()).cumsum()
    length = x.groupby(groups).transform('size')
    return x.notna() & length.ge(run_length)


def interpolate_short(t, values, *, max_gap_seconds, eligible=None, groups=None, anchors_ok=None):
    """Fill entire interior runs only, measured between bounding observations.

    Reject duplicate/reversed/invalid times. Require every missing point and
    both bounding observations in one consecutive mode segment. Never partially
    fill a long gap. Invalid tokens and stopped operation are ineligible by CLI.
    """
    t = pd.Series(t).reset_index(drop=True)
    x = pd.Series(values, dtype=float).reset_index(drop=True)
    if len(t) != len(x):
        raise ValueError('length mismatch')
    if max_gap_seconds <= 0 or t.isna().any() or t.duplicated().any() or not t.is_monotonic_increasing:
        raise ValueError('interpolation requires valid, unique, increasing times and positive gap')
    ok = np.ones(len(x), bool) if eligible is None else np.asarray(eligible, dtype=bool)
    anchor = np.ones(len(x), bool) if anchors_ok is None else np.asarray(anchors_ok, dtype=bool)
    g = np.zeros(len(x), int) if groups is None else np.asarray(groups)
    if any(len(a) != len(x) for a in (ok, anchor, g)):
        raise ValueError('mask length mismatch')
    y = x.copy(); filled = pd.Series(False, index=x.index)
    i = 0
    while i < len(x):
        if pd.notna(x.iloc[i]):
            i += 1; continue
        a = i
        while i < len(x) and pd.isna(x.iloc[i]): i += 1
        b = i
        if a == 0 or b == len(x): continue
        span = (t.iloc[b]-t.iloc[a-1]).total_seconds()
        if not (span <= max_gap_seconds and ok[a:b].all() and anchor[a-1] and anchor[b] and np.all(g[a-1:b+1] == g[a-1])):
            continue
        w = (t.iloc[a:b]-t.iloc[a-1]).dt.total_seconds()/span
        y.iloc[a:b] = x.iloc[a-1] + w*(x.iloc[b]-x.iloc[a-1])
        filled.iloc[a:b] = True
    return y, filled


def compare(before, after):
    a, b = pd.Series(before, dtype=float).reset_index(drop=True), pd.Series(after, dtype=float).reset_index(drop=True)
    if len(a) != len(b): raise ValueError('comparison requires matched rows')
    paired = a.notna() & b.notna()
    def stats(x):
        return {'n': int(x.count()), 'mean': x.mean(), 'std_ddof1': x.std(ddof=1), 'min': x.min(), 'max': x.max()}
    return {'before': stats(a), 'after': stats(b), 'paired_n': int(paired.sum()),
            'paired_max_abs_change': (b[paired]-a[paired]).abs().max(),
            'filled_n': int((a.isna() & b.notna()).sum())}
