import pandas as pd
import bspline_approx as bapprox

# TODO:
# 1. import file
# 2. extract water points, and zero conc points (bc, river, zero trees)
# 3. Interpolation (modify for anisotropy
# 4. Plot interpolation and errors
# 5. Evaluate source concentrations at trees from their root bulk
#
# 6. .... analysis

file_name = "statistika Jaworzno.xlsx"
df = pd.read_excel(file_name, sheet=0, index_col='sample name')
