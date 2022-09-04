import sys
import pandas as pd 
pd.set_option("display.max_rows", None, "display.max_columns", None)
sys.path.append('src/utils')
from load_data import get_roster_year, get_full_roster, get_pbp_data, get_full_pbp_data

rosters = get_roster_year(2018)
data = get_pbp_data(2018)
print(data.head())
print("=========================================")
print("=========================================")
print(rosters.head())