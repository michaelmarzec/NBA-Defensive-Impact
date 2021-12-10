#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime


# Loading in data
# df = pd.read_csv('final_joined_base_data.csv.csv', low_memory=False)
df = pd.read_parquet('final_joined_base_data.parquet', engine='pyarrow')
df.head(5)

# Convert MATCH_UP min column to seconds as integer
def convert_to_minutes(value):
#     if len(value) <= 5:
#         minutes, seconds = value.split(':')
#     else:
#         minutes, seconds, zeros = value.split(':')
#     return int(minutes) + int(seconds) /60

    return int(round(value*60))

    
df['matchup_min'] = df['matchup_min'].apply(convert_to_minutes)


# Build Directed Graph using networkx function
G = nx.DiGraph()
# Create list of tuples with each tuple containing Offensive Player IDs and Player Names (dictionary form)
# This way when we add nodes to our Graph, they will already have labels
nodes_list = []
for idx in df.index:
    name_label = {"Player Name": str(df.loc[idx,'off_player_name'])}
#     position_label = {"Position": str(df.loc[idx,'off_player_pos'])}
    node = int(df.loc[idx,'off_player_id'])
    name_list = [node, name_label]
    nodes_list.append(name_list)
    
# Add in Offensive Player IDs from dataset as nodes. Note that function add_nodes_from only adds in distinct values
G.add_nodes_from(nodes_list)
# G.nodes()

#Add position attribute to each node
unique_df = pd.DataFrame(df, columns = ["off_player_id","off_player_pos"])
unique_df = unique_df.drop_duplicates()
position_labels = {}
for idx in unique_df.index:
    position = {"Position": str(df.loc[idx,'off_player_pos'])}
    position_labels[int(unique_df.loc[idx,'off_player_id'])] = position

nx.set_node_attributes(G, position_labels)

# Add relationship between Offensive Player IDs and Defensive Player IDs as edges to graph
# Weight each edge based on MATCHUP_MIN
edges_list = []
for idx in df.index:
    source = int(df.loc[idx,'off_player_id'])
    target = int(df.loc[idx,'def_player_id'])
    weight = round(float(df.loc[idx,'matchup_min']),4)
    
    edge = (source,target,weight)
    edges_list.append(edge)
    
G.add_weighted_edges_from(edges_list)


# Export Edges File
nx.write_weighted_edgelist(G, "weighted.edgelist.csv", delimiter = ",")
# Export Nodes File
nodes_path = "nodes.csv"
nodes_file = open(nodes_path, 'w', encoding='utf-8')
nodes_file.write("id,name,position" + "\n")
names_list = []
position_list = []
for value in list(G.nodes(data=True)):
    names_list.append(value[1].get('Player Name'))
    position_list.append(value[1].get('Position'))

# print(names_list) 
del names_list[-1]

# print(G.nodes)
nodes = list(G.nodes(data=True))
del nodes[-1]

# for count,value in enumerate(list(G.nodes(data=True))):
for count,value in enumerate(nodes):
    nodes_file.write( str(value[0]) + "," + str(names_list[count]) +  "," +str(position_list[count]) + "\n")
nodes_file.close()


# In[ ]:




