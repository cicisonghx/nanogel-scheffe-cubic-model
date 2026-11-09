"""
load_data.py

Load the ternary (AETC/AM/BAC) formulations screening dataset from the project's raw Excel file
and returns a clean df for plotting,

Usage:
    from load_data import load_data
    df = load_data()
"""

import numpy as np
import pandas as pd
import config
from sanity_check import Sanity_check

EXCLUDE_ROWS = []

def Load_data():
    df = pd.read_excel(config.data, header = 0)

    def to_percent(col):
        return col*100 if col.max()<1 else col

    out = pd.DataFrame({
        'AETC': df[config.COL_AETC],
        'AM': df[config.COL_AM],
        'BAC':df[config.COL_BAC],
        'dH':df[config.COL_DH],
        'PDI':df[config.COL_PDI]
    })

    if EXCLUDE_ROWS:
        out = out.drop(index = EXCLUDE_ROWS).reset_index(drop = True)

    Sanity_check(out)

    return out

if __name__ == '__main__':
    Load_data()






