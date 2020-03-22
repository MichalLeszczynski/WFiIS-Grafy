import pytest

import random
import copy

from spacja.algorithms import (
    find_eulerian_trail,
    find_hamiltonian_circuit,
    find_shortest_path_dijkstra,
    get_minimal_spanning_tree_kruskal,
)
from spacja.graph_builder import GraphBuilder as gb
from spacja.graph import Edge
from pprint import pprint


class TestAlgorithms:
    def test_find_eulerian_trail(self):
        g = gb.get_eulerian_graph(size=5)
        edges = copy.deepcopy(g.edges)
        euler_trail = find_eulerian_trail(g)
        trail_edges = set()
        for i in range(len(euler_trail) - 1):
            edge = Edge(euler_trail[i], euler_trail[i + 1])
            edge.sort()
            trail_edges.add(edge)
        for edge in edges:
            assert edge in trail_edges

    def test_find_hamiltonian_circuit(self):
        g = gb.get_k_regular_graph(size=8, k=7)  # graf pełny
        hamiltonian_circuit = find_hamiltonian_circuit(g)
        # Sprawdź czy krawędzie istnieją
        for i in range(1, len(hamiltonian_circuit) - 1):
            assert g.is_connected(hamiltonian_circuit[i], hamiltonian_circuit[i + 1])
        # Sprawdź czy każdy wierzchołek (oprócz ostatniego) został odwiedzony dokładnie raz
        assert sorted(hamiltonian_circuit, key=lambda x: x.index) == sorted(
            g.nodes, key=lambda x: x.index
        )

    def test_find_shortest_path_dijkstra(self):
        pass

    def test_get_minimal_spanning_tree_kruskal(self):
        pass