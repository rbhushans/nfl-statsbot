import re
from load_constants import teams, categories, years
from load_data import get_full_roster
from converters import convert_category
from utils import is_int

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
    roster_df = get_full_roster(['player_name', 'first_name', 'last_name'])
    player_names, first, last = (roster_df['player_name'].str.lower().to_numpy(),
                                roster_df['first_name'].str.lower().to_numpy(),
                                roster_df['last_name'].str.lower().to_numpy())
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

# parses a request tweet for players, teams, years and categorys
def mention_parser(tweet):
    print(tweet)
    at_tag = re.compile("@([a-zA-Z0-9]|[_])*", re.IGNORECASE)
    punctuation = re.compile("[!?\\-@:\n]")
    if tweet[0] == '.':
        tweet = tweet[1:]
    #parse a more specific and targeted tweet and return a player/team, year, category
    category = []
    player = []
    team = []
    year = []
    positions = []
    roster_df = get_full_roster(['player_name', 'first_name', 'last_name'])
    players, first, last = (roster_df['player_name'].str.lower().to_numpy(),
                                roster_df['first_name'].str.lower().to_numpy(),
                                roster_df['last_name'].str.lower().to_numpy())
    tweet = at_tag.sub('', tweet)
    tweet = punctuation.sub('', tweet)
    tweet = tweet.replace("'", "")
    while len(tweet) > 0 and tweet[0] == ' ':
        tweet = tweet[1:]
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
        c = "default"
        if w[-1] == 's':
            c = w[:-1]
        cat1 = convert_category(w)
        cat2 = convert_category(c)
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