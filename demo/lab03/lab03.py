#!/usr/bin/env python3

import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import find_shortest_path_dijkstra
from spacja.functions import get_all_trails_from_predecessors

# 1 
g = gb.get_random_weighted_connected_graph(8)
print(g)
pprint(g.edges)

# 2 
print("Dijkstra:")
distances, predecessors = find_shortest_path_dijkstra(g, tuple(g.nodes)[0])

print("Odleglosci od wierzcholka:")
pprint(distances)
print("Poprzednicy wierzcholkow:")
pprint(predecessors)

# 3 
pprint(get_all_trails_from_predecessors(predecessors))