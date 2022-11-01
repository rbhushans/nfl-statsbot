import datetime
import numpy as np
import pandas as pd
import nfl_data_py as nfl

current_year = 2022
data_folder = "data/"

all_categories = np.array(nfl.see_pbp_cols(), dtype=str)
p_cats = np.flatnonzero(np.core.defchararray.find(all_categories,"_id")!=-1)
master_player_categories = []
for p in p_cats:
    master_player_categories.append(all_categories[p])
years = np.genfromtxt(data_folder + 'years.txt', dtype='str')
years_int_list = list(np.genfromtxt(data_folder + 'years.txt', dtype=int))
teams = pd.read_csv(data_folder + 'teams.csv', dtype='str')
teams = teams.applymap(lambda s:s.lower() if type(s) == str else s)
f_categories = pd.read_csv(data_folder + 'cat_format.csv', dtype='str')
categories = f_categories['category'].values
off_categories = np.genfromtxt(data_folder + 'off_cats.txt', dtype='str')
stat_set = set()
off_pos = ["QB", "RB", "WR", "TE", "T", "OG", "OT", "G", "FB", "C", "LS", "P", "K"]
full_roster_columns = ['player_name', 'position', 'first_name', 'last_name', 'player_id', 'depth_chart_position']

print("[LOAD_CONSTANTS]: Caching pbp data")
today_date = datetime.datetime.today().weekday()
if today_date == 1:
    nfl.cache_pbp(years_int_list)
print("[LOAD_CONSTANTS]: Done caching pbp data")
