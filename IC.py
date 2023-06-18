from dag import DAG, Node, Edge
from bnetbase import Factor
import itertools
import csv
import pandas as pd

def IC(data):
    """Run IC Algorithm over given data
    data is a csv file, header included.
    Returns a DAG """
    graph = construct_graph(data)
    print(" A complete graph has been constructed.")
    print(graph)
    # Step 1
    graph = construct_skeleton(graph, data)
    print("A skeleton has been constructed.")
    print(graph)
    # Step 2
    #graph = find_collider(graph, data)
    #Step 33``
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
                line += 1
            else:
                break
    # Retrieve domain value of each node
    file = pd.read_csv(data)
    for key in d:
        d[key] = list(set(file[key]))
    # Add domain value to each node
    for node in nodelist:
        node.add_domain_values(d[node.name])
    edges = []
    # create non directed edges between all possible vertices
    for (a,b) in itertools.combinations(nodelist, 2):
        e = Edge(a, b)
        edges.append(e)
    graph = DAG("Graph", nodelist, edges)
    return graph


def find_collider(graph: DAG, data):
    """For each pair of nonadjacent variables a and b with a common neighbor c,
    check if c is in the set S_ab such that a and b are independent given
    S_ab. If not, then c is a collider. a --> c <-- b """
    for (a,b) in itertools.combinations(graph.Nodes, 2):
        if a in b.neighbors: # neighborhood is symmetric so do not check if b is a's neighbor
            continue
        # if a and b are not neighbors, check if they have any common neighbor
        c_lst = list(set(a.neighbors).intersection(b.neighbors))
        if len(c_lst) == 0:
            pass
        # now since c_lst is not empty, for every vertice c, check if they belong to S_ab
        for c in c_lst:
            if check_collider(a,b,data,graph, c):
                # make c becomes collider by adding arrow a -> c and b -> c
                for e in graph.Edges:
                    if a in e and c in e:
                        e.add_arrow(c)
                    elif b in e and c in e:
                        e.add_arrow(c)
            else:
                continue
    return graph

def check_collider(a: Node, b: Node, data, graph: DAG, c: Node):
    """ Returns whether c is a collider of a and b given current graph and data"""
    vertices = graph.nodes()
    vertices.remove(a)
    vertices.remove(b)
    for r in range(1, len(vertices) + 1):
        for comb in itertools.combinations(vertices, r):
            if c not in comb:
                continue
            if test_independence(list(c), a, b, data):
                return True
    return False

def construct_skeleton(graph: DAG, data):
    """Step 1 in IC Algorithm. 
    For each pair of vertices, check whether there is a set that d-separate them.
    If such set exist, remove the edge from 2 vertices."""
    vertices = graph.Nodes
    for (a,b) in itertools.combinations(vertices, 2): # generate all possible pair (a,b) of vertices
        for r in range(1, len(vertices)-1): 
            others = vertices.copy()
            others.remove(a)
            others.remove(b)
            found_s = False
            for c in itertools.combinations(others,r):# generate all possible subsets of vertices that excludes 
                                                      # a,b to find a set S a indep b given S
                if test_independence(list(c), a, b, data): # if a and b are indep given set C, then remove the edge a-b
                    print(list(c), "d-separate ", a, " and ", b)
                    e = find_edge(a,b,graph)
                    graph.Edges.remove(e)
                    a.remove_neighbors([b])
                    b.remove_neighbors([a])
                    found_s = True
                    break
            if found_s:
                break
    return graph


def find_edge(var1: Node, var2: Node, graph: DAG):
    """Find an edge that connects 2 nodes var1 and var2"""
    for e in graph.Edges:
        if var1 in e.get_vertices() and var2 in e.get_vertices():
            return e
        

def test_independence(s: list[Node], n1: Node, n2: Node, data):
    """Returns whether a set of variables s d-separate 2 nodes n1 and n2."""

    ### Calculate P(n1 | s)
    n1_s = cond_prob([n1], s, data)
    print("Probability of ", n1, " given ", s, " is ", n1_s)
    ### Calculate P(n2 | s)
    n2_s = cond_prob([n2], s, data)
    print("Probability of ", n2, " given ", s, " is ", n2_s)
    ### Calculate P(n1, n2 | s)
    n1n2_s = cond_prob([n1, n2], s, data)
    print("Probability of ", [n1,n2], " given ", s, " is ", n1n2_s)
    return n1_s*n2_s == n1n2_s # if 2 values are equal then
                                # n1, n2 are independent conditioning on S


def cond_prob(nodes: list[Node], s: list[Node], data):
    """Calculate P(nodes|s)
    Returns a real number between 0 and 1"""
    target = []
    for node in nodes:
        target.append(node.dom[0])
    evidence = []
    for node in s:
        evidence.append(node.dom[0])
    data = pd.read_csv(data)
    data_ev = reduce(data, s, evidence) # data_ev will be used to calculate P(s)
    data_joined = reduce(data_ev, nodes, target) # data_joined will be used to calculate P(nodes AND s)
    return len(data_joined)/len(data_ev)


def reduce(data, nodes: list[Node], target: list[str]):
    """Returns a table only with rows contain target values."""
    col = [node.name for node in nodes]
    return data[data[col] == target] # will have to recheck the syntax



if __name__ == '__main__':
    data = "pharm_data.csv"
    graph = IC(data)
    # print(graph)
