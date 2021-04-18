import sys
import threading
from collections import defaultdict

sys.setrecursionlimit(800000)
threading.stack_size(67108864)

# # Kosaraju's Two-pass Algorithm
# # 1) let Grev = G with all arcs reversed
# # 2) run DFS-loop on Grev (compute "magical" ordering of nodes)
# # 3) run DFS-loop on G (discover the SCCs one-by-one)

finishing_times = []
leaders = defaultdict(list)


def build_graphs(file_name):
    graph = defaultdict(list)
    graph_rev = defaultdict(list)

    with open(file_name, "r") as f:
        for line in f.readlines():
            v, u, _ = line.split(" ")
            v = int(v.strip())
            u = int(u.strip())
            graph[v].append(u)
            graph_rev[u].append(v)
    return graph_rev, graph


def dfs(g, node_i, visited, is_first_pass=True, leader_node=None):
    visited.add(node_i)
    if not is_first_pass:
        leaders[leader_node].append(node_i)
    for neighbor_node in g[node_i]:
        if neighbor_node not in visited:
            dfs(g, neighbor_node, visited, is_first_pass, leader_node)

    if is_first_pass:
        # g = graph_rev
        finishing_times.append(node_i)
    return


def first_pass(g, start_node, end_node):
    visited = set()
    for node_i in range(end_node, start_node-1, -1):
        if node_i not in visited:
            dfs(g, node_i, visited)


def second_pass(g):
    visited = set()
    while finishing_times:
        node_i = finishing_times.pop()
        if node_i not in visited:
            leader_node = node_i
            dfs(g, node_i, visited, is_first_pass=False, leader_node=leader_node)


def test():
    # example taken from https://www.youtube.com/watch?v=_2XSoIb6wQo
    graph_rev, graph = build_graphs("week1/adj_list_test.txt")

    # reset global variables
    global finishing_times
    global leaders
    finishing_times = []
    leaders = defaultdict(list)

    first_pass(graph_rev, 0, 3)
    second_pass(graph)

    # now find the biggest SCCs
    sccs = sorted([len(v) for k, v in leaders.items()], reverse=True)[:5]
    return sccs


assert test() == [3, 1]


def actual():
    graph_rev, graph = build_graphs("week1/adj_list.txt")

    # reset global variables
    global finishing_times
    global leaders
    finishing_times = []
    leaders = defaultdict(list)

    first_pass(graph_rev, 1, 875714)
    second_pass(graph)

    # now find the biggest SCCs
    sccs = sorted([len(v) for k, v in leaders.items()], reverse=True)[:5]
    return sccs


thread = threading.Thread(target=actual)
thread.start()





