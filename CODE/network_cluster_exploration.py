# Make sure to run pip install pyarrow before running Data Import
import networkx as nx
from networkx.algorithms import community

import pandas as pd
import numpy as np
from datetime import datetime
import csv

import community
import collections

import matplotlib.pyplot as plt






with open('nodes.csv', 'r') as nodecsv: # Open the file
    nodereader = csv.reader(nodecsv) # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:] # [1:]



node_names = [n[0] for n in nodes] # Get a list of only the node names

with open('edge_small.csv', 'r') as edgecsv: # Open the file
    edgereader = csv.reader(edgecsv) # Read the csv
    edges = [tuple(e) for e in edgereader][1:] # Retrieve the data

# print('going1')

g = nx.Graph()

g.add_nodes_from(node_names)
g.add_edges_from(edges)

# print('going2')

###
# breaks into three communities
###
communities = community.greedy_modularity_communities(G)
print(communities)



###
# something about it showing maximal ... seems like we might be getting a never ending grouping
###
players = pd.read_csv('nodes.csv', dtype={'id':'Int64','name':'str'})

for x in communities:
    group = np.array(list(x))
    group = pd.DataFrame(group)
    group.columns = ['id']
    group = group.astype('int32')
    ply_names = group.merge(players,left_on = 'id', right_on='id')


cliques = list(nx.find_cliques(G))
print(cliques)



#####
# shows that they're all connected
#####
# print('going')
subs = nx.connected_components(G)
for x in subs:
    print('1')
    print('-'*50)
    print(len(x))


# ### community detection (via python-louvian)###
# # results in 4 groups and not well divided
# ####
partition = community.best_partition(G)
values = [partition.get(node) for node in G.nodes()]
counter=collections.Counter(values)
print(counter)

sp = nx.spring_layout(G)
nx.draw_networkx(G, pos=sp, with_labels=False, node_size=35, node_color=values)
# plt.axes('off')
plt.show()




#### Jaccard Distance: "close if they share common neighbors" #### https://stackoverflow.com/questions/49064611/how-to-find-different-groups-in-networkx-using-python

nn = len(g.nodes)
mat = np.empty((nn, nn), dtype=float)
mat.fill(-100.0)
np.fill_diagonal(mat, -0.0)

preds = nx.jaccard_coefficient(g, g.edges)
print('going3')
for u, v, j in preds:
    mat[int(u),int(v)] = -100 * (1 - j)


from sklearn.cluster import AffinityPropagation

print('going4')


# parameters = {'preference':[-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,-5,-1,0,5,10],'affinity':'precomputed','random_state'=[1]}

# pref = [-100,-95, -90, -80,-70,-60,-50,-40,-30,-20,-10,-5,-1,0,5,10]


### Preferences ###
#-85:1083
#-95: 1039
#-97.5: 1034
#-98.75: 1031
#-99.5: 1029
# -99.9: 1027
# -99.95: 1027
# -99.99: 1027
# -99.99999: 1027
# -99.999999999999:1032
# -99.9999999999999: 849
# -99.99999999999995: 387
# -99.99999999999997: 217
# -99.999999999999975: 217
# -99.999999999999977: 217
# -99.9999999999999786: 217
# -99.9999999999999788: 1
# -99.999999999999979: 1
# -99.99999999999998: 1
# -99.99999999999999: 1
# -99.9999999999999999: 1
# -99.9999999999999999999: 1
#-100: 1


np.median(mat)
af = AffinityPropagation(preference=-99.9999999999999787,affinity="precomputed",random_state=1) # preference=-100, 
lab = af.fit_predict(mat)
print('num_unique:')
print(len(np.unique(lab)))

