from load_constants import categories, f_categories, teams

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
        return possible[0]

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