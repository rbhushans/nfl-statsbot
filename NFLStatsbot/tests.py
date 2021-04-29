from utils import random_stat, team_stat, player_stat, mention_parser, get_players, get_player_id

# print(team_stat("bears", True, 2006, "touchdown")) # had 44
# print(team_stat("bears", False, 2006, "touchdown")) # allowed 32
# print(team_stat("cowboys", True, 2006, "touchdown")) # 
# print(team_stat("cowboys", False, 2006, "touchdown"))

# print(team_stat("bears", True, None, "xyac_epa"))
# print(team_stat("bears", True, 2020, None))
# print(team_stat("ravens", True, 2020, None)) 
# print(team_stat("bears", False, 2020, None))
# print(team_stat("ravens", True, 2020, "tot_yards"))
# print(team_stat("ravens", False, 2020, "tot_yards"))
# print(team_stat("ravens", True, 2020, "cmp_pct"))
# print(team_stat("ravens", False, 2020, "cmp_pct"))
# print(team_stat("ravens", True, 2020, "kick_distance"))
# print(team_stat("ravens", False, 2020, "interception"))
# print(team_stat("ravens", True, 2020, "interception"))
# print(team_stat("ravens", False, 2020, "fumble"))
# print(team_stat("ravens", True, 2020, "fumble"))
# print(team_stat("ravens", False, 2020, "fumble_forced"))
# print(team_stat("ravens", True, 2020, "fumble_forced"))
# print(team_stat("ravens", False, 2020, "passing_yards"))
# print(team_stat("ravens", True, 2020, "passing_yards"))
# print(random_stat())

# print(player_stat("lamar jackson", 2020, "tot_yards"))
# print(player_stat("aaron donald", 2020, "tot_yards")) 
# print(player_stat("lamar jackson", 2018, "cmp_pct"))
# print(player_stat("lamar jackson", 2019, "cmp_pct"))
# print(player_stat("lamar jackson", 2020, "cmp_pct"))
# print(player_stat("lamar jackson", 2010, "passing_yards"))
# print(player_stat("marlon humphrey", 2020, "fumble_forced"))
# print(player_stat("chase claypool", 2010, "pass_touchdown"))
# print(player_stat("chase claypool", 2020, "touchdown"))
# print(player_stat("aaron rodgers", 2020, "passing_yards"))
# print(player_stat("deshaun watson", 2018, "receiving_yards"))
# print(player_stat("aaron donald", 2020, "cmp_pct")) 
# print(player_stat("marquise brown", 2020, "receiving_yards"))
# print(player_stat("josh allen", 2020, "passing yards"))
# print(player_stat("sam koch", None, "cmp_pct"))
# print(player_stat("tom brady", 2020, "touchdown")) 
# print(player_stat("tua tagovailoa", 2020, "touchdown")) 
# print(player_stat("tom brady", 2020, "interception")) 
# print(player_stat("tua tagovailoa", 2020, "interception")) 
# print(player_stat("lamar jackson", 2020, "touchdown"))
# print(player_stat("doug baldwin", 2017, "qb hit"))
# print(player_stat("marlon humphrey", 2020, "qb hit"))
# print(player_stat("lamar jackson", 2020, "qb hit"))
# print(player_stat("doug baldwin", 2017, "tackle"))
# print(player_stat("marlon humphrey", 2020, "tackle"))
# print(player_stat("lamar jackson", 2020, "tackle"))
# print(player_stat("doug baldwin", 2017, "sack"))
# print(player_stat("marlon humphrey", 2020, "sack"))
# print(player_stat("lamar jackson", 2020, "sack"))
# print(player_stat("lamar jackson", 2010, "sack"))
# print(player_stat("lamar jackson", 2010, "qb hit"))
# print(player_stat("josh allen", 2020, "qb hit"))
# print(player_stat("aaron donald", 2020, "qb hit"))
# print(player_stat("russell wilson", 2020, "qb hit"))
# print(player_stat("russell wilson", 1999, "qb hit"))
# print(mention_parser("@nfl_statsbot epa/play, Tim Hightower, lamar jackson, 2010."))
# print(mention_parser("@nfl_statsbot epa, lamar jackson(db), josh allen (qb), 2019"))
# print(mention_parser("@nfl_statsbot xyac epa/play, josh allen, 2020."))
# print(mention_parser("@nfl_statsbot qb epa/play, tom brady, 2013."))
# print(mention_parser("@nfl_statsbot air epa/play, Aaron Rodgers, 2018."))
# print(mention_parser("@nfl_statsbot xyac epa, josh allen, 2020."))
# print(mention_parser("@nfl_statsbot qb epa, tom brady, 2013."))
# print(mention_parser("@nfl_statsbot air epa, Aaron Rodgers, 2018."))
# print(mention_parser("@nfl_statsbot detroit lions, epa/play allowed, 2008"))
# print(mention_parser("@nfl_statsbot lamar jackson (qb), epa/play, 2020"))
# print(mention_parser("@nfl_statsbot lamar jackson (db), epa/play, 2020"))
# print(mention_parser("@nfl_statsbot josh allen (qb), epa/play, 2020"))
# print(team_stat("lions", False, 2008, "epa/play"))
# print(player_stat("kurt vollers", 2004, "sack"))
# print(player_stat("kurt vollers", 2004, "tackle"))
# print(player_stat("kurt vollers", 2004, "qb_hit"))
# print(player_stat("fred warner", 2020, "qb_hit"))
# print(player_stat("fred warner", 2020, "fumble"))
# print(player_stat("fred warner", 2020, "fumble_forced"))
# print(player_stat("lamar jackson", 2019, "fumble"))
# print(player_stat("kyler murray", 2019, "fumble_forced"))
# # print(get_players(None))
# print(team_stat("texans", False, 1999, "rush"))
# print(player_stat("julio jones", None, "interception"))
# # print(player_stat("julio jones", 2020, "fumble"))
# print(player_stat("lamar jackson", None, "interception"))
# print(player_stat("tom brady", 2004, "rushing_yards"))
# print(player_stat("marlon humphrey", 2019, "rushing_yards"))
# print(player_stat("luke kuechly", 2016, "sack"))
# print(player_stat("luke kuechly", 2016, "assist_tackle"))
# print(player_stat("ronnie stanley", 2019, "penalty"))
# print(player_stat("ronnie stanley", 2018, "penalty_yards"))
# print(player_stat("lamar jackson", 2018, "fourth_down_converted", "qb"))
# print(player_stat("lamar jackson", 2018, "fourth_down_converted"))
# print(player_stat("lamar jackson", 2018, "fourth_down_converted", "db"))
# print(player_stat("lamar jackson", 2018, "first_down_penalty", None))
# print(player_stat("sam koch", 2018, "cpoe"))
# print(player_stat("saquon barkley", 2018, "cpoe"))
# print(player_stat("marlon humphrey", 2018, "cpoe"))
# print(player_stat("brandon williams", 2018, "cpoe"))
# print(player_stat("mohamed sanu", 2018, "pass_attempt"))
# print(player_stat("jarvis landry", 2020, "incomplete_pass"))
# print(player_stat("tom brady", 2020, "reception"))
# print(player_stat("tarik cohen", 2019, "tot_yards"))
# print(player_stat("deshon elliott", 2020, "fumble_forced"))
# print(player_stat("tarik cohen", 2019, "fumble_forced"))
# print(player_stat("russell wilson", 2020, "sack"))
# print(get_player_id("lamar jackson", 2020, "qb"))
# print(get_player_id("lamar jackson", 2020, "db"))
# print(get_player_id("lamar jackson", 2020, None))
# print(get_player_id("lamar jackson", 2020, None))
# print(get_player_id("lamar jackson", 2020, None))
# print(get_player_id("lamar jackson", 2020, "wr"))
# print(get_player_id("lamar jackson", 2020, None))
# print(get_player_id("tom brady", 2004, None))
# text = "@nfl_statsbot lamar jackson (qb), lamar jackson (db), lamar jackson (wr), lamar jackson (qb), josh allen, josh allen (de), epa/play, 2020"
# msg = ""
# play, team, year, cat, positions = mention_parser(text)
# print("Parameters: ", str(play), str(team), str(year), str(cat), str(positions))
# err = False

# if play == [None] and team == [None]:
#     print("Err 1")
# elif team == [None] and cat == [None]:
#     msg = "That request was invalid! Make sure to use a valid category: https://github.com/rbhushans/nfl-statsbot/blob/master/data/cat_format.csv"
# else:
#     i = 0
#     for p in play:
#         if p == None:
#             break
#         for c in cat:
#             if err:
#                 err = False
#                 break
#             if c is not None and "_allowed" in c:
#                 c = c.replace("_allowed", "")
#             for y in year:
#                 try:
#                     print("Calling stat with", p, y, c, positions[i])
#                     stat = player_stat(p, y, c, positions[i])
#                     i += 1
#                 except Exception as e:
#                     print("Err 2:", e)
#                 if stat == None:
#                     continue
#                 m =  stat + "\n"
#                 if len(msg) + len(m) > 280:
#                     break
#                 msg += m
#                 if "did not play in the NFL" in stat or "rookies from the 2020 NFL season" in stat:
#                     err = True
#                     break
#     for t in team:
#         if t == None:
#             break
#         for c in cat:
#             if c is not None and "_allowed" in c:
#                 off = False
#                 c = c.replace("_allowed", "")
#             else:
#                 off = True
#             for y in year:    
#                 try:                    
#                     stat = team_stat(t, off, y, c)
#                 except:
#                     print("Err 3")
#                 if stat == None:
#                     continue
#                 m =  stat + "\n"
#                 if len(msg) + len(m) > 280:
#                     break
#                 msg += m
# print(msg)
