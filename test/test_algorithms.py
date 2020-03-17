import random
import pytest
from spacja.algorithms import *
from spacja.graph_builder import GraphBuilder
from spacja.graphs import Edge
from pprint import pprint

class TestAlgorithms:
    def setup_method(self):
        self.gb = GraphBuilder()

    def test_find_eulerian_trail(self):
        g = self.gb.get_eulerian_graph(size=5)
        edges = copy.deepcopy(g.edges)
        euler_trail = find_eulerian_trail(g)
        trail_edges = set()
        for i in range(len(euler_trail) - 1):
            edge = Edge(euler_trail[i], euler_trail[i+1])
            edge.sort()
            trail_edges.add(edge)
        for edge in edges:
            assert edge in trail_edges

    def test_find_hamiltonian_circuit(self):
        g = self.gb.get_k_regular_graph(size=8, k=7)  # graf pełny
        # vertices = [v for v, _ in g.g.items()]
        hamiltonian_circuit = find_hamiltonian_circuit(g)
        # Sprawdź czy krawędzie istnieją
        for i in range(1, len(hamiltonian_circuit) - 1):
            assert g.is_connected(hamiltonian_circuit[i], hamiltonian_circuit[i + 1])
        # Sprawdź czy każdy wierzchołek (oprócz ostatniego) został odwiedzony dokładnie raz
        assert sorted(hamiltonian_circuit, key=lambda x: x.index) == sorted(g.nodes, key=lambda x: x.index)
