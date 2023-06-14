from dag import DAG, Node, Edge
from bnetbase import Factor
import itertools
import csv

def IC(data):
    """Run IC Algorithm over given data
    data is a csv file, header included.
    Returns a DAG """
    graph = construct_graph(data)
    # Step 1
    graph = construct_skeleton(graph)
    # Step 2
    graph = find_collider(graph)
    return graph


def construct_graph(data):
    """Construct a graph that have each column as a node, and there are edges between every node."""
    nodelist = []
    d = {} # dictionary contains {nodename: [node_values]}
    with open(data) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line = 0
        for row in csv_reader:
            if line == 0:
                nodename = row # list of node name
                for v in nodename:
                    d[v] = []
                    new_node = Node(name = v)
                    nodelist.append(new_node)
            else:
                break
    # Retrieve domain value of each node
    file = csv.DictReader(data)
    for col in file:
        for key in d:
            if col[key] not in d[key]:
                d[key].append(col[key])
    # Add domain value to each node
    for node in nodelist:
        node.add_domain_values(d[node.name])
    edges = []
    # create non directed edges between all possible vertices
    for (a,b) in itertools.combinations(nodelist, 2):
        e = Edge(a, b)
        edges.append(e)
    factors = create_factor(nodelist, data)
    graph = DAG("Graph", nodelist, edges, factors )
    return graph


def create_factor(variables: list(Node), data):
    """ Create a factor representing joint distribution of variables"""
    # TODO
    pass


def find_collider(graph: DAG):
    """For each pair of nonadjacent variables a and b with a common neighbor c,
    check if c is in the set S_ab such that a and b are independent given
    S_ab. If not, then c is a collider. a --> c <-- b """
    #TODO
    pass


def construct_skeleton(graph: DAG):
    """Step 1 in IC Algorithm. 
    For each pair of vertices, check whether there is a set that d-separate them.
    If such set exist, remove the edge from 2 vertices."""
    vertices = graph.nodes()
    for (a,b) in itertools.combinations(vertices, 2): # generate all possible pair (a,b) of vertices
        for r in range(1, len(vertices)-1): 
            others = vertices.copy()
            others.remove(a)
            others.remove(b)
            found_s = False
            for c in itertools.combinations(others,r):# generate all possible subsets of vertices that excludes 
                                                      # a,b to find a set S a indep b given S
                if test_independence(list(c), a, b, graph): # if a and b are indep given set C, then remove the edge a-b
                    e = find_edge(a,b,graph)
                    graph.edges.remove(e)
                    found_s = True
                    break
            if found_s:
                break
    return graph


def find_edge(var1: Node, var2: Node, graph: DAG):
    """Find an edge that connects 2 nodes var1 and var2"""
    for e in graph.edges:
        if var1 in e.get_vertices() and var2 in e.get_vertices:
            return e
        

def test_independence(s: list[Node], n1: Node, n2: Node, graph: DAG):
    """Returns whether a set of variables s d-separate 2 nodes n1 and n2."""

    ### Calculate P(n1 | s)
    n1_s = cond_prob([n1], s, graph)
    ### Calculate P(n2 | s)
    n2_s = cond_prob([n2], s, graph)
    ### Calculate P(n1, n2 | s)
    n1n2_s = cond_prob([n1, n2], s, graph)
    return n1_s*n2_s == n1n2_s # if 2 values are equal then
                                # n1, n2 are independent conditioning on S


def cond_prob(nodes: list(Node), s: list(Node), graph: DAG):
    """Calculate P(nodes|s)
    Returns a real number between 0 and 1"""
    
if __name__ == '__main__':
    data = "pharm_data.csv"
    print(IC(data))
