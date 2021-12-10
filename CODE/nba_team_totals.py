import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashteamstats

# user must update following parameters to manually obtain data for each season. Subsequently, combine the 4 csv files.
	#line 10: season = 2017-18, 2018-19, 2019-20, 2020-21
	#line 11: output['SEASON_ID'] = 22017, 22018, 22019, 22020
	#line 14: output.to_csv('2017_...') .... 2018_, 2019_, 2020_

output = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='PerGame', season_type_all_star='Regular Season', season='2017-18', measure_type_detailed_defense='Base').get_data_frames()[0]
output['SEASON_ID'] = 22017 #, 22018, 22019, 22020


output.to_csv('2017_nba_team_totals_scrape.csv')