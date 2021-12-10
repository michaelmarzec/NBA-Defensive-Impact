import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_parquet('../Final Raw Data Files/grouped_player_data.parquet')\
.sort_values(['off_player_name', 'def_player_name']).set_index('off_player_name')

# Get per min
data.matchup_player_pts = data.matchup_player_pts / data.matchup_min
data.matchup_team_pts = data.matchup_team_pts / data.matchup_min

# Filter out short matchups and no shots taken (so ts% is not known)
data = data.loc[(data.matchup_min > 1) & (data.matchup_ts.notnull())]

# Only take columns we need
data = data[
    ['def_player_name', 'off_player_pos', 'def_player_pos', 'matchup_min', 
     'matchup_player_pts', 'matchup_team_pts', 'matchup_ts', 'avg_team_pts', 
     'off_player_min', 'off_player_pts', 'off_player_efg', 'off_player_ts']
]

# Get mu and sigma per offensive player, stat
avgs = data.groupby('off_player_name')[['matchup_player_pts', 'matchup_team_pts', 'matchup_ts']].mean()
stds = data.groupby('off_player_name')[['matchup_player_pts', 'matchup_team_pts', 'matchup_ts']].std()

# impact = (x_off_stat - mu_off_stat) / sigma_off_stat
impacts = (data[['matchup_player_pts', 'matchup_team_pts', 'matchup_ts']] - avgs) / stds
impacts.columns = 'impact_' + impacts.columns

# Add impact
data = pd.concat([data.reset_index(drop=True), impacts.reset_index()], 1)

# Add offensive player average, stdev
avgs.columns = 'avg_' + avgs.columns
stds.columns = 'std_' + stds.columns
avgs = avgs.reset_index()
stds = stds.reset_index()
data = data.merge(avgs, on = 'off_player_name', how='inner').merge(stds, on='off_player_name', how='inner')

# Drop those with null impacts (becuase divide by 0)
data = data[~data.loc[:, data.columns.str.startswith('impact_')].isnull().any(1)]

# Load in heights and weights
ends = ['1', '1a', '1b', '1c']
player_info = pd.concat(
    [
        pd.read_csv(f'../Raw Data Input Files/player_info_{end}.csv')[
            ['DISPLAY_FIRST_LAST', 'HEIGHT', 'WEIGHT']
        ] 
        for end in ends
    ]
)
player_info = player_info.loc[player_info.HEIGHT.apply(lambda x: isinstance(x, str))]
player_info['height'] = player_info.HEIGHT.apply(lambda x: 12*int(x.split('-')[0]) + int(x.split('-')[1]))
player_info['weight'] = player_info.WEIGHT
player_info['player_name'] = player_info.DISPLAY_FIRST_LAST
player_info = player_info[['height', 'weight', 'player_name']]

# From perspective of offensive and defense
player_info_off = player_info.copy()
player_info_off.columns = "off_" + player_info_off.columns
player_info_def = player_info.copy()
player_info_def.columns = "def_" + player_info_def.columns

data = data\
.merge(player_info_off, on='off_player_name', how='inner')\
.merge(player_info_def, on='def_player_name', how='inner')

data = data.set_index(['def_player_name', 'off_player_name'])
data.to_parquet('../Final Raw Data Files/eda_data.parquet')
