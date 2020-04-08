import pytest

from spacja.graph import Node
from spacja.simple_graph import SimpleGraph


class TestSimpleGraph:
    def test_from_graph_sequence(self):
        g = SimpleGraph()
        g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
        assert g.to_adjacency_list() == {
            1: {2, 3, 4, 5},
            2: {1, 3, 4},
            3: {1, 2, 5},
            4: {1, 2},
            5: {1, 3},
            6: {7},
            7: {6},
        }
        assert g.graph_sequence() == [4, 3, 3, 2, 2, 1, 1]

        with pytest.raises(ValueError):
            g.from_graph_sequence([4, 3, 3, 2, 2, 1])

    def test_connect(self):
        g = SimpleGraph(8)
        n1 = 1
        n2 = 2
        
        g.connect(n1, n2)
        assert g.is_connected(n1, n2)
        assert g.is_connected(n2, n1)

        g.disconnect(n1, n2)
        assert not g.is_connected(n1, n2)
        assert not g.is_connected(n2, n1)

    def test_is_connected_graph(self):
        g = SimpleGraph(4)
        g.connect(1, 2)
        g.connect(3, 4)
        assert not g.is_connected_graph()

        g.connect(2, 3)
        assert g.is_connected_graph()

    def test_add_random_edges(self):
        g = SimpleGraph(8)  # 8 vertices => max 28 edges
        g.add_random_edges(8)
        assert len(g.edges) == 8
        g.add_random_edges(20)
        assert len(g.edges) == 28
        with pytest.raises(ValueError):
            g.add_random_edges(1)

    def test_save_to_file_and_load(self):
        g = SimpleGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.save("test", "al")
        g.load("test.al")
        after = g.to_adjacency_list()
        assert before == after

    def test_adjacency_list(self):
        g = SimpleGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.from_adjacency_list(before)
        after = g.to_adjacency_list()

        assert before == after

    def test_adjacency_matrix(self):
        g = SimpleGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_matrix()
        g.from_adjacency_matrix(before)
        after = g.to_adjacency_matrix()

        assert before == after

    def test_incidence_matrix(self):
        g = SimpleGraph(8)
        g.add_random_edges(15)

        before = g.to_adjacency_list()
        g.from_incidence_matrix(g.to_incidence_matrix())
        after = g.to_adjacency_list()

        assert before == after

    def test_components(self):
        g = SimpleGraph()
        g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
        comps = g.components()

        assert comps[1] == comps[2] == comps[3] == comps[4] == comps[5]
        assert comps[6] == comps[7]
        assert comps[1] != comps[6]

    def test_component_list(self):
        g = SimpleGraph()
        g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
        comps = g.component_list()

        assert [1, 2, 3, 4, 5] in comps.values()
        assert [6, 7] in comps.values()
