from dag import DAG, Node, Edge
from bnetbase import Factor
import itertools
def IC(varlist, factors):
    """Run IC Algorithm over variables and given probability distribution
    Returns a DAG """
    # construct a complete graph
    edges = []
    # create non directed edges between all possible vertices
    for (a,b) in itertools.combinations(varlist, 2):
        e = Edge(a, b)
        edges.append(e)
    graph = DAG("Graph", varlist, edges, factors )
    graph = construct_skeleton(graph)
    return graph

def construct_skeleton(graph):
    """Step 1 in IC Algorithm. 
    For each pair of vertices, check whether there is a set that d-separate them.
    If such set exist, remove the edge from 2 vertices."""
    varlist = graph.nodes()
    for (a,b) in itertools.combinations(varlist, 2):
        for r in range(1, len(varlist)+1):
            others = varlist.copy()
            others.remove(a)
            others.remove(b)
            for c in itertools.combinations(others,r):
                if test_independence(c, a, b, graph.factors()):
                    e = find_edge(a,b,graph)
                    graph.edges.remove(e)
    return graph

def find_edge(var1, var2, graph):
    """Find an edge that connects 2 nodes var1 and var2"""
    for e in graph.edges:
        if var1 in e.get_vertices() and var2 in e.get_vertices:
            return e
        
def test_independence(s, n1, n2, factors):
    """Check if a set of variables s d-separate 2 nodes n1 and n2"""
    ### Calculate P(n1 | s)
    n1_s = None
    ### Calculate P(n2 | s)
    n2_s = None
    ### Calculate P(n1, n2 | s)
    n1n2_s = None
    return n1_s*n2_s == n1n2_s # if 2 values are equal then
                                # n1, n2 are independent conditioning on S


if __name__ == '__main__':
    # Data
    # Variables in the graph
    Z = Node("Z", ["z", "-z"])
    X = Node("X", ["x", "-x"])
    M = Node("M", ["m", "-m"])
    Y = Node("Y", ["y", "-y6"])
    vars = [Z, X, M, Y]
    # Probability distribution
    F = Factor("P(Z,X,M,Y)", [Z, X, M, Y])
    F.add_values([["-z", "-x", "-m", "-y", 0.0392], ["-z", "-x", "-m", "y", 0.0098],
                  ["-z", "-x", "m", "-y", 0.1372], ["-z", "-x", "m", "y", 0.0588],
                  ["-z", "x", "-m", "-y", 0.0399], ["-z", "x", "-m", "y", 0.0021],
                  ["-z", "x", "m", "-y", 0.05355], ["-z", "x", "m", "y", 0.00945],
                  ############################Z = 1###########################
                  ["z", "-x", "-m", "-y", 0.0286], ["z", "-x", "-m", "y", 0.0234],
                  ["z", "-x", "m", "-y", 0.0832], ["z", "-x", "m", "y", 0.1248],
                  ["z", "x", "-m", "-y", 0.1014], ["z", "x", "-m", "y", 0.0546],
                  ["z", "x", "m", "-y", 0.117], ["-z", "x", "m", "y", 0.117]])
    factors = [F]
    dag = IC(vars, factors)
