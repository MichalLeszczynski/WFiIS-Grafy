import pytest

from spacja.functions import is_valid_graph_sequence

GRAPH_SEQUENCES = [
    ([4, 3, 3, 2, 2, 1, 1], True),
    ([4, 3, 3, 2, 2, 1], False),
    ([6, 6, 6, 4, 4, 2, 2], False),
]


class TestFunctions:
    @pytest.mark.parametrize("sequence, result", GRAPH_SEQUENCES)
    def test_is_valid_graph_sequence(self, sequence, result):
        assert is_valid_graph_sequence(sequence) == result
