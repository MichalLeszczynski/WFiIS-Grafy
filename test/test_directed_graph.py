import pytest

from spacja.graph import Node
from spacja.directed_graph import DirectedGraph


class TestDirectedGraph:
    def test_connect_with_node(self):
        g = DirectedGraph(8)
        index_1 = 1
        index_2 = 2
        n1 = Node(index_1)
        n2 = Node(index_2)

        g.connect(n1, n2)
        assert g.is_connected(index_1, index_2)
        assert g.is_connected(n1, n2)
        assert not g.is_connected(index_2, index_1)
        assert not g.is_connected(n2, n1)

        g.disconnect(n1, n2)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)

    def test_connect_with_index(self):
        g = DirectedGraph(8)
        index_1 = 1
        index_2 = 2
        n1 = Node(index_1)
        n2 = Node(index_2)

        g.connect(index_1, index_2)
        assert g.is_connected(index_1, index_2)
        assert g.is_connected(n1, n2)

        g.disconnect(index_1, index_2)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)

    def test_connect_with_node_and_index(self):
        g = DirectedGraph(8)
        index_1 = 1
        index_2 = 2
        n1 = Node(index_1)
        n2 = Node(index_2)

        g.connect(index_1, index_2)
        assert g.is_connected(index_1, index_2)
        assert not g.is_connected(index_2, index_1)
        assert g.is_connected(n1, n2)
        assert not g.is_connected(n2, n1)

        g.disconnect(n1, n2)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)

        g.connect(n1, n2)
        assert g.is_connected(index_1, index_2)
        assert g.is_connected(n1, n2)

        g.disconnect(index_1, index_2)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)

        g.connect(n1, n2)
        g.connect(n2, n1)
        assert g.is_connected(index_1, index_2)
        assert g.is_connected(n1, n2)
        assert g.is_connected(index_2, index_1)
        assert g.is_connected(n2, n1)

        g.disconnect(index_1, index_2)
        assert g.is_connected(index_2, index_1)
        assert g.is_connected(n2, n1)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)

        g.disconnect(index_2, index_1)
        assert not g.is_connected(index_1, index_2)
        assert not g.is_connected(n1, n2)
        assert not g.is_connected(index_2, index_1)
        assert not g.is_connected(n2, n1)

    def test_save_to_file_and_load(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.save("test", "al")
        g.load("test.al")
        after = g.to_adjacency_list()
        assert before == after

    def test_adjacency_list(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.fill_from_adjacency_list(before)
        after = g.to_adjacency_list()

        assert before == after

    def test_adjacency_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_matrix()
        g.fill_from_adjacency_matrix(before)
        after = g.to_adjacency_matrix()

        assert before == after

    def test_incidence_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)
        before = g.to_adjacency_list()
        g.fill_from_incidence_matrix(g.to_incidence_matrix())
        after = g.to_adjacency_list()

        assert before == after
