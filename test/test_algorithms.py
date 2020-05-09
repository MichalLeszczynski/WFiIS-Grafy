import pytest

import copy

from spacja.algorithms import (
    find_eulerian_trail,
    find_hamiltonian_circuit,
    get_distances_to_nodes_matrix,
    get_graph_center,
    get_minimax_graph_center,
    get_minimum_spanning_tree_kruskal,
    breadth_first_search,
    ford_fulkerson,
)
from spacja.directed_graph import DirectedGraph
from spacja.functions import get_trail_to_node
from spacja.graph_builder import GraphBuilder as gb
from spacja.helper_structures import Edge
from spacja.simple_graph import SimpleGraph


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
        assert sorted(hamiltonian_circuit, key=lambda x: x) == sorted(
            g.nodes, key=lambda x: x
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

    @pytest.mark.parametrize("graph, center", GRAPHS_WITH_CENTERS)
    def test_get_graph_center(self, graph, center):
        g = SimpleGraph().from_adjacency_matrix(graph)
        assert get_graph_center(g) == center

    @pytest.mark.parametrize("graph, minimax_center", GRAPHS_WITH_MINIMAX_CENTERS)
    def test_minimax_get_graph_center(self, graph, minimax_center):
        g = SimpleGraph().from_adjacency_matrix(graph)
        assert get_minimax_graph_center(g) == minimax_center

    def test_get_minimum_spanning_tree_kruskal(self):
        g = gb.get_random_connected_graph()
        mst1 = get_minimum_spanning_tree_kruskal(g)
        assert all(node in mst1.nodes for node in g.nodes)

        mst2 = get_minimum_spanning_tree_kruskal(g)
        assert all(node in mst1.nodes for node in g.nodes)

        sum_g = sum(edge.weight for edge in g.edges)
        sum_mst1 = sum(edge.weight for edge in mst1.edges)
        sum_mst2 = sum(edge.weight for edge in mst2.edges)
        assert sum_mst1 == sum_mst2 <= sum_g

    BFS_G1 = {
        1: {2, 3},
        2: {1, 4, 5},
        3: {1, 6, 7},
        4: {2},
        5: {2, 7},
        6: {3},
        7: {3, 5, 8},
        8: {7},
    }
    BFS_GRAPH_SOURCE_TARGET_TRAIL = [
        (BFS_G1, 1, 8, [1, 3, 7, 8]),
        (BFS_G1, 5, 3, [5, 7, 3]),
    ]

    @pytest.mark.parametrize(
        "graph, source, target, trail", BFS_GRAPH_SOURCE_TARGET_TRAIL
    )
    def test_breadth_first_search(self, graph, source, target, trail):
        g = SimpleGraph().from_adjacency_list(graph)
        tr = get_trail_to_node(breadth_first_search(g, source, target), target)
        assert tr == trail

    FF_G1 = [
        [0, 10, 3, 6, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 0, 8, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 10, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    FF_GRAPH_F_MAX = [(FF_G1, 19)]

    @pytest.mark.parametrize("graph, f_max", FF_GRAPH_F_MAX)
    def test_ford_fulkerson(self, graph, f_max):
        g = DirectedGraph().from_adjacency_matrix(graph)
        f = ford_fulkerson(g)

        gf_max = sum(weight for ((begin, end), weight) in f.items() if begin == 1)
        assert gf_max == f_max
