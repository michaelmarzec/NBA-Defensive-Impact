import pandas as pd
import numpy as np

from nba_api.stats.endpoints.leaguedashplayerstats import LeagueDashPlayerStats
import csv



try:
    # get the first player, for the column headers
    print('2020')
    output1 = LeagueDashPlayerStats(last_n_games=0, per_mode_detailed='Totals', season_type_all_star='Regular Season', season='2020-21', measure_type_detailed_defense='Base').get_data_frames()
    df_2020_21 = pd.DataFrame(output1[0])
    df_2020_21['SEASON_ID'] = '22020'
    # print(df_info)
except Exception as e:
    print("error in getting 2020-21 season")
    print("Error occurred: " + str(e))

try:
    # get the first player, for the column headers
    print('2019')
    output2 = LeagueDashPlayerStats(last_n_games=0, per_mode_detailed='Totals', season_type_all_star='Regular Season', season='2019-20', measure_type_detailed_defense='Base').get_data_frames()
    df_2019_20 = pd.DataFrame(output2[0])
    df_2019_20['SEASON_ID'] = '22019'
    # print(df_info)
except Exception as e:
    print("error in getting 2019-20 season")
    print("Error occurred: " + str(e))


try:
    # get the first player, for the column headers
    print('2018')
    output3 = LeagueDashPlayerStats(last_n_games=0, per_mode_detailed='Totals', season_type_all_star='Regular Season', season='2018-19', measure_type_detailed_defense='Base').get_data_frames()
    df_2018_19 = pd.DataFrame(output3[0])
    df_2018_19['SEASON_ID'] = '22018'
    # print(df_info)
except Exception as e:
    print("error in getting 2018-19 season")
    print("Error occurred: " + str(e))


try:
    # get the first player, for the column headers
    print('2017')
    output4 = LeagueDashPlayerStats(last_n_games=0, per_mode_detailed='Totals', season_type_all_star='Regular Season', season='2017-18', measure_type_detailed_defense='Base').get_data_frames()
    df_2017_18 = pd.DataFrame(output4[0])
    df_2017_18['SEASON_ID'] = '22017'
    # print(df_info)
except Exception as e:
    print("error in getting 2017-18 season")
    print("Error occurred: " + str(e))

print('combine')
# append all of the data frames
df_final_stats = df_2020_21.append([df_2019_20,df_2018_19,df_2017_18])

 # output players to file
df_final_stats.to_csv('final_player_stats_v2.csv')
