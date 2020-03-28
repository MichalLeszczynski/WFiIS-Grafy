import pytest

from spacja.graph import Node, Edge
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

    # def test_is_connected_graph(self):
    #     g = DirectedGraph(4)
    #     g.connect(1, 2)
    #     g.connect(3, 4)
    #     assert not g.is_connected_graph()

    #     g.connect(2, 3)
    #     assert g.is_connected_graph()

    # def test_add_random_edges(self):
    #     g = DirectedGraph(8)  # max edges 28
    #     g.add_random_edges(8)
    #     assert len(g.edges) == 8
    #     g.add_random_edges(20)
    #     assert len(g.edges) == 28
    #     with pytest.raises(ValueError):
    #         g.add_random_edges(1)

    def test_save_to_file_and_load(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.save("test")
        g.load("test.g")
        after = g.to_adjacency_list()
        assert before == after

    def test_adjacency_list(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        # TODO: add hard-coded test
        before = g.to_adjacency_list()
        g.fill_from_adjacency_list(before)
        after = g.to_adjacency_list()

        assert before == after

    def test_adjacency_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)

        # TODO: add hard-coded test
        before = g.to_adjacency_matrix()
        g.fill_from_adjacency_matrix(before)
        after = g.to_adjacency_matrix()

        assert before == after

    def test_incidence_matrix(self):
        g = DirectedGraph(8)
        g.add_random_edges(15)
        print(g)
        print(g.edges)
        # TODO: add hard-coded test
        before = g.to_adjacency_list()
        g.fill_from_incidence_matrix(g.to_incidence_matrix())
        after = g.to_adjacency_list()

        assert before == after

    # def test_components(self):
    #     g = DirectedGraph()
    #     g.fill_from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
    #     comps = g.components()

    #     assert comps[1] == comps[2] == comps[3] == comps[4] == comps[5]
    #     assert comps[6] == comps[7]
    #     assert comps[1] != comps[6]
