from bnetbase import Factor, Variable
class DAG:
    def __init__(self, name, nodes, edges, factor) -> None:
        """Create a DAG that represents the given information """
        self.name = name
        self.Nodes = list(nodes) # list of nodes in the graph
        self.Edges = list(edges) # list of edges in the graph
        self.Factors = list(factor) # list of factors representing probability
                                    # distribution in the graph 

    def add_edges(self,var1, var2, endpoint = None):
        e = Edge(var1, var2, endpoint)
        self.Edges.append(e)

    def remove_edges(self, var1, var2):
        for e in self.Edges:
            if var1 in e.get_vertices() and var2 in e.get_vertices():
                self.Edges.remove(e)

    def factors(self):
        return list(self.Factors)
    
    def nodes(self):
        return list(self.Nodes)
    
    def edges(self):
        return list(self.Edges)
    
class Node(Variable):       
    def __init__(self, name, domain=[], neighbors=[]):
        '''Create a node object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                #text name for variable
        self.dom = list(domain)         #Make a copy of passed domain
        self.neighbors = list(neighbors) #list of neighbors to this node 
        self.evidence_index = 0         #evidence value (stored as index into self.dom)
        self.assignment_index = 0       #For use by factors. We can assign variables values
                                        #and these assigned values can be used by factors
                                        #to index into their tables
    
    def add_neighbors(self, n):
        '''Add new neighbors. n should be a list.'''
        for val in n: self.neighbors.append(val)

    def remove_neighbors(self, n):
        '''Remove neighbors. n should be a list.'''
        for val in n: self.neighbors.remove(val)

class Edge:
    def __init__(self, var1, var2, end = None) -> None:
        self.endpoints = [var1, var2]
        self.arrow = end # end represents which variable the arrow points to, 
                        # if the edge does not have direction the end would just be none.
    
    def get_vertices(self):
        """Get 2 endpoints of an edge"""
        return self.endpoints
    
    def add_endpoint(self,var):
        """Adding arrow to this edge"""
        self.arrow = var
    
    def remove_endpoint(self):
        """Make the edge undirected"""
        self.arrow = None

    def __repr__(self):
        '''string to return when evaluating the object'''
        if self.arrow is None:
            return("{}".format(self.endpoints[0]) + 
                   "------" + "{}".format(self.endpoints[1]))
        else:
            if self.endpoints[0] == self.arrow:
                return("{}".format(self.endpoints[1]) + 
                   "----->" + "{}".format(self.endpoints[0]))
            else:
                return("{}".format(self.endpoints[0]) + 
                   "----->" + "{}".format(self.endpoints[1]))