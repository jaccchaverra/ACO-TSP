import random
from graph import Graph
from colony import Colony
"""
Ant contains information about how ants can act manipulating the cost matrix and pheromoneSpace status based on its colony parameter.
"""
class Ant(object):
    def __init__(self, colony: Colony, graph: Graph):
        """
        :param colony: Contains the colony parameters of the ant.
        :param graph: Contains the graph of the problem.
        :param totalCost: Total cost acumulated on the ant tour.
        :param tabu: Contains the cities visited for the ant.
        :param deltaPheromone: Contains the pheromone changes generated by each Ant over each edge on the graph.
        :param allowedSites
        :param currentSite
        :param eta: Contains the visibility level for each edge on the graph.
        """
        self.colony = colony
        self.graph = graph
        self.totalCost = 0.0
        self.tabu = []
        self.deltaPheromone = []
        self.allowedSites = [i for i in range(graph.totalSites)]
        self.eta = [[1 / graph.costMatrix[i][j] if i != j else 0 for j in range(graph.totalSites)] for i in range(graph.totalSites)]
        originSite = random.randint(0, graph.totalSites - 1)
        self.tabu.append(originSite)
        self.currentSite = originSite
        self.allowedSites.remove(originSite)
    
    def nextMovement(self):
        denominator = 0
        for site in self.allowedSites:
            denominator += self.graph.pheromoneSpace[self.currentSite][site] ** self.colony.alpha * self.eta[self.currentSite][site] ** self.colony.beta
        probabilities = [0]*self.graph.totalSites
        
        for site in self.allowedSites:
            probabilities[site] = self.graph.pheromoneSpace[self.currentSite][site] ** self.colony.alpha * self.eta[self.currentSite][site] ** self.colony.beta / denominator
            
        #Select next site according by probability each site.
        nextSite = 0
        randomSite = random.random()
        for site, probability in enumerate(probabilities):
            randomSite -= probability
            if randomSite <= 0:
                nextSite = site
                break
        self.allowedSites.remove(nextSite)
        self.tabu.append(nextSite)
        self.totalCost += self.graph.costMatrix[self.currentSite][nextSite]
        self.currentSite = nextSite
    
    def updateDeltaPheromone(self):
        self.deltaPheromone = [[0] * self.graph.totalSites] * self.graph.totalSites
        for step in range(len(self.tabu)-1):
            i = self.tabu[step]
            j = self.tabu[step + 1]
            if self.colony.scheme == 0: #ant-ranking system
                self.deltaPheromone[i][j] = self.colony.Q / self.totalCost
            elif self.colony.scheme == 1: #ant-colony system
                self.deltaPheromone[i][j] = self.colony.Q
            elif self.colony.scheme == 2: #ant-elitist system
                self.deltaPheromone[i][j] = self.colony.Q / self.graph.costMatrix[i][j]

