import nfl_data_py as nfl
from load_constants import years, years_int_list, f_categories, master_player_categories, all_categories
from utils import blockPrint, enablePrint

def get_roster_year(year, columns=None):
    blockPrint()
    if columns == None:
        data = nfl.import_rosters([int(year)])
    else:
        data = nfl.import_rosters([int(year)], columns)
    enablePrint()
    return data

def get_full_roster(columns):
    blockPrint()
    if columns == None:
        data = nfl.import_rosters(years_int_list)
    else:
        data = nfl.import_rosters(years_int_list, columns)
    enablePrint()
    return data

def get_pbp_data(year):
    blockPrint()
    try:
        data = nfl.import_pbp_data([int(year)], cache=True)
    except:
        data = nfl.import_pbp_data([int(year)], cache=False)
        nfl.cache_pbp([int(year)])
    enablePrint()
    return data

# loads play by play data for all years
def get_full_pbp_data():
    blockPrint()
    try:
        data = nfl.import_pbp_data(years_int_list, cache=True)
    except:
        data = nfl.import_pbp_data(years_int_list, cache=False)
        nfl.cache_pbp(years_int_list)

    enablePrint()
    return data

def get_player_cats(cat):
    OFF = ["receiver_id", "receiver_player_id", "passer_id", "passer_player_id", "rusher_id", "rusher_player_id", 
            "lateral_receiver_player_id", "lateral_rusher_player_id", "punter_player_id", "kicker_player_id"]
    row = f_categories[(f_categories == cat).any(axis=1)] 
    item = str(row["player_cat"].values[0])
    if item == "NA" or item == "nan":
        return master_player_categories
    else:
        r_cats = item.split("|")
        if len(r_cats) == 0:
            return master_player_categories
        cats = []
        for c in r_cats:
            if c == "OFF":
                cats += OFF
            elif c in all_categories:
                cats.append(c)
            else:
                print("Unrecognized category:", c)
        return cats