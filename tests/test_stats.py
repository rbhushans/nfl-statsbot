import sys

sys.path.append('src/utils')
from stats import player_stat

print(player_stat("kurt vollers", 2004, "sack"))
print(player_stat("lamar jackson", 2021, "sack"))
print(player_stat("travon walker", 2022, "sack"))
