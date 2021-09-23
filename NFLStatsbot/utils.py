'''
This file contains the logic for the statistics
NFLFastR -> https://cran.r-project.org/web/packages/nflfastR/nflfastR.pdf
'''
import os
import requests
import random
import numpy as np
import nflfastpy
import pandas as pd
import re
import time

all_categories = np.genfromtxt('data/categories.txt', dtype='str')
p_cats = np.flatnonzero(np.core.defchararray.find(all_categories,"_id")!=-1)
master_player_categories = []
for p in p_cats:
    master_player_categories.append(all_categories[p])
years = np.genfromtxt('data/years.txt', dtype='str')
teams = pd.read_csv('data/teams.csv', dtype='str')
teams = teams.applymap(lambda s:s.lower() if type(s) == str else s)
f_categories = pd.read_csv('data/cat_format.csv', dtype='str')
categories = f_categories['category'].values
off_categories = np.genfromtxt('data/off_cats.txt', dtype='str')
stat_set = set()
off_pos = ["QB", "RB", "WR", "TE", "T", "OG", "OT", "G", "FB", "C", "LS", "P", "K"]

def get_full_roster():
    roster_url = 'https://github.com/mrcaseb/nflfastR-roster/blob/master/data/nflfastR-roster.csv.gz?raw=True'
    df = pd.read_csv(roster_url, compression='gzip', low_memory=False)
    return df

def get_roster_data(year):
    roster_url = f'https://github.com/mrcaseb/nflfastR-roster/blob/master/data/seasons/roster_{year}.csv?raw=True'
    df = pd.read_csv(roster_url, low_memory=False)
    return df

# loads play by play data for all years
def load_pbp_data_():
    d = {}
    for y in years:
        d[int(y)] = nflfastpy.load_pbp_data(year=int(y))
    return d

# gets player names
def get_players(year):
    if year == None:
        roster_df = get_full_roster()
    else:
        roster_df = get_roster_data(year)
    return (roster_df['full_name'].str.lower().to_numpy(),
            roster_df['first_name'].str.lower().to_numpy(),
            roster_df['last_name'].str.lower().to_numpy())
    

# gets player position
def get_position(gsis_id, pbp_id, year):
    roster_df = get_roster_data(year)
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
    roster_df = get_full_roster()
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
        roster_df = get_full_roster()
        # keys = {"full_name":"teamPlayers.displayName", "gsis_id":"teamPlayers.gsisId", "espn_id":"pbp_id"}
        keys = {"full_name":"full_name", "gsis_id":"gsis_id", "espn_id":"espn_id"}
    else:
        roster_df = get_roster_data(year)
        keys = {"full_name":"full_name", "gsis_id":"gsis_id", "espn_id":"espn_id"}
    
    name = name.lower()
    rd = roster_df
    rd[keys["full_name"]] = roster_df[keys["full_name"]].str.lower()
    rd["position"] = roster_df["position"].str.lower()
    rd = roster_df.loc[roster_df[keys['full_name']] == name]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(rd[list(keys.keys()) + ['position']])
    gsis_df = rd[rd[keys["gsis_id"]].notna()]
    pbp_df = rd[rd[keys["espn_id"]].notna()]
    gsis_id = None
    pbp_id = None

    if gsis_df.shape[0] == 0 and pbp_df.shape[0] == 0:
        return (gsis_id, pbp_id)

    if gsis_df.shape[0] != 0 and pbp_df.shape[0] != 0:
        if gsis_df.shape[0] <= 1  or pbp_df.shape[0] <= 1:
            r = 0
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
            pbp_id = gsis_df[keys['espn_id']].iloc[r]
        elif position == None or (position not in gsis_df['position'].values and position not in pbp_df['position'].values):
            r = random.randint(0,min(gsis_df.shape[0], pbp_df.shape[0])-1)
            gsis_id = gsis_df[keys['gsis_id']].iloc[r]
            pbp_id = gsis_df[keys['espn_id']].iloc[r]
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
        gsis_id = None
    
    return (gsis_id, pbp_id)

# returns True if the player is active
def is_active(gsis_id, pbp_id):
    roster_df = get_roster_data(2021)
    rd = roster_df[roster_df['espn_id'] == pbp_id]
    if len(rd) == 0:
        rd = roster_df[roster_df['gsis_id'] == gsis_id]
    if len(rd) >= 1:
        return True
    else:
        return False

# Converts the readable category to NFLFastR category
def convert_category(s_cat):
    if s_cat.lower() == "win":
        return None
    if s_cat.lower() == "td":
        return "touchdown"
    cat = '_'.join(s_cat.lower().split(' '))
    possible = []
    for c in categories:
        if cat == c:
            return cat
        if cat in c: 
            possible.append(c)
    if len(possible) == 1:
        return possible[0]
    elif len(possible) == 0:
        try:
            row = f_categories[(f_categories == s_cat).any(axis=1)]
            if len(row) == 0:
                return None
            return row["category"].values[0]
        except:
            return None
    else:
        # print("Too Many Category Matches")
        return possible[0]

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


# Converts team name from 'name' to opt
def convert_team(name, opt):
    name = name.lower()
    row = teams[(teams == name).any(axis=1)]
    if opt == "abbrev":
        return row["abbrev"].values[0]
    elif opt == "full":
        return row["full"].values[0]
    elif opt == "city":
        return row["city"].values[0]
    else:
        return row["mascot"].values[0]

# formats the category based on if it is singular or plural (data/cat_format.csv)
def format_cat(cat, single, pos="DEFAULT"):
    if pos == None:
        pos = "DEFAULT"
    cat = cat.lower()
    if ("tackle" in cat or "sack" in cat or (cat=="qb_hit" and pos=="QB")) and pos in off_pos and not (pos=="QB" and "tackle" in cat):
        if single:
            return "time"
        else:
            return "times"
    if ("tackle" in cat or "sack" in cat) and pos == "OFFENSE":
        if single:
            return "time"
        else:
            return "times"
    row = f_categories[(f_categories == cat).any(axis=1)]
    if single:
        return row["singular"].values[0]
    else:
        return row["plural"].values[0]

def capitalize_name(name):
  fname = ""
  sp = name.split(" ")
  for s in sp:
    comps = s.split(".")
    apost = s.split("'")
    if len(comps) > 1:
      for c in comps:
        if c == "":
          continue
        fname = fname + c.capitalize() + "." 
      fname += " "
    elif len(apost) > 1:
      for a in range(len(apost)):
        if apost[a] == "":
          continue
        if a != len(apost)-1:
          fname = fname + apost[a].capitalize() + "'" 
        else:
          fname = fname + apost[a].capitalize()
      fname += " "
    else:
      fname = fname + s.capitalize() + " " 
  return fname

# obtains a random statistic. Does not repeat statistics if called multiple times
# Has a higher chance of player due to large number of players compared to teams
def random_stat():
    r = random.uniform(0, 1)
    random_cats = categories.tolist()
    if r < 0.9:
        # random player stat
        r = random.randint(0, len(random_cats)-1)
        r_category = random_cats[r]
        r = random.randint(0, len(years)-1)
        r_year = years[r]
        players, first, last = get_players(r_year)
        r = random.randint(0, len(players)-1)
        r_player = players[r]
        # print("\t\t", r_player, r_year, r_category)
        msg = player_stat(r_player, r_year, r_category)
        if msg in stat_set:
            return None
        if "has not played" in msg or "did not play" in msg:
            return None
        stat_set.add(msg)
        return msg
    else:
        # random team stat
        r = random.randint(0, teams.shape[0]-1)
        r_team = teams["abbrev"].iloc[r]
        r = random.randint(0, len(random_cats)-1)
        r_category = random_cats[r]
        r = random.randint(0, len(years)-1)
        r_year = years[r]
        r = random.randint(0, 1)
        pos = (r == 1)
        # print("\t\t", r_team, pos, r_year, r_category)
        msg = team_stat(r_team, pos, r_year, r_category)
        if msg in stat_set:
            return None
        stat_set.add(msg)
        return msg

# helper function to underline a string
def underline(string):
    u = "\u0332"
    underlined = ""
    for s in string:
        underlined += s + u
    return underlined

# helper function for formatting joining a player/team name with the statistic
def joiner(cat, p_or_t, off_team, id, pos, year=None):
    av_cats = ["ydstogo", "yards_gained"]
    cur_season = year == 2021
    if p_or_t == "player":
        if cat == "extra_point_result" or cat == "field_goal_result":
            c = " made "
        elif pos == "QB" and "tackle" in cat:
            c = " was on the field for "
        elif cat == "qb_hit" and pos in off_pos and pos != "QB":
            c = " was on the field for "
        elif cat == "temp" or cat == "wind":
            c = " played in an average "
        elif "prob" in cat or cat == "cp" or cat == "cpoe" or cat in av_cats:
            c = " has an average of " if cur_season else " had an average of "
        elif ("tackle" in cat or "sack" in cat or (cat == "qb_hit" and pos=="QB")) and pos in off_pos:
            fcat = format_cat(cat, True)
            if "tackle" in cat:
                fcat = fcat.replace("tackle", "tackled")
            elif "sack" in fcat:
                fcat = fcat.replace("sack", "sacked")
            elif cat == "qb_hit":
                fcat = "hit"
            c = " was " + fcat + " "
        elif (is_active(id[0], id[1]) and off_team) or cur_season:
            c = " has "
        else:
            c = " had "
    else:
        if cat == "extra_point_result" or cat == "field_goal_result":
            c = " has made the " if cur_season else " made "
        elif off_team == False and cat in av_cats:
            c = " defense has allowed an average " if cur_season else " defense allowed an average "
        elif cat == "temp" or cat == "wind":
            c = " played in average "
        elif "prob" in cat or cat == "cp" or cat == "cpoe" or cat in av_cats:
            c = " has an average " if cur_season else " had an average "
        elif off_team == False and cat in off_categories:
            c = " defense has allowed" if cur_season else " defense allowed "
        elif off_team == False and cat not in off_categories:
            c = " defense has " if cur_season else " defense had "
        elif ("tackle" in cat or "sack" in cat) and off_team == True:
            fcat = format_cat(cat, True)
            if "tackle" in cat:
                fcat = fcat.replace("tackle", "tackled")
            elif "sack" in fcat:
                fcat = fcat.replace("sack", "sacked")
            connector =  " have been " if cur_season else " were "
            c = connector + fcat + " "
        elif cur_season: 
            c = " has "
        else:
            c = " had "
    return c

# obtains a player statistic with the given name, year, and category
# if year is None, obtains career stats
def player_stat(name, year, category, position=None):
    if year is not None and (int(year) < 1999 or int(year) > 2021):
        return None
    if category == None:
        return None

    cat = convert_category(category)
    if cat == None:
        print("Error: Invalid Category:", category)
        return None
    player_categories = get_player_cats(cat)
    s_name = name
    names = s_name.split(" ")
    fname = capitalize_name(name)
    s_name = names[0][0] + "." + name.replace(names[0] + " ", "")
    gsis_id, pbp_id = get_player_id(name, year, position)
    if gsis_id == None and pbp_id == None:
        if year == None:
            return fname + "has not played in the NFL."
        else:
            return fname + "did not play in the NFL in " + str(year) + "."
    if gsis_id == None:
        try:
            gsis_id = nflfastpy.utils.convert_to_gsis_id(pbp_id)
        except Exception as e:
            print(e)
            return fname + "has not played in the NFL."
    if gsis_id == None and year == None:
        return fname + "has not played in the NFL."
    elif gsis_id == None:
        return fname + "did not play in the NFL in " + str(year) + "."
    if year == None:
        pos = get_position_all(gsis_id, pbp_id)
    else:
        pos = get_position(gsis_id, pbp_id, year)

    if year == None:
        df = pd.DataFrame()
        for y in years:
            data = nflfastpy.load_pbp_data(year=int(y))
            data = data[data['week']<=(18 if int(y) >= 2021 else 17)]

            if cat == "fg_prob":
                data = data[player_categories + [cat, "field_goal_attempt"]]
            elif cat == "extra_point_prob":
                data = data[player_categories + [cat, "extra_point_attempt"]]
            elif "td_prob" in cat:
                data = data[player_categories + [cat, "touchdown"]]
            elif "/play" in cat and "epa" in cat:
                data = data[player_categories + [cat.replace("/play", "")]]
            elif cat == "reception":
                data = data[player_categories + ["passing_yards"]]
            elif pos == "QB" and "touchdown" in cat:
                data = data[["interception", "fumble"] + player_categories + [cat]]
            elif cat == "tot_yards":
                data = data[["passing_yards", "receiving_yards", "rushing_yards"] + player_categories]
            elif cat == "cmp_pct":
                data = data[data["interception"] != 1]
                data = data[["pass_attempt", "complete_pass", "incomplete_pass", "passer_player_id", "passer_id"]]
                data = data[data["complete_pass"] != data["incomplete_pass"]]
            elif cat not in player_categories:
                data = data[player_categories + [cat]]
            else:
                data = data[player_categories]

            data = data.applymap(lambda s:s.lower() if type(s) == str else s)
            data = data[data.eq(gsis_id).any(1)]
            df = df.append(data)
        c = joiner(cat, "player", True, (gsis_id, pbp_id), pos, year)
        if pos == None:
            f_pos = ""
        else:
            f_pos = "(" + pos + ")"

        if(len(df.index) == 0):
            return fname + f_pos + c + "0 " + format_cat(cat, False, pos=pos) + " in his career."
            
        stat_sum = get_stat(df, cat, pos, gsis_id)

        if stat_sum == 1:
            return fname + f_pos + c + str(stat_sum) + " " + format_cat(cat, True, pos=pos) + " in his career."
        else:
            return fname + f_pos + c + str(stat_sum) + " " + format_cat(cat, False, pos=pos) + " in his career."
    else:
        data = nflfastpy.load_pbp_data(year=int(year))
        data = data[data['week']<=(18 if int(year) >= 2021 else 17)]

        if cat == "fg_prob":
            df = data[player_categories + [cat, "field_goal_attempt"]]
        elif cat == "extra_point_prob":
            df = data[player_categories + [cat, "extra_point_attempt"]]
        elif "td_prob" in cat:
            df = data[player_categories + [cat, "touchdown"]]
        elif "/play" in cat and "epa" in cat:
            df = data[player_categories + [cat.replace("/play", "")]]
        elif cat == "reception":
            df = data[player_categories + ["passing_yards"]]
        elif pos == "QB" and "touchdown" in cat:
            df = data[["interception", "fumble"] + player_categories + [cat]]
        elif cat == "tot_yards":
            df = data[["passing_yards", "receiving_yards", "rushing_yards"] + player_categories]
        elif cat == "cmp_pct":
            data = data[data["interception"] != 1]
            df = data[["pass_attempt", "complete_pass", "incomplete_pass", "passer_player_id", "passer_id"]]
            df = df[df["complete_pass"] != df["incomplete_pass"]]
        elif cat not in player_categories:
            df = data[player_categories + [cat]]
        else:
            df = data[player_categories]

        df = df.applymap(lambda s:s.lower() if type(s) == str else s)
        df = df[df.eq(gsis_id).any(1)]
        zero_cats = ["reception", "receiving_yards", "cmp_pct", "tot_yards"]
        c = joiner(cat, "player", False, (gsis_id, pbp_id), pos, year)
        if(len(df.index) == 0):
            df = data[master_player_categories]
            df = df.applymap(lambda s:s.lower() if type(s) == str else s)
            df = df[df.eq(gsis_id).any(1)]
            if len(df.index) != 0:
                return fname + "(" + pos + ")" + c + "0 " + format_cat(cat, False, pos=pos) + " in " + str(year) + "."
            return fname + "(" + pos + ")" + " did not play in the NFL in " + str(year) + "."

        stat_sum = get_stat(df, cat, pos, gsis_id)
        
        if stat_sum == 1:
            return fname + "(" + pos + ")" + c + str(stat_sum) + " " + format_cat(cat, True, pos=pos) + " in " + str(year) + "."
        else:
            return fname + "(" + pos + ")" + c + str(stat_sum) + " " + format_cat(cat, False, pos=pos) + " in " + str(year)  + "."
    return -1

# helper function to get a statistic from the dataframe
def get_stat(df, cat, pos="DEFAULT", player=""):  
    epa_play = False
    if "/play" in cat:
        epa_play = True
        cat = cat.replace("/play", "")
    prob_cats = ["cp", "xpass", "xyac_success", "xyac_fd", "cmp_pct"]
    big_prob_cats = ["pass_oe", "cpoe"]
    av_cats = ["ydstogo", "yards_gained"]
    if cat == "extra_point_result":
        values = df[cat].value_counts()
        if 'good' in values:
            stat_sum = values['good']
        else:
            stat_sum = 0
    elif cat == "tot_yards":
        rush_yards = df["rushing_yards"].dropna().sum()
        stat_sum = rush_yards 
        if pos == "QB":
            stat_sum += df["passing_yards"].dropna().sum()
        else:
            stat_sum += df["receiving_yards"].dropna().sum()
    elif cat == "cmp_pct":
        try:
            cmps = df["complete_pass"].sum()
            att = df["pass_attempt"].sum()
            if att > 50:
                stat_sum = ((cmps-att/100)/att) #weighting for nflfastr discrepancies
            else:
                stat_sum = (cmps/att)
        except:
            stat_sum = 0
    elif "sack" == cat and player != "":
        try:
            sack_p_cats = [x for x in df.columns if "sack" in x]
            half_sack_cats = [x for x in sack_p_cats if "half" in x]
            sack_p_cats = [x for x in sack_p_cats if "half" not in x]

            half_sacks = df[half_sack_cats + [cat]].dropna()
            full_sacks = df[sack_p_cats].dropna()
            stat_sum = 0.5 * half_sacks[cat].sum() + full_sacks[cat].sum() 
        except:
            stat_sum = 0
    elif cat == "reception":
        probs = [float(i) for i in df["passing_yards"].values if (not np.isnan(i))]
        stat_sum = len(probs)
    elif epa_play:
        stat_sum = df[cat.replace("/play", "")].sum()
        try:
            stat_sum /= df.shape[0]
        except:
            stat_sum = 0
    elif cat == "penalty_type":
        values = df[cat].value_counts()
        stat_sum = len(values)
    elif cat == "pass_length":
        values = df[cat].value_counts()
        if 'deep' in values:
            stat_sum = values['deep']
        else:
            stat_sum = 0
    elif cat == "field_goal_result":
        values = df[cat].value_counts()
        if 'made' in values:
            stat_sum = values['made']
        else:
            stat_sum = 0
    elif "td_prob" in cat:
        try:
            df = df[df["touchdown"] == 1]
            probs = [float(i) for i in df[cat].values if (not np.isnan(i) and i != 0)]
            stat_sum = sum(probs)
            stat_sum /= len(probs)
        except:
            stat_sum = 0
    elif cat == "fg_prob":
        try:
            df = df[df["field_goal_attempt"] == 1]
            probs = [float(i) for i in df[cat].values if (not np.isnan(i) and i != 0)]
            stat_sum = sum(probs)
            stat_sum /= len(probs)
        except:
            stat_sum = 0
    elif cat == "extra_point_prob":
        try:
            df = df[df["extra_point_attempt"] == 1]
            probs = [float(i) for i in df[cat].values if (not np.isnan(i) and i != 0)]
            stat_sum = sum(probs)
            stat_sum /= len(probs)
        except:
            stat_sum = 0
    elif cat == "two_point_conv_result":
            values = df[cat].value_counts()
            if 'success' in values:
                stat_sum = values['success']
            else:
                stat_sum = 0
    elif cat == "touchdown" and pos == "QB":
        df = df[df["interception"]!=1]
        df = df[df["fumble"]!=1]
        stat_sum = df[cat].sum()
    elif "prob" in cat or cat == "wind" or cat == "temp" or cat in prob_cats or cat in big_prob_cats or cat in av_cats:
        try: 
            probs = [float(i) for i in df[cat].values if (not np.isnan(i) and i != 0)]
            stat_sum = sum(probs)
            stat_sum /= len(probs)
            stat_sum = round(stat_sum, 3)
        except:
            stat_sum = 0
    else:
        try:
            stat_sum = df[cat].sum()
            values = df[cat].value_counts()
        except:
            stat_sum = df[cat].count()
    
    try:
        i_sum = int(stat_sum)
    except:
        stat_sum = df[cat].count()
        i_sum = stat_sum
    if i_sum == stat_sum:
        stat_sum = i_sum
    else:
        stat_sum = round(stat_sum, 3)
    
    if ("prob" in cat or cat in prob_cats):
        stat_sum *= 100
        stat_sum = round(stat_sum, 3)
        stat_sum = str(stat_sum) + "%"
    return stat_sum

# obtains a team statistic from the given name, defense or offense, year, and category
# pos - True if on offense (has possession)
def team_stat(name, pos, year, category):
    if year is not None and (int(year) < 1999 or int(year) > 2021):
        return None
    act_name = convert_team(name, "abbrev")
    if act_name == "oak" or act_name == "lv":
      abbrev_name = "lv"
      if int(year) >= 2020:
        act_name = "lv"
      else:
        act_name = "oak"
    elif act_name == "sd" or act_name == "lac":
      abbrev_name = "lac"
      if int(year) >= 2017:
        act_name = "lac"
      else:
        act_name = "sd"
    elif act_name == "stl" or act_name == "la":
      abbrev_name = "la"
      if int(year) >= 2016:
        act_name = "la"
      else:
        act_name = "stl"
    else:
      abbrev_name = act_name
    
    team_cats_o = ["passing_yards", "rushing_yards", "touchdown", "epa"]
    team_cats_d = ["fumble_forced", "interception", "sack", "solo_tackle", "epa"]
    if year == None:
        if category == None:
            df_o = pd.DataFrame()
            df_d = pd.DataFrame()
            for y in years:
                data = nflfastpy.load_pbp_data(year=int(y))
                data = data[data['week']<=(18 if int(y) >= 2021 else 17)]
                data = data.applymap(lambda s:s.lower() if type(s) == str else s)
                data_o = data[['posteam'] + team_cats_o]
                data_o = data_o[data_o.eq(abbrev_name).any(1)]
                data_d = data[['defteam'] + team_cats_d]
                data_d = data_d[data_d.eq(abbrev_name).any(1)]
                df_o = df_o.append(data_o)
                df_d = df_d.append(data_d)
            stats_o = {}
            stats_d = {}
            for i in team_cats_o:
                if i == "epa":
                    i = "epa/play"
                stats_o[i] = get_stat(df_o, i)
            for i in team_cats_d:
                if i == "epa":
                    i = "epa/play"
                stats_d[i] = get_stat(df_d, i)
              
            fnames = convert_team(act_name, "full").split(" ")
            fnames = [f.capitalize() for f in fnames]
            fname = " ".join(fnames)
            msg = underline(fname + " - Since 1999:")
            for s in stats_o.keys():
                if s == "epa/play":
                    f_c = "Offense EPA/Play"
                else:
                    if stats_o[s] == 1:
                      f_c = format_cat(s, True).title()
                    else:
                      f_c = format_cat(s, False).title()
                msg += "\n" + f_c + ": " + str(stats_o[s])
            for s in stats_d.keys():
                if s == "fumble_forced":
                    f_c = "Forced Fumbles"
                elif s == "epa/play":
                    f_c = "Defense EPA/Play"
                else:
                    if stats_d[s] == 1:
                      f_c = format_cat(s, True).title()
                    else:
                      f_c = format_cat(s, False).title()
                msg += "\n" + f_c + ": " + str(stats_d[s])
            return msg
        else:
            df = pd.DataFrame()
            cat = convert_category(category)
            if cat == None:
                print("Error: Invalid Category:", category)
                return None
            for y in years:
                data = nflfastpy.load_pbp_data(year=int(y))
                data = data[data['week']<=(18 if int(y) >= 2021 else 17)]

                if_fg = []
                if "/play" in cat:
                    if_fg.append(cat.replace("/play", ""))
                elif cat == "reception":
                    if_fg.append("passing_yards")
                elif cat == "tot_yards":
                    if_fg += ["receiving_yards", "rushing_yards"]
                elif cat == "cmp_pct":
                    if_fg += ["pass_attempt", "complete_pass", "incomplete_pass"]
                else:
                    if_fg.append(cat)

                if cat == "fg_prob":
                    if_fg.append("field_goal_attempt")
                elif cat == "extra_point_prob":
                    if_fg.append("extra_point_attempt")
                elif "td_prob" in cat:
                    if_fg.append("touchdown")

                if pos:
                    data = data[['posteam'] + if_fg]
                else:
                    data = data[['defteam'] + if_fg]
                
                if cat == "cmp_pct":
                    data = data[data["complete_pass"] != data["incomplete_pass"]]

                data = data.applymap(lambda s:s.lower() if type(s) == str else s)
                data = data[data.eq(abbrev_name).any(1)]
                df = df.append(data)
            
            stat_sum = get_stat(df, cat, "TEAM")

            fnames = convert_team(act_name, "full").split(" ")
            fnames = [f.capitalize() for f in fnames]
            fname = " ".join(fnames)
            if pos:
                f_cat_pos = "OFFENSE"
            else:
                f_cat_pos = "DEFAULT"

            c = joiner(cat, "team", pos, name, "", year)
            if stat_sum == 1:
                return "The " + fname + c + str(stat_sum) + " " + format_cat(cat, True, f_cat_pos) + " since 1999."
            else:
                return "The " + fname + c + str(stat_sum) + " " + format_cat(cat, False, f_cat_pos) + " since 1999."
    else:
        data = nflfastpy.load_pbp_data(year=int(year))
        data = data[data['week']<=(18 if int(year) >= 2021 else 17)]
        if category == None:
            data = data.applymap(lambda s:s.lower() if type(s) == str else s)
            df_o = data[['posteam'] + team_cats_o]
            df_o = df_o[df_o.eq(abbrev_name).any(1)]
            df_d = data[['defteam'] + team_cats_d]
            df_d = df_d[df_d.eq(abbrev_name).any(1)]
            stats_o = {}
            stats_d = {}
            for i in team_cats_o:
                if i == "epa":
                    i = "epa/play"
                stats_o[i] = get_stat(df_o, i)
            for i in team_cats_d:
                if i == "epa":
                    i = "epa/play"
                stats_d[i] = get_stat(df_d, i)
            fnames = convert_team(act_name, "full").split(" ")
            fnames = [f.capitalize() for f in fnames]
            fname = " ".join(fnames)
            msg = underline(fname + " - " + str(year) + ":")
            for s in stats_o.keys():
                if s == "epa/play":
                    f_c = "Offense EPA/Play"
                else:
                    if stats_o[s] == 1:
                      f_c = format_cat(s, True).title()
                    else:
                      f_c = format_cat(s, False).title() 
                msg += "\n" + f_c + ": " + str(stats_o[s])
            for s in stats_d.keys():
                if s == "forced_fumble_player_1_team":
                    f_c = "Forced Fumbles"
                elif s == "epa/play":
                    f_c = "Defense EPA/Play"
                else:
                    if stats_d[s] == 1:
                      f_c = format_cat(s, True).title()
                    else:
                      f_c = format_cat(s, False).title()
                msg += "\n" + f_c + ": " + str(stats_d[s])
            return msg
        else:
            cat = convert_category(category)
            if cat == None:
                print("Error: Invalid Category:", category)
                return None
            
            if_fg = []
            if "/play" in cat:
                if_fg.append(cat.replace("/play", ""))
            elif cat == "reception":
                if_fg.append("passing_yards")
            elif cat == "tot_yards":
                if_fg += ["receiving_yards", "rushing_yards"]
            elif cat == "cmp_pct":
                if_fg += ["pass_attempt", "complete_pass", "incomplete_pass"]
            else:
                if_fg.append(cat)
                
            if cat == "fg_prob":
                if_fg.append("field_goal_attempt")
            elif cat == "extra_point_prob":
                if_fg.append("extra_point_attempt")
            elif "td_prob" in cat:
                if_fg.append("touchdown")

            if pos:
                df = data[['posteam'] + if_fg]
            else:
                df = data[['defteam'] + if_fg]

            if cat == "cmp_pct":
                df = df[df["complete_pass"] != df["incomplete_pass"]]

            df = df.applymap(lambda s:s.lower() if type(s) == str else s)
            df = df[df.eq(abbrev_name).any(1)]
            stat_sum = get_stat(df, cat, "TEAM")
            fnames = convert_team(act_name, "full").split(" ")
            fnames = [f.capitalize() for f in fnames]
            fname = " ".join(fnames)

            if pos:
                f_cat_pos = "OFFENSE"
            else:
                f_cat_pos = "DEFAULT"

            c = joiner(cat, "team", pos, name, "", year)

            if stat_sum == 1:
                return "The " + fname + c + str(stat_sum) + " " + format_cat(cat, True, f_cat_pos) + " in " + str(year) + "."
            else:
                return "The " + fname + c + str(stat_sum) + " " + format_cat(cat, False, f_cat_pos) + " in " + str(year) + "."

    return -1

# parses any tweet to find players and teams
def tweet_parser(tweet):
    #parse a tweet and return a tuple of arrays of players and teams
    punctuation = re.compile("[.!?\\-@':,\n#]")
    tweet = punctuation.sub('', tweet)
    tweet = tweet.replace("#", "")
    tweet = tweet.replace("'", "")
    words = tweet.split(" ")
    p_players = []
    p_teams = []
    player_names, first, last = get_players(None)
    for i in range(len(words)):
        if i < len(words)-1:
            p_name = words[i] + " " + words[i+1]
        else:
            p_name = None
        p_team = words[i]
        if p_team.lower() in teams.values and p_team not in p_teams:
            p_teams.append(p_team)
        elif p_name is not None and p_name.lower() in player_names and p_name not in p_players:
            p_players.append(p_name)
    return (p_players, p_teams)

# helper function to check if s is an int
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# parses a request tweet for players, teams, years and categorys
def mention_parser(tweet):
    print(tweet)
    at_tag = re.compile("@([a-zA-Z0-9]|[_])*", re.IGNORECASE)
    punctuation = re.compile("[!?\\-@:\n]")
    #parse a more specific and targeted tweet and return a player/team, year, category
    category = []
    player = []
    team = []
    year = []
    positions = []
    players, first, last = get_players(None)
    tweet = at_tag.sub('', tweet)
    tweet = punctuation.sub('', tweet)
    tweet = tweet.replace("'", "")
    while len(tweet) > 0 and tweet[0] == ' ':
        tweet = tweet[1:]
    # print(tweet)
    words = tweet.split(",")
    for w in words:
        w = w.lower()
        if "allowed" in w:
          w = w.replace("allowed", "")
          defense = True
        else:
          defense = False
        if w == "":
            continue
        if "(" in w and ")" in w:
            p_pos = w.split("(")
            pos = p_pos[1].replace(")", "")
            w = w.replace("(" + pos + ")", "")
        else:
            pos = None
        while w[0] == ' ':
            w = w[1:]
        while w[-1] == ' ' or w[-1]==".":
            w = w[:-1]
        # print(w)
        c = "default"
        if w[-1] == 's':
            c = w[:-1]
        cat1 = convert_category(w)
        cat2 = convert_category(c)
        # print("categories", cat1, cat2)
        if cat1 in categories and cat1 not in category:
            if defense:
              category.append(cat1+"_allowed")
            else:
              category.append(cat1)
        elif cat2 in categories and cat2 not in category:
            if defense:
              category.append(cat2+"_allowed")
            else:
              category.append(cat2)
        elif is_int(w) and w in years and int(w) not in year:
            year.append(int(w))
        elif w in teams.values and w not in team:
            team.append(w)
        elif w in players and w not in player:
            player.append(w)
            positions.append(pos)
        elif w in players and w in player and pos != None and pos not in positions:
            player.append(w)
            positions.append(pos)
        else:
            print("ERROR: Invalid parameter, skipping")
            continue
    if player == []:
        player = [None]
        positions=[None]
    if team == []:
        team = [None]
    if category == []:
        category = [None]
    if year == []:
        year = [None]
    return (player, team, year, category, positions)    

# helper function to find the unique values in a column of the play by play data
def unique_finder(cat):
  data = pd.read_csv(
            'https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_' \
            + str(2019) + '.csv.gz?raw=True',compression='gzip', low_memory=False
  )
  return data[cat].unique()