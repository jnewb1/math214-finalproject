import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np

import custom
  
# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.eigenvector_centrality.html
def run_prediction(G, pos, weights):
    print("Running Prediction")
    # calculate eigenvector_centrality
    centrality = custom.eigenvector_centrality(G, weight="weight", max_iter=1000)

    f = open("214_slide_pictures/matrix.txt", "w")
    f.write("\\begin{bmatrix}\n")
    for x in centrality:
        f.write("{:0.3f}\\\\\n".format(centrality[x]))
    f.write("\\end{bmatrix}\n")
    f.write("\n\n")
    f.write("\\begin{bmatrix}\n")
    for u in G.nodes():
        for v in G.nodes():
            if((u,v) in G.edges()):
                w = G[u][v]["weight"]
            else:
                w = 0
            f.write("{:1.0f} & ".format(w))
            
        f.write("\n")
    f.write("\\end{bmatrix}\n")

    A = nx.adjacency_matrix(G).toarray()
    c = list(centrality.values())
    b = np.dot(A, c)

    eigenvalue_valid = 0
    eigenvalue_count = 0

    for y in range(len(b)):
        if(b[y] > 0.0001 and c[y] > 0.0001):
            eigenvalue_valid += b[y] / c[y]
            eigenvalue_count += 1
        print("{:0.3f} {:0.3f}".format(b[y], c[y]))
    
    print(eigenvalue_valid / eigenvalue_count)
    

    

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
            node_size=20,
        )
    # draw all edges on the graph
    nx.draw_networkx_edges(G,pos,width=1.0, edge_color=weights)

    # draw all labels on the graph
    nx.draw_networkx_labels(G,pos,labels,font_size=4, font_color="#FFFFFF")
    print("Finished Prediction")
    

