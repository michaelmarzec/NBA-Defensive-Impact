import pandas as pd

years = [str(x) for x in list(range(2017, 2022))]
dfs = {year: pd.read_csv(f'../Raw Data Input Files/bball_ref{year}.csv', usecols=['Player', 'Pos']) for year in years}

player_pos = pd.concat(dfs).reset_index(drop=True)
player_pos.Player = player_pos.Player.str.split('\\').apply(lambda x: x[0] if isinstance(x, list) else None)
player_pos = player_pos.loc[player_pos.Player.notnull()]

# Take most common position per player
player_pos = player_pos.groupby('Player').agg(lambda x: x.value_counts().index[0]).reset_index()

replace_dict = {
    'ć': 'c', 'Ş': 'S', 'ü': 'u', 'ã': 'a', 'Ž': 'Z', 'ž': 'z', 
    'č': 'c', 'ņ': 'n', 'í': 'i', 'ā': 'a', 'Š': 'S',
    'ö': 'o', 'ū': 'u', 'é': 'e', 'İ': 'I', 'ó': 'o', 'ģ': 'g',
    'ê': 'e', 'š': 's', 'á': 'a', 'ò': 'o', 'è': 'e',
    'ý': 'y', 'Č': 'C', 'Á': 'A', 'Ö': 'O', 'ş': 's', 'ı': 'i'


}

for special, reg in replace_dict.items():
    player_pos.Player = player_pos.Player.str.replace(special, reg)
    

# these players are missing so add them manually
missing_players = {
'Andrew White III': 'SF',
 'Brian Bowen II': 'SF',
 'C.J. Wilcox': 'SG',
 'CJ Miles': 'SG',
 'Charlie Brown Jr.': 'SG',
 'DJ Stephens': 'SF',
 'Danuel House Jr.': 'SF',
 'Harry Giles III': 'PF',
 'JJ Redick': 'SG',
 'JR Smith': 'SG',
 'James Ennis III': 'SF',
 "Johnny O'Bryant III": 'C',
 'Juancho Hernangomez': 'PF',
 'KJ Martin': 'SF',
 'Kevin Knox II': 'SF',
 'Lonnie Walker IV': 'SG',
 'Marcus Morris Sr.': 'PF',
 'Matt Williams Jr.': 'SG',
 'Michael Frazier II': 'SG',
 'Mitchell Creek': 'SF',
 'Otto Porter Jr.': 'SF',
 'RJ Hunter': 'SG',
 'Robert Williams III': 'C',
 'Robert Woodard II': 'SF',
 'Vincent Edwards': 'SF',
 'Vincent Hunter': 'PF',
 'Wade Baldwin IV': 'PG',
 'Wes Iwundu': 'SF'
}
missing_pos = pd.Series(missing_players).reset_index().rename(columns={'index': 'Player', 0: 'Pos'})
player_pos = pd.concat([player_pos, missing_pos])
    
player_pos.to_csv('../Final Raw Data Files/player_positions.csv', index=False)
