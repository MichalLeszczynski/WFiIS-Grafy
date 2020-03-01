#!/usr/bin/env python3
from graph import Graph, print2d

g = Graph(5)

g.create_edge(1, 2)
g.create_edge(2, 3)
g.create_edge(3, 4)
g.create_edge(4, 5)
g.create_edge(5, 1)
g.create_edge(5, 2)
g.create_edge(2, 4)

print(g.g)
print(g.edges())

print('zapis do pliku')

g.save('test.g')
g.load('test.g')

print(g.g)
print(g.edges())

print('macierz sąsiedztwa')

print2d(g.adj_matrix())

g.from_adj_matrix(g.adj_matrix())

print(g.g)
print(g.edges())

print('macierz incydencji')

print2d(g.inc_matrix())

g.from_inc_matrix(g.inc_matrix())

print(g.g)
print(g.edges())

print('dodawanie losowych krawędzi')
g = Graph(8)
g.create_random_edges(5)

print(g.g)
print(g.edges())


print('łączenie z prawdopodobieństwem')
g = Graph(12)
g.connect_random(0.5)

print(g.g)
print(g.edges())

# rysowanie grafu
# dla małych grafów lub słabo połączonych nie rysuje dokładnego okręgu
g.save_dot('test.gv', engine='circo')
