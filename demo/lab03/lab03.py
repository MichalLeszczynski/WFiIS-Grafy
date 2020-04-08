#!/usr/bin/env python3

import sys
from pprint import pprint
import copy

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import (
    find_shortest_path_dijkstra,
    get_distances_to_nodes_matrix,
    get_graph_center,
    get_minimax_graph_center,
    get_minimal_spanning_tree_kruskal,
)
from spacja.functions import get_all_trails_from_predecessors

# 1
print("\n\n***** 1 *****")

g = gb.get_random_weighted_connected_graph(12)
print(g)
pprint(g.edges)
g.save("lab03", file_format="png")

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
distances_matrix = get_distances_to_nodes_matrix(g)
for l in distances_matrix:
    print(*l, sep="\t")

pprint(g.to_adjacency_matrix())
# 4
print("\n\n***** 4 *****")

print(f"\nCentrum grafu: {get_graph_center(g)}")

print(f"\nMinimaxowe centrum grafu: {get_minimax_graph_center(g)}")


# 5
print("\n\n***** 5 *****")
print("\nGraf dla którego szukamy minimalnego drzewa rozpinającego:")
print(g)
print(g.edges)
mst = get_minimal_spanning_tree_kruskal(g)
print("\nMinimalne drzewo rozpinające (szukane algorytmem kruskala):")
print(mst)
print(mst.edges)
