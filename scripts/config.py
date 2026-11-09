from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
data = project_root/'data'/'scheffe subic model dataset.xlsx'


COL_AETC = 'AETC_%mol'
COL_BAC = 'BAC_%mol'
COL_AM = 'AM_%mol'
COL_DH = 'average_dH(nm)'
COL_PDI = 'average_PDI'

figure_dir  = project_root/'outputs'/'figures'

output_dir = project_root/'outputs'/'excels'