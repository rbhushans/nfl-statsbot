from load_data import get_roster_year, get_full_roster
from load_constants import current_year, full_roster_columns
import pandas as pd
import random

# function to return a dict of player details:
# position, player_id, player_name, first_name, last_name, depth_chart_position, 
def get_player_details(name, year, position=None):
    if year == None:
        roster_df = get_full_roster(full_roster_columns)
    else:
        roster_df = get_roster_year(year)
    
    name = name.lower()
    rd = roster_df
    rd["player_name"] = roster_df["player_name"].str.lower()
    rd["position"] = roster_df["position"].str.lower()
    rd = roster_df.loc[roster_df["player_name"] == name]

    if len(rd) == 0:
        return None

    if position == None:
        # get random row
        r = random.randint(0,rd.shape[0]-1)
        row = rd.iloc[r]
    else:
        rd = rd[(rd == position).any(axis=1)]
        if len(rd) == 0:
            return None
        row = rd.iloc[0]

    return {"player_name": row["player_name"],
            "position": row["position"],
            "depth_chart_position": row["depth_chart_position"],
            "player_id": row["player_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"]}

# gets player names
def get_players(year):
    if year == None:
        roster_df = get_full_roster(full_roster_columns)
    else:
        roster_df = get_roster_year(year)
    return (roster_df['player_name'].str.lower().to_numpy(),
            roster_df['first_name'].str.lower().to_numpy(),
            roster_df['last_name'].str.lower().to_numpy())
    

# gets player position
def get_position(gsis_id, pbp_id, year):
    roster_df = get_roster_year(year)
    if pbp_id == "NaN":
        pbp_id = "DEFAULT" 
    try:
        rd = roster_df.loc[roster_df['espn_id'] == pbp_id]
        
        if len(rd) == 0:
            rd = roster_df.loc[roster_df['gsis_id'] == gsis_id]
        pos = rd['position'].iloc[0]
        return pos
    except:
        return None

def get_position_all(gsis_id, pbp_id):
    roster_df = get_full_roster(full_roster_columns)
    if pbp_id == "NaN":
        pbp_id = "DEFAULT"
    try:
        rd = roster_df.loc[roster_df['espn_id'] == pbp_id]
        
        if len(rd) == 0:
            rd = roster_df.loc[roster_df['gsis_id'] == gsis_id]
        pos = rd['position'].iloc[0]
        return pos
    except:
        return None

# returns gsis ID and pbp ID of player
def get_player_id(name, year, position=None):
    if year == None:
        roster_df = get_full_roster(full_roster_columns)
        # keys = {"player_name":"teamPlayers.displayName", "gsis_id":"teamPlayers.gsisId", "espn_id":"pbp_id"}
        keys = {"player_name":"player_name", "gsis_id":"gsis_id", "espn_id":"espn_id"}
    else:
        roster_df = get_roster_year(year)
        keys = {"player_name":"player_name", "gsis_id":"gsis_id", "espn_id":"espn_id"}
    
    name = name.lower()
    rd = roster_df
    print(rd.head())
    print(rd.columns)
    rd[keys["player_name"]] = roster_df[keys["player_name"]].str.lower()
    rd["position"] = roster_df["position"].str.lower()
    rd = roster_df.loc[roster_df[keys['player_name']] == name]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    gsis_df = rd[rd[keys["gsis_it_id"]].notna()]
    pbp_df = rd[rd[keys["espn_id"]].notna()]
    gsis_id = None
    pbp_id = None

    if gsis_df.shape[0] == 0 and pbp_df.shape[0] == 0:
        return (gsis_id, pbp_id, position)

    if gsis_df.shape[0] != 0 and pbp_df.shape[0] != 0:
        if gsis_df.shape[0] <= 1  or pbp_df.shape[0] <= 1:
            r = 0
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
            pbp_id = gsis_df[keys['espn_id']].iloc[r]
        elif position == None or (position not in gsis_df['position'].values and position not in pbp_df['position'].values):
            r = random.randint(0,min(gsis_df.shape[0], pbp_df.shape[0])-1)
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
            pbp_id = gsis_df[keys['espn_id']].iloc[r]
            position = gsis_df['position'].iloc[r]
        else:
            if position in gsis_df['position'].values:
                row = gsis_df[(gsis_df == position).any(axis=1)]
                if len(row) >= 1:
                    gsis_id = row['gsis_id'].values[0]
            if position in pbp_df['position'].values:
                row = pbp_df[(pbp_df == position).any(axis=1)]
                if len(row) >= 1:
                    pbp_id = row['espn_id'].values[0]
            if pbp_id == None:
                r = random.randint(0,pbp_df.shape[0]-1)
                pbp_id = pbp_df[keys['espn_id']].iloc[r]
            if gsis_id == None:
                r = random.randint(0,pbp_df.shape[0]-1)
                pbp_id = pbp_df[keys['espn_id']].iloc[r]
    elif gsis_df.shape[0] != 0:
        if gsis_df.shape[0] <= 1:
            r = 0
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
        elif position in gsis_df['position'].values:
            row = gsis_df[(gsis_df == position).any(axis=1)]
            if len(row) >= 1:
                gsis_id = row['gsis_id'].values[0]
        else:
            r = random.randint(0,gsis_df.shape[0]-1)
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
            position = gsis_df['position'].iloc[r]
        pbp_id = None
    else:
        if pbp_df.shape[0] <= 1:
            r = 0
            pbp_id = pbp_df[keys['espn_id']].iloc[r]
        elif position in pbp_df['position'].values:
            row = pbp_df[(pbp_df == position).any(axis=1)]
            if len(row) >= 1:
                pbp_id = row['espn_id'].values[0]
        else:
            r = random.randint(0,pbp_df.shape[0]-1)
            pbp_id = pbp_df[keys['espn_id']].iloc[r]
            position = pbp_df['position'].iloc[r]
        gsis_id = None
    
    return (gsis_id, pbp_id, position)

# returns True if the player is active
def is_active(player_id):
    roster_df = get_roster_year(current_year)
    rd = roster_df[roster_df['espn_id'] == player_id]
    
    if len(rd) >= 1:
        return True
    else:
        return False