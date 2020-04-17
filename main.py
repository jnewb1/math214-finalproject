from prediction import run_prediction
from simulation import run_simulation

import networkx as nx
import matplotlib.pyplot as plt

import random

# setup subplots and title of window
fig, ax = plt.subplots(1, 2, num=1, figsize=(10,5))
fig.tight_layout(pad=1.5)
fig.canvas.set_window_title('Eigenvector Centrality - Prediction of Hotspots')

def generate_graph(people, density):
    n = int(people / density * 100)
    c = 2.8
    print(n, c)
    G = nx.erdos_renyi_graph(n, c / n, 10)
    return G


num_nodes = 10 # number of people in the simulation
connections_per_node = 4 # average number of connections that each node has

# create random graph
#G = nx.erdos_renyi_graph(num_nodes, connections_per_node / num_nodes, 10)

people = 17635.0 # number of people
density =  67 # population density

G = generate_graph(people, density)


# calculate node weights https://onlinelibrary.wiley.com/doi/10.1002/jmv.25750
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4944951/ 

weights = {}

for u, v in G.edges():
    G[u][v]['weight'] = 1.0

colors = [(0,G[u][v]['weight'], 0) for u,v in G.edges() ]


# layout for the nodes
pos=nx.spring_layout(G)

# plot the prediction on the left window
left = ax[0]
plt.sca(left)
left.set_title("Prediction")
run_prediction(G, pos, colors)

extent = left.get_tightbbox(renderer = fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted())
fig.savefig("214_slide_pictures/prediction.png", dpi=1000,
    bbox_inches=extent)

# plot the simulation on the right window
right = ax[1]


plt.sca(right)
right.set_title("Simulation")
run_simulation(G, pos, right, fig, colors)

plt.show()
