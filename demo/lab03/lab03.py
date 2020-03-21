#!/usr/bin/env python3

import sys
from pprint import pprint
import copy

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import find_shortest_path_dijkstra, get_minimal_spanning_tree_kruskal
from spacja.functions import get_all_trails_from_predecessors

# 1 
print("\n\n***** 1 *****")
g = gb.get_random_weighted_connected_graph(8)
print(g)
pprint(g.edges)

# 2 
print("\n\n***** 2 *****")

print("\nDijkstra:")
distances, predecessors = find_shortest_path_dijkstra(g, tuple(g.nodes)[0])

print("Odleglosci od wierzcholka:")
pprint(distances)
print("\nPoprzednicy wierzcholkow:")
pprint(predecessors)
print("\nSciezki:")
pprint(get_all_trails_from_predecessors(predecessors))

# 3
print("\n\n***** 3 *****")

print("\nMacierz odleglosci:")
distances_matrix = [[0 for _ in g.nodes] for _ in g.nodes]

for node in g.nodes:
    distances, _ = find_shortest_path_dijkstra(g, node)
    for to_node, distance in distances.items():
        distances_matrix[node.index-1][to_node.index-1] = distance

for l in distances_matrix:
    print(*l, sep="\t")


# 4
print("\n\n***** 4 *****")

print("\nSumy odleglosci:")
summary_distances = [sum(distances_from_node) for distances_from_node in distances_matrix]
pprint(summary_distances)
graph_center = summary_distances.index(min(summary_distances))
print(f"Centrum grafu: {graph_center + 1}, suma odleglosci: {summary_distances[graph_center]}")

print("\nMaksymalne odleglosci od wierzcholkow:")
max_distances = [max(distances_from_node) for distances_from_node in distances_matrix]
pprint(max_distances)
graph_center = max_distances.index(min(max_distances))
print(f"Minimaxowe centrum grafu: {graph_center + 1}, minimalna odleglosc: {max_distances[graph_center]}")


# 5
print("\n\n***** 5 *****")
print("\nGraf dla którego szukamy minimalnego drzewa rozpinającego:")
print(g)
print(g.edges)
mst = get_minimal_spanning_tree_kruskal(g)
print("\nMinimalne drzewo rozpinające (szukane algorytmem kruskala):")
print(mst)
print(mst.edges)
