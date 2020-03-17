#!/usr/bin/env python3

import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph

g = SimpleGraph(5)
g.connect(1, 2)
g.connect(2, 3)
g.connect(3, 4)
g.connect(4, 5)
g.connect(5, 1)
g.connect(5, 2)
g.connect(2, 4)

print(g)
print(g.get_edges())

print("\nZapis do pliku")
g.save("lab01")
g.load("lab01.g")

print(g)
print(g.get_edges())

print("\nMacierz sąsiedztwa\n")

pprint(g.to_adjacency_matrix())
print("\nPo konwersji:\n")
g.fill_from_adjacency_matrix(g.to_adjacency_matrix())

print(g)
print(g.get_edges())

print("\nMacierz incydencji")

pprint(g.to_incidence_matrix())

print("\nPo konwersji:\n")

g.fill_from_incidence_matrix(g.to_incidence_matrix())

print(g)
print(g.get_edges())

print("\nDodawanie losowych krawędzi")
g = SimpleGraph(8)
g.add_random_edges(17)

print(g)
print(g.get_edges())


print("\nLosowe łączenie wierzchołków")
g = SimpleGraph(12)
g.connect_random(0.5)

print(g)
print(g.get_edges())

# Rysowanie grafu
# Dla małych grafów lub słabo połączonych nie rysuje dokładnego okręgu
g.save("lab01_circo", file_format="g", engine="circo")
g.save("lab01_circo", file_format="png", engine="circo")
g.save("lab01_dot", file_format="png", engine="dot")
