#!/usr/bin/env python3
import pytest
from .simple_graph import SimpleGraph


class TestSimpleGraph:
    def test_from_graph_sequence(self):
        g = SimpleGraph()
        g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
        assert g.g == {
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

    def test_add_random_edges(self):
        g = SimpleGraph(8)  # max = 28
        g.add_random_edges(8)
        assert len(g.edges()) == 8
        g.add_random_edges(20)
        assert len(g.edges()) == 28
        with pytest.raises(ValueError):
            g.add_random_edges(1)

    def test_components(self):
        g = SimpleGraph()
        g.from_graph_sequence([4, 3, 3, 2, 2, 1, 1])
        assert g.components() == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2}
