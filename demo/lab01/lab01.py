#!/usr/bin/env python3

import sys

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
print(g.edges())

print("\nZapis do pliku")
g.save("lab01")
g.load("lab01.g")

print(g)
print(g.edges())

print("\nMacierz sąsiedztwa")

print(g.adjacency_matrix())

g.from_adjacency_matrix(g.adjacency_matrix())

print(g)
print(g.edges())

print("\nMacierz incydencji")

print(g.incidence_matrix())

g.from_incidence_matrix(g.incidence_matrix())

print(g)
print(g.edges())

print("\nDodawanie losowych krawędzi")
g = SimpleGraph(8)
g.add_random_edges(5)

print(g)
print(g.edges())


print("\nLosowe łączenie wierzchołków")
g = SimpleGraph(12)
g.connect_random(0.5)

print(g)
print(g.edges())

# Rysowanie grafu
# Dla małych grafów lub słabo połączonych nie rysuje dokładnego okręgu
g.save("lab01_circo", file_format="png", engine="circo")
g.save("lab01_dot", file_format="png", engine="dot")
