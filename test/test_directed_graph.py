import pytest
import copy

from spacja.graph import Node
from spacja.directed_graph import DirectedGraph


class TestDirectedGraph:
    def test_connect(self):
        g = DirectedGraph(8)
        n1 = 1
        n2 = 2

        g.connect(n1, n2)
        assert g.is_connected(n1, n2)
        assert not g.is_connected(n2, n1)

        g.disconnect(n1, n2)
        assert not g.is_connected(n1, n2)

        g.connect(n1, n2)
        g.connect(n2, n1)
        assert g.is_connected(n1, n2)
        assert g.is_connected(n2, n1)

    def test_adjacency_list(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.from_adjacency_list(before)
        after = g.to_adjacency_list()

        assert before == after

    def test_adjacency_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_matrix()
        g.from_adjacency_matrix(before)
        after = g.to_adjacency_matrix()

        assert before == after

    def test_incidence_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)
        before = g.to_adjacency_list()
        g.from_incidence_matrix(g.to_incidence_matrix())
        after = g.to_adjacency_list()

        assert before == after

    def test_adjacency_list_file(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_matrix()
        g.save("test", "al")
        g.load("test.al")
        after = g.to_adjacency_matrix()

        assert before == after

    def test_adjacency_matrix_file(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_matrix()
        g.save("test", "am")
        g.load("test.am")
        after = g.to_adjacency_matrix()

        assert before == after

    def test_incidence_matrix_file(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)
        
        before = g.to_adjacency_matrix()
        g.save("test", "im")
        g.load("test.im")
        after = g.to_adjacency_matrix()

        assert before == after

    def test_is_connected_graph(self):
        g = DirectedGraph(3)
        g.connect(1, 2)
        g.connect(1, 3)
        g.connect(2, 3)
        assert not g.is_connected_graph()

        g.connect(3, 1)
        assert g.is_connected_graph()

    def test_components(self):
        g = DirectedGraph(3)
        g.connect(2, 1)
        g.connect(1, 3)
        g.connect(3, 1)

        comps = g.components()

        assert comps[1] == comps[3]
        assert comps[2] != comps[1]
        assert comps[2] != comps[3]

    def test_component_list(self):
        g = DirectedGraph(3)
        g.connect(2, 1)
        g.connect(1, 3)
        g.connect(3, 1)

        comps = g.component_list()

        assert [1, 3] in comps.values()
        assert [2] in comps.values()
        assert [2, 1] not in comps.values()