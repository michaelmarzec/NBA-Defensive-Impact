import pandas as pd
import numpy as np
from nba_api.stats.endpoints.commonallplayers import CommonAllPlayers
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
import csv

### Obtain player IDs from players.csv file ####
df_ids = pd.read_csv('players.csv')
# print(df_ids.head(10))

# select the players active from 2015 on
# and put the id's into a list to loop through
mask = df_ids['TO_YEAR'].values >= 2015
df_ids = df_ids[mask]
id_list = df_ids['PERSON_ID'].tolist()
# print(len(id_list))

try:
    # get the first player, for the column headers
    pid = id_list[0]
    output_list_info = CommonPlayerInfo(player_id=pid).get_data_frames()
    df_info = pd.DataFrame(output_list_info[0])
    df_info.drop(index=df_info.index[0], 
            axis=0, 
            inplace=True)
    # print(df_info)
except Exception as e:
    print("error in getting first player")
    print("Error occurred: " + str(e))


try:
# get all of the players
# it will pass back up to 100 at a time
    for id in id_list[0:1200]:   # 1125 players from 2015 season on
        pid=str(id)
        output_list_info = CommonPlayerInfo(player_id=pid).get_data_frames()
        df = pd.DataFrame(output_list_info[0])
        df_info = df_info.append(df)
        print(pid)

   

except Exception as e:
    print("error in getting full players")
    print("Error occurred: " + str(e))

    
 # output players to file
df_info.to_csv('player_info.csv')

