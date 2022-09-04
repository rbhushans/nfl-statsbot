from load_constants import f_categories, off_categories, off_pos, current_year
from player_details import is_active

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

def format_name(name):
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
    cur_season = year == current_year
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
        elif (is_active(id) and off_team) or cur_season:
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
            c = " have "
        else:
            c = " had "
    return c
