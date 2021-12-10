import pandas as pd
import itertools

pos_stats = pd.read_csv(
    'tableauData_overall_position_grouped.csv', 
    usecols = [
        'off_player_pos', 'def_player_pos', 'avg_ts_diff', 
        'avg_player_pts_pct_diff', 'avg_team_pts_pct_diff']
).set_index(['off_player_pos', 'def_player_pos'])

offs = ['PG', 'SG', 'SF', 'PF', 'C']
deffs = ['PG', 'SG', 'SF', 'PF', 'C']
matchups = list(itertools.product(offs, deffs))
combos = list(itertools.combinations(matchups, 5))

def is_unique(my_list):
    return len(set(my_list)) == len(my_list)

combos_valid = list(filter(lambda x: is_unique(list(zip(*x))[0]) and is_unique(list(zip(*x))[1]), combos))

matchups = pd.DataFrame(
    {
        v_combo: pos_stats\
        .loc[list(v_combo)][['avg_ts_diff', 'avg_player_pts_pct_diff', 'avg_team_pts_pct_diff']]\
        .mean() 
        for v_combo in combos_valid
    }
).T

matchups = matchups.reset_index()

for col in matchups.columns:
    if not col.startswith("level"):
        continue
    else:
        matchups.loc[:, col] = matchups.loc[:, col].apply(lambda x: x[1])

matchups = matchups.rename(columns={
    "level_0": 'pg_defender', 'level_1': "sg_defender",
    "level_2": "sf_defender", "level_3": "pf_defender",
    "level_4": "c_defender"
}).set_index(["pg_defender", "sg_defender", "sf_defender", "pf_defender", "c_defender"])

# Lower numbers mean better matchups for the defense
matchups = matchups.sort_values('avg_player_pts_pct_diff')

matchups.to_csv('lineup_matchups.csv')