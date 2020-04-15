import networkx as nx 
  
#importing the matplotlib library for plotting the graph 
import matplotlib.pyplot as plt 
  
fig = plt.gcf()
fig.canvas.set_window_title('Random Graph + Eigenvector Centrality')

# random graph

G = nx.erdos_renyi_graph(20, 0.2, 10) 

# calculate eigenvector_centrality
centrality = nx.eigenvector_centrality(G)

pos=nx.spectral_layout(G)

# setup labels for graph
labels = {}

for node in range(len(centrality.items())):
    nx.draw_networkx_nodes(G,pos,
                        nodelist=[node],
                        node_color=[(min(centrality[node]*2, 1) ,0,0)],
                        node_size=100,
                    )
    labels[node] = "{:0.2f}".format(centrality[node])

# edges
nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

# some math labels
nx.draw_networkx_labels(G,pos,labels,font_size=4, font_color="#FFFFFF")

plt.show()

