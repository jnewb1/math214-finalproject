import networkx as nx 
import matplotlib.pyplot as plt 
  
# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.eigenvector_centrality.html
def run_prediction(G, pos):
    print("Running Prediction")
    # calculate eigenvector_centrality
    centrality = nx.eigenvector_centrality(G, weight="weight")

    # find scale for the "redness" of each node
    scale = 1/max(centrality.values())

    labels = {}
    for node in range(len(centrality.items())):
        # setup labels for each node with centrality 
        labels[node] = "{:0.2f}".format(centrality[node])

        # draw node on the graph
        nx.draw_networkx_nodes(G,pos,
            nodelist=[node],
            node_color=[(centrality[node]*scale ,0,0)],
            node_size=100,
        )

    # draw all edges on the graph
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

    # draw all labels on the graph
    nx.draw_networkx_labels(G,pos,labels,font_size=4, font_color="#FFFFFF")
    print("Finished Prediction")
    

