# NFL Statsbot

## Description

The NFL Statsbot is a Twitter bot [(@nfl_statsbot)](https://twitter.com/nfl_statsbot) used to easily obtain any season or career statistic of any player or team since 1999. The football statistics are generated using play by play data from [NFLFastR](https://github.com/mrcaseb/nflfastR) with wrapper functions from [NFLFastPy](https://github.com/fantasydatapros/nflfastpy). For descriptions/definitions of statistics, the [NFLFastR documentation](https://cran.r-project.org/web/packages/nflfastR/nflfastR.pdf) can be referenced.

## Functionality

The Twitter bot currently has three points of main functionality:

- **Random Player/Team Statistics**

  The bot spits out a random statistic of one of the thousands of NFL players since 1999. For all possible statistics, the first column of cat_format.csv in the data folder can be referenced (offense only statistics can be found in off_cats.txt).

- **Statistic Requests**

  Any twitter user can request a statistic by mentioning it in a tweet. Statistics can be requested by separating parameters by commas. Parameters can be player names, team names (abbreviation, city, mascot, or full name), statistical categories, and years. The request MUST have at least one player name or team name and a category. If no years are provided, then the bot will use career statistics (since 1999). The bot currently requires a statistical category for players, but future iterations will introduce primary statistics for each position to use when a category is not provided. If no category is provided for a team statistic, a summary of that team's statistics are included:

  - Passing yards
  - Rushing yards
  - Touchdowns
  - Offense EPA/play
  - Forced Fumbles
  - Interceptions
  - Sack
  - Solo Tackles
  - Defense EPA/play

  For all possible statistics, the first column of cat_format.csv in the data folder can be referenced (offense only statistics can be found in off_cats.txt). Requests are cases insensitive. A player's full name must be used (e.g. Joe Flacco and not Flacco).

  Sample Requests:
  | Tweet | Result |
  | ----- | ------ |
  | @nflstatsbot ravens, 2017, 2018, 2019, 2020, touchdown | The Baltimore Ravens had 38 touchdowns in 2017. <br> The Baltimore Ravens had 38 touchdowns in 2018. <br> The Baltimore Ravens had 59 touchdowns in 2019. <br> The Baltimore Ravens had 54 touchdowns in 2020. |
  | @NFLStatsBot lamar jackson, epa, 2019 | Lamar Jackson (QB) had 192.9113 EPA in 2019. |
  | @NFLstatsbot bears, ravens, 2000, passing yards | The Chicago Bears had 3005 passing yards in 2000. <br> The Baltimore Ravens had 3102 passing yards in 2000.
  | @NFLStatsbot 2004, ED REED, interceptions | Ed Reed (SS) had 9 interceptions in 2004. |
  | @nflstatsbot ravens, 2019 | B̲a̲l̲t̲i̲m̲o̲r̲e̲ ̲R̲a̲v̲e̲n̲s̲ ̲-̲ ̲2̲0̲1̲9̲:̲ <br> Passing Yards: 3350 <br> Rushing Yards: 3287 <br> Touchdowns: 59 <br> Offense EPA/Play: 200.1676 <br> Forced Fumbles: 15<br> Interceptions: 13 <br> Sacks: 37 <br> Solo Tackles: 580 <br> Defense EPA/Play: -87.0218 |

- **Player/Team Recognition**

  When major NFL accounts send a tweet including a player name or team name, the bot will reply to it with a random statistic pertaining to that player or team (if multiple players or teams are present in the tweet only one will be chosen at random).

## Caveats

- For a player that never played a game in the NFL (but was on a team in some capacity at some point), the bot will state they never played in the NFL
- Some categories were only introduced in recent years, and as a result will display as 0 for these older statistics.
- Full career stats will take some time to load.
- For defensive team stats, adding "allowed" to the end of any stat will obtain the defensive statistic (e.g. if the goal is to obtain the number of passing yards the ravens defense allowed in 2020, the parameters of the tweet would include: ravens, 2020, passing yards allowed)

## Future Functionality

- Multiple Players/Teams Graphs - Include a data visualization comparing multiple players in both the random tweets and statistic requests.
- Smart Category Selection - Random statistics will only select categories that are valid in the random year selected.
- Week Option - The bot currently only supports Season and Career stats, but a week option will be included in the near future.
- Playoff Option - The bot currently only support regular season stats, but a playoff option will be included in the near future.
