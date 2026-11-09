"""
Save results to csv files in the outputs folder
"""

import os
import pandas as pd
import config

def Save_table(df, file_name):
    df = df.copy()
    if 'terms' in df.columns:
        df['terms'] = df['terms'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

    os.makedirs(config.output_dir, exist_ok = True)
    save_path = os.path.join(config.output_dir, file_name)
    df.to_csv(save_path, index = False)

    print(f'Table saved --> {save_path}')

    return save_path