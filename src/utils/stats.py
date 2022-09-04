import random
import pandas as pd
import numpy as np
from load_constants import categories, years, stat_set, teams, master_player_categories, full_roster_columns
from load_data import get_full_roster, get_player_cats, get_pbp_data
from converters import convert_category, convert_team
from formatters import format_name, format_cat, joiner, underline
from player_details import get_player_id, get_position, get_position_all, get_player_details
pd.set_option("display.max_rows", None, "display.max_columns", None)

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
        roster_df = get_full_roster(['player_name', 'first_name', 'last_name'])
        players = roster_df['player_name'].str.lower().to_numpy()
        r = random.randint(0, len(players)-1)
        r_player = players[r]
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
        msg = team_stat(r_team, pos, r_year, r_category)
        if msg in stat_set:
            return None
        stat_set.add(msg)
        return msg

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
    fname = format_name(name)
    s_name = names[0][0] + "." + name.replace(names[0] + " ", "")
    player_det = get_player_details(name, year, position)

    if player_det == None:
        if year == None:
            if position == None:
                return fname + " has not played in the NFL."
            else:
                return fname + "(" + position + ") has not played in the NFL."
        else:
            return fname + "did not play in the NFL in " + str(year) + "."
    
    pos_tuple = [player_det['position'], player_det['depth_chart_position']]

    pos_spec = pos_tuple[1]
    if pos_spec == None:
        pos_spec = pos_tuple[0]
   
    pos_spec = pos_spec.upper()

    if year == None:
        df = pd.DataFrame()
        for y in years:
            data = get_pbp_data(int(y))
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
            elif "QB" in pos_tuple and "touchdown" in cat:
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
            data = data[data.eq(player_det['player_id']).any(1)]
            df = pd.concat([df, data])
        c = joiner(cat, "player", True, player_det['player_id'], pos_spec, year)
        f_pos = "(" + pos_spec + ")"

        if(len(df.index) == 0):
            return fname + f_pos + c + "0 " + format_cat(cat, False, pos=pos_spec) + " in his career."
            
        stat_sum = get_stat(df, cat, pos_spec, player_det['player_id'])

        if stat_sum == 1:
            return fname + f_pos + c + str(stat_sum) + " " + format_cat(cat, True, pos=pos_spec) + " in his career."
        else:
            return fname + f_pos + c + str(stat_sum) + " " + format_cat(cat, False, pos=pos_spec) + " in his career."
    else:
        data = get_pbp_data(int(year))
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
        elif "QB" in pos_tuple and "touchdown" in cat:
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
        df = df[df.eq(player_det['player_id']).any(1)]
        zero_cats = ["reception", "receiving_yards", "cmp_pct", "tot_yards"]
        c = joiner(cat, "player", False, player_det['player_id'], pos_spec, year)
        if(len(df.index) == 0):
            df = data[master_player_categories]
            df = df.applymap(lambda s:s.lower() if type(s) == str else s)
            df = df[df.eq(player_det['player_id']).any(1)]
            if len(df.index) != 0:
                return fname + "(" + pos_spec + ")" + c + "0 " + format_cat(cat, False, pos=pos_spec) + " in " + str(year) + "."
            return fname + "(" + pos_spec + ")" + " did not play in the NFL in " + str(year) + "."

        stat_sum = get_stat(df, cat, pos_spec, player_det['player_id'])
        
        if stat_sum == 1:
            return fname + "(" + pos_spec + ")" + c + str(stat_sum) + " " + format_cat(cat, True, pos=pos_spec) + " in " + str(year) + "."
        else:
            return fname + "(" + pos_spec + ")" + c + str(stat_sum) + " " + format_cat(cat, False, pos=pos_spec) + " in " + str(year)  + "."
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
                data = get_pbp_data(int(y))
                data = data[data['week']<=(18 if int(y) >= 2021 else 17)]
                data = data.applymap(lambda s:s.lower() if type(s) == str else s)
                data_o = data[['posteam'] + team_cats_o]
                data_o = data_o[data_o.eq(abbrev_name).any(1)]
                data_d = data[['defteam'] + team_cats_d]
                data_d = data_d[data_d.eq(abbrev_name).any(1)]
                df_o = pd.concat([df_o, data_o])
                df_d = pd.concat([df_d, data_d])

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
                data = get_pbp_data(int(y))
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
                df = pd.concat([df, data])
            
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
        data = get_pbp_data(int(year))
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
