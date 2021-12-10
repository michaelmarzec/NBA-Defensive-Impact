import pandas as pd
import numpy as np

import csv


### Obtain player IDs from players.csv file ####
df_start_stats_2017 = pd.read_csv('2017_2018_player_stats.csv',encoding='ANSI')
df_tot_2017 = df_start_stats_2017.loc[ (df_start_stats_2017['Tm'].values == 'TOT') ]
tot_list_2017 = df_tot_2017['Player'].tolist()
df_final_2017 = df_start_stats_2017[~df_start_stats_2017['Player'].isin(tot_list_2017)]
df_final_2017 = df_final_2017.append(df_tot_2017)


df_adv_stats_2017 = pd.read_csv('2017_2018_player_stats_advanced.csv',encoding='ANSI')
df_adv_tot_2017 = df_adv_stats_2017.loc[ (df_adv_stats_2017['Tm'].values == 'TOT') ]
tot_adv_list_2017 = df_adv_tot_2017['Player'].tolist()
df_final_adv_2017 = df_adv_stats_2017[~df_adv_stats_2017['Player'].isin(tot_adv_list_2017)]
df_final_adv_2017 = df_final_adv_2017.append(df_adv_tot_2017)


df_final_2017 = pd.merge(df_final_2017, df_final_adv_2017, on='Player')
df_final_2017['SEASON_ID'] = '22017'


df_start_stats_2018 = pd.read_csv('2018_2019_player_stats.csv',encoding='ANSI')
df_tot_2018 = df_start_stats_2018.loc[ (df_start_stats_2018['Tm'].values == 'TOT') ]
tot_list_2018 = df_tot_2018['Player'].tolist()
df_final_2018 = df_start_stats_2018[~df_start_stats_2018['Player'].isin(tot_list_2018)]
df_final_2018 = df_final_2018.append(df_tot_2018)

df_adv_stats_2018 = pd.read_csv('2018_2019_player_stats_advanced.csv',encoding='ANSI')
df_adv_tot_2018 = df_adv_stats_2018.loc[ (df_adv_stats_2018['Tm'].values == 'TOT') ]
tot_adv_list_2018 = df_adv_tot_2018['Player'].tolist()
df_final_adv_2018 = df_adv_stats_2018[~df_adv_stats_2018['Player'].isin(tot_adv_list_2018)]
df_final_adv_2018 = df_final_adv_2018.append(df_adv_tot_2018)

df_final_2018 = pd.merge(df_final_2018, df_final_adv_2018, on='Player')
df_final_2018['SEASON_ID'] = '22018'

df_start_stats_2019 = pd.read_csv('2019_2020_player_stats.csv',encoding='ANSI')
df_tot_2019 = df_start_stats_2019.loc[ (df_start_stats_2019['Tm'].values == 'TOT') ]
tot_list_2019 = df_tot_2019['Player'].tolist()
df_final_2019 = df_start_stats_2019[~df_start_stats_2019['Player'].isin(tot_list_2019)]
df_final_2019 = df_final_2019.append(df_tot_2019)

df_adv_stats_2019 = pd.read_csv('2019_2020_player_stats_advanced.csv',encoding='ANSI')
df_adv_tot_2019 = df_adv_stats_2019.loc[ (df_adv_stats_2019['Tm'].values == 'TOT') ]
tot_adv_list_2019 = df_adv_tot_2019['Player'].tolist()
df_final_adv_2019 = df_adv_stats_2019[~df_adv_stats_2019['Player'].isin(tot_adv_list_2019)]
df_final_adv_2019 = df_final_adv_2019.append(df_adv_tot_2019)

df_final_2019 = pd.merge(df_final_2019, df_final_adv_2019, on='Player')
df_final_2019['SEASON_ID'] = '22019'


df_start_stats_2020 = pd.read_csv('2020_2021_player_stats.csv',encoding='ANSI')
df_tot_2020 = df_start_stats_2020.loc[ (df_start_stats_2020['Tm'].values == 'TOT') ]
tot_list_2020 = df_tot_2020['Player'].tolist()
df_final_2020 = df_start_stats_2020[~df_start_stats_2020['Player'].isin(tot_list_2020)]
df_final_2020 = df_final_2020.append(df_tot_2020)

df_adv_stats_2020 = pd.read_csv('2020_2021_player_stats_advanced.csv',encoding='ANSI')
df_adv_tot_2020 = df_adv_stats_2020.loc[ (df_adv_stats_2020['Tm'].values == 'TOT') ]
tot_adv_list_2020 = df_adv_tot_2020['Player'].tolist()
df_final_adv_2020 = df_adv_stats_2020[~df_adv_stats_2020['Player'].isin(tot_adv_list_2020)]
df_final_adv_2020 = df_final_adv_2020.append(df_adv_tot_2020)

df_final_2020 = pd.merge(df_final_2020, df_final_adv_2020, on='Player')
df_final_2020['SEASON_ID'] = '22020'



frames = [df_final_2017,df_final_2018,df_final_2019, df_final_2020]
df_final_all = pd.concat(frames)

df_final_all.to_csv('stats_final.csv')