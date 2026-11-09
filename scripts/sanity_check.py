"""
sanity_check.py

Data quality check for Scheffe cubic model

Usage:
    from sanity_check import sanity check
    sanity_check(df)
"""

import numpy as np

def Sanity_check(df):
    """
    Things to be checked:
    1. AETC + AM + BAC = 100%
    2. No missing dH or PDI values
    """

    total = df['AETC'] + df['AM'] + df['BAC']
    bad = ~np.isclose(total, 100, atol = 0.1)
    if bad.any():
        print(f'WARNING: {bad.sum()} row(s) do not add up to 100%:')
        print(df.loc[bad, ['AETC','AM','BAC']])

    else:
        print(f'all {len(df)} rows sum to 100%. Constraint is satisfied.')

    if df[['dH', 'PDI']].isna().any().any():
        n_missing = df[['dH', 'PDI']].isna().any(axis=1).sum()
        print(f'WARNING: {n_missing} row(s) have missing dH or PDI values')

    else:
        print('No missing values.')


