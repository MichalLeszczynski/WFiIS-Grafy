#!/usr/bin/env python3

import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder
from spacja.functions import is_valid_graph_sequence
from spacja.algorithms import find_eulerian_trail, find_hamiltonian_circuit


def example01():
    """Ciąg graficzny"""
    print(is_valid_graph_sequence([4, 3, 3, 2, 2, 1, 1]))
    print(is_valid_graph_sequence([4, 3, 3, 2, 2, 1]))
    print(is_valid_graph_sequence([4, 4, 3, 1, 2]))

    g = SimpleGraph().from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
    g.save(filename="graph1", file_format="png")


def example02():
    """Randomizacja"""
    g = SimpleGraph().from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
    g.save(filename="graph2_before", file_format="png")
    g.randomize(100)
    g.save(filename="graph2_after", file_format="png")


def example03():
    """Największa wspólna składowa"""
    g = SimpleGraph().from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
    g.save(filename="graph3", file_format="png")
    pprint(g.component_list())
    print(f"Największa składowa: {g.largest_component()}")


def example04():
    """Losowy graf Eulerowski"""
    g = gb.get_eulerian_graph(size=8)
    print(g.graph_sequence())
    print(g)
    g.save(filename="graph4", file_format="png")
    euler_path = find_eulerian_trail(g)
    print("Ścieżka Eulera")
    print(euler_path)


def example05():
    """Generowanie grafów k-regularnych"""
    g = gb.get_k_regular_graph(size=6, k=2)
    g.save("k2", "png")

    g = gb.get_k_regular_graph(size=6, k=2, connected=True)
    g.save("k2_connected", "png")

    g = gb.get_k_regular_graph(size=6, k=4)
    g.save("k4", "png")

    g = gb.get_k_regular_graph(size=8, k=6)
    g.save("k6", "png")


def example06():
    """Grafy Hamiltonowskie"""
    for i in range(100):
        g = gb.get_random_graph(max_size=16)
        try:
            hamiltonian_circuit = find_hamiltonian_circuit(g)
            print(f"Znaleziono cykl Hamiltona:\n{hamiltonian_circuit}")
            print(g)
            g.save(f"Hamilton_{len(g)}_{i}", file_format="png")
            break
        except ValueError as e:
            print(e)
    else:
        print(
            "Nie udało się wygenerować losowo żadnych poprawnych grafów Hamiltonowskich"
        )


if __name__ == "__main__":
    gb = GraphBuilder()
    examples = [None, example01, example02, example03, example04, example05, example06]
    if len(sys.argv) == 2:
        example = int(sys.argv[1])
        examples[example]()
    else:
        print("Nieprawidłowa liczba argumentów:\n./lab02 <numer przykładu>")
