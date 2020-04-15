import networkx as nx 
import matplotlib.pyplot as plt 

from epydemic import *

# https://pyepydemic.readthedocs.io/en/latest/tutorial/build-sir.html
# COVID-19 Recovery Article https://time.com/5810454/coronavirus-immunity-reinfection/
class SIR(CompartmentedModel):

    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    REMOVED = 'R'
    DEAD = 'D'


    # the model parameters
    P_INFECTED = 'pInfected'
    P_INFECT = 'pInfect'
    P_REMOVE = 'pRemove'
    P_INFECT_FROM_RECOVERED = 'pInfectRecovered'
    P_DEAD_FROM_INFECTED = 'pDeadInfected'

    SI = 'SI'
    RI = 'RI'

    def build( self, params):
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]
        pInfectRecovered = params[self.P_INFECT_FROM_RECOVERED]
        pDeadInfected = params[self.P_DEAD_FROM_INFECTED]

        self.addCompartment(self.INFECTED,pInfected)
        self.addCompartment(self.REMOVED, 0.0)
        self.addCompartment(self.SUSCEPTIBLE, 1- pInfected)
        self.addCompartment(self.DEAD, 0.0)

        self.trackNodesInCompartment(self.INFECTED)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackEdgesBetweenCompartments(self.REMOVED, self.INFECTED, name=self.RI)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.RI, pInfectRecovered, self.infect_recovered)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)
        self.addEventPerElement(self.INFECTED, pDeadInfected, self.dead)

    def infect( self, t, e ):
        (n, m) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)
        update_gui(self)

    def infect_recovered( self, t, e ):
        (n, m) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)
        update_gui(self)

    def remove( self, t, n ):
        self.changeCompartment(n, self.REMOVED)
        update_gui(self)
    
    def dead( self, t, n):
        self.changeCompartment(n, self.DEAD)
        update_gui(self)
    
G_ = None
pos_ = None
bbox_ = None
fig_ = None

x = 0

def update_gui(m):

    global x

    susceptible = []
    recovered = []
    infected = []
    dead = []

    if('S' in m.compartments()):
        susceptible  = m.compartment('S')
    if('R' in m.compartments()):
        recovered = m.compartment('R')
    if('I' in m.compartments()):    
        infected = m.compartment('I')
    if('D' in m.compartments()):    
        dead = m.compartment('D')
    

    nodes = {}

    # get all nodes that are susceptible, recovered, or infected
    for node in susceptible:
        nodes[node] = "S"
    for node in recovered:
        nodes[node] = "R"
    for node in infected:
        nodes[node] = "I"
    for node in dead:
        nodes[node] = "D"
    
    print(dead)
    
    labels = {}    

    for node in nodes:
        # setup labels for each node with centrality 
        labels[node] = ""

        # draw node on the graph
        nx.draw_networkx_nodes(G_,pos_,
            nodelist=[node],
            node_color=[( nodes[node] == "D", nodes[node] == "R", nodes[node] == "I" )],
            node_size=100,
        )
    
    plt.draw()

    extent = ax_.get_tightbbox(renderer = fig_.canvas.get_renderer()).transformed(fig_.dpi_scale_trans.inverted())
    fig_.savefig("/mnt/c/Users/justin/Desktop/214_slide_pictures/" + str(x) + ".png", dpi=500,
    bbox_inches=extent)
    x+=1

def run_simulation(G, pos, ax, fig):
    global G_
    global pos_
    global ax_
    global fig_

    G_ = G
    pos_ = pos
    ax_ = ax
    fig_ = fig

    print("Running Simulation")
    param = dict()
    # infected by anther infected
    param[SIR.P_INFECT] = .5

    # being removed when infected
    # Recovery Rate: https://www.fatherly.com/news/recovery-rate-coronavirus/
    param[SIR.P_REMOVE] = 0.3
    
    # starting infected
    param[SIR.P_INFECTED] = 0.05

    # infected again after recovered
    param[SIR.P_INFECT_FROM_RECOVERED] = 0.05

    # dead after infected
    # Mortality Rate: https://www.statnews.com/2020/03/16/lower-coronavirus-death-rate-estimates/
    # Age 15-44: Worst Case: 1.3%, Best Case: 0.1%, Average Case: 0.5%
    # Age 45-64: Worst Case: 1.1%, Best Case: 0.5% 
    param[SIR.P_DEAD_FROM_INFECTED] = .03

    # create a model and a dynamics to run it
    m = SIR()                      # the model (process) to simulate
    e = StochasticDynamics(m, G)   # use stochastic (Gillespie) dynamics
    
      # draw all edges on the graph
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)


    # set the parameters we want and run the simulation
    rc = e.set(param).run()
    

    
    print("Finished Simulation")

