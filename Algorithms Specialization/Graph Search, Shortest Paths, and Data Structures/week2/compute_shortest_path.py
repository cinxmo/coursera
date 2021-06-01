from collections import defaultdict
import heapq

with open('dijkstraData.txt', 'r') as f:
    # 201 since the 0th index isn't used
    n = 201
    graph = defaultdict(dict)

    for line in f.readlines():
        vertices = line.split('\t')
        # remove newline
        vertices.pop()
        # beginning node
        v = int(vertices[0])
        for tail in range(1, len(vertices)):
            # populate the matrix so we can quickly get the length
            u, length = vertices[tail].split(",")
            u = int(u)
            graph[v][u] = int(length)

# we'll define the shortest-path distance between 1 and v to be 1000000
shortest_paths = [1000000] * (n + 1)
def compute_shortest_paths(start_node, end_node):
    shortest_paths[1] = 0
    visit_next = [(0, start_node)]
    heapq.heapify(visit_next)
    while visit_next:
        length, node = heapq.heappop(visit_next)
        for neighbor_node in graph[node].keys():
            # update shortest distances if possible
            if length + graph[node][neighbor_node] < shortest_paths[neighbor_node]:
                shortest_paths[neighbor_node] = length + graph[node][neighbor_node]
                heapq.heappush(visit_next, (length + graph[node][neighbor_node], neighbor_node))


if __name__ == '__main__':
    for node in range(2, 201):
        compute_shortest_paths(1, node)
    indices = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    print(list(map(shortest_paths.__getitem__, indices)))
