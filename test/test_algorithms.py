import random
import pytest
from spacja.algorithms import *
from spacja.graph_builder import GraphBuilder


class TestAlgorithms:
    def setup_method(self):
        self.gb = GraphBuilder()

    def test_find_eulerian_trail(self):
        g = self.gb.get_eulerian_graph(size=8)
        edges = g.edges()
        euler_trail = find_eulerian_trail(g)
        trail_edges = set()
        for i in range(len(euler_trail) - 1):
            v1 = min(euler_trail[i], euler_trail[i + 1])
            v2 = max(euler_trail[i], euler_trail[i + 1])
            trail_edges.add((v1, v2))
        assert edges == trail_edges

    def test_find_hamiltonian_circuit(self):
        g = self.gb.get_k_regular_graph(size=8, k=7)  # graf pełny
        vertices = [v for v, _ in g.g.items()]
        hamiltonian_circuit = find_hamiltonian_circuit(g)
        # Sprawdź czy krawędzie istnieją
        for i in range(1, len(hamiltonian_circuit) - 1):
            assert g.is_connected(hamiltonian_circuit[i], hamiltonian_circuit[i + 1])
        # Sprawdź czy każdy wierzchołek (oprócz ostatniego) został odwiedzony dokładnie raz
        assert sorted(hamiltonian_circuit) == sorted(vertices)
