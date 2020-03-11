#!/usr/bin/env python3

import sys

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder
from spacja.functions import is_valid_graph_sequence
from spacja.algorithms import find_eulerian_trail, find_hamiltonian_circuit

# setup
gb = GraphBuilder()

# 1
print("\n#1 Ciąg graficzny")
print(is_valid_graph_sequence([4, 3, 3, 2, 2, 1, 1]))
print(is_valid_graph_sequence([4, 3, 3, 2, 2, 1]))
g = SimpleGraph()
g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])

# 2
print("\n#2 Randomizacja")
print(g.edges())
g.randomize(100)
print(g.edges())

# 3
print("\n#3 Największa wspólna składowa")
g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
print(g.largest_component())

# 4
print("\n#4 Losowy graf Eulerowski")
g = gb.get_eulerian_graph(size=8)
print(g.graph_sequence())
print(g)
g.save(filename="euler", file_format="png")
euler_path = find_eulerian_trail(g)
print("Ścieżka Eulera")
print(euler_path)

# 5
print("\n#5 Generowanie grafów k-regularnych")
g = gb.get_k_regular_graph(size=6, k=2)
g.save("k2", "png")
g = gb.get_k_regular_graph(size=6, k=2, connected=True)
g.save("k2_connected", "png")
g = gb.get_k_regular_graph(size=6, k=4)
g.save("k4", "png")
g = gb.get_k_regular_graph(size=8, k=6)
g.save("k6", "png")

# 6
print("\n#6 Grafy Hamiltonowskie")
for i in range(100):
    g = gb.get_random_graph(max_size=16)
    try:
        hamiltonian_circuit = find_hamiltonian_circuit(g)
        print("Znaleziono cykl Hamiltona")
        print(hamiltonian_circuit)
        g.save("Hamilton_{}".format(i), "png")
        break
    except ValueError as e:
        print(e)
else:
    print("Nie udało się wygenerować losowo żadnych poprawnych grafów Hamiltonowskich")
