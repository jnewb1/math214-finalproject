import networkx as nx 
import matplotlib.pyplot as plt 

from epydemic import *

class SIR(CompartmentedModel):

    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    REMOVED = 'R'


    # the model parameters
    P_INFECTED = 'pInfected'
    P_INFECT = 'pInfect'
    P_REMOVE = 'pRemove'

    SI = 'SI'

    def build( self, params ):
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)
        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)

        self.trackNodesInCompartment(self.INFECTED)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

    def infect( self, t, e ):
        (n, m) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)

    def remove( self, t, n ):
        self.changeCompartment(n, self.REMOVED)
    


    

def run_simulation(G, pos):
    param = dict()
    param[SIR.P_INFECT] = .3
    param[SIR.P_REMOVE] = 0.5
    param[SIR.P_INFECTED] = 0.05

    # create a model and a dynamics to run it
    m = SIR()                      # the model (process) to simulate
    e = StochasticDynamics(m, G)   # use stochastic (Gillespie) dynamics

    # set the parameters we want and run the simulation
    rc = e.set(param).run()

    susceptible  = m.compartment('S')
    recovered = m.compartment('R')
    infected = m.compartment('I')

    nodes = {}

    
    for node in susceptible:
        nodes[node] = "S"
    for node in recovered:
        nodes[node] = "R"
    for node in infected:
        nodes[node] = "I"
    
    labels = {}    

    for node in nodes:
        # setup labels for each node with centrality 
        labels[node] = ""

        # draw node on the graph
        nx.draw_networkx_nodes(G,pos,
            nodelist=[node],
            node_color=[(nodes[node] == "R",0,0)],
            node_size=100,
        )

    # draw all edges on the graph
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

    # draw all labels on the graph
    nx.draw_networkx_labels(G,pos,labels,font_size=4, font_color="#FFFFFF")

