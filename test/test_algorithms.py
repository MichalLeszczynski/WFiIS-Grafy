import pytest

import random
import copy

from spacja.algorithms import (
    find_eulerian_trail,
    find_hamiltonian_circuit,
    find_shortest_path_dijkstra,
    get_graph_center,
    get_minimax_graph_center,
    get_minimal_spanning_tree_kruskal,
)
from spacja.graph_builder import GraphBuilder as gb
from spacja.helper_structures import Edge
from spacja.simple_graph import SimpleGraph
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

    G1 = [
        [0, 4, 1, 4, 10],
        [4, 0, 2, 0, 6],
        [1, 2, 0, 10, 0],
        [4, 0, 10, 0, 0],
        [10, 6, 0, 0, 0],
    ]

    G2 = [
        [0, 0, 6, 10, 8, 4, 1],
        [0, 0, 9, 0, 0, 8, 8],
        [6, 9, 0, 7, 9, 10, 0],
        [10, 0, 7, 0, 0, 4, 4],
        [8, 0, 9, 0, 0, 4, 4],
        [4, 8, 10, 4, 4, 0, 4],
        [1, 8, 0, 4, 4, 4, 0],
    ]

    G3 = [[0, 8, 2, 0], [8, 0, 0, 8], [2, 0, 0, 2], [0, 8, 2, 0]]

    G4 = [
        [0, 3, 10, 0, 8, 0, 0],
        [3, 0, 0, 0, 5, 6, 0],
        [10, 0, 0, 0, 8, 9, 8],
        [0, 0, 0, 0, 0, 10, 0],
        [8, 5, 8, 0, 0, 1, 0],
        [0, 6, 9, 10, 1, 0, 6],
        [0, 0, 8, 0, 0, 6, 0],
    ]

    GRAPHS_WITH_CENTERS = [(G1, 3), (G2, 7), (G3, 1), (G4, 5)]

    GRAPHS_WITH_MINIMAX_CENTERS = [(G1, 2), (G2, 7), (G3, 1), (G4, 6)]

    def test_find_shortest_path_dijkstra(self):
        pass

    @pytest.mark.parametrize("graph, center", GRAPHS_WITH_CENTERS)
    def test_get_graph_center(self, graph, center):
        g = SimpleGraph().fill_from_adjacency_matrix(graph)
        assert get_graph_center(g).index == center

    @pytest.mark.parametrize("graph, minimax_center", GRAPHS_WITH_MINIMAX_CENTERS)
    def test_minimax_get_graph_center(self, graph, minimax_center):
        g = SimpleGraph().fill_from_adjacency_matrix(graph)
        assert get_minimax_graph_center(g).index == minimax_center

    def test_get_minimal_spanning_tree_kruskal(self):
        pass
