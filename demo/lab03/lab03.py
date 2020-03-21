#!/usr/bin/env python3

import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import find_shortest_path_dijkstra

# 1 
g = gb.get_random_weighted_connected_graph(8)
print(g)
print(g.get_edges())

# 2 
print("Dijkstra:")
distances, predecessors = find_shortest_path_dijkstra(g, tuple(g.nodes)[0])

print("Odleglosci od wierzcholka:")
pprint(distances)
print("Poprzednicy wierzcholkow:")
pprint(predecessors)