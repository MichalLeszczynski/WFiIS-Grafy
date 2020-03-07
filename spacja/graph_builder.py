import random
from .simple_graph import SimpleGraph
from .functions import is_valid_graph_sequence


class GraphBuilder:
    """Tworzy różne rodzaje grafów"""

    def get_eulerian_graph(self, size):
        """Losowy graf Eulerowski"""
        while True:
            seq = []
            for d in range(size):
                d = random.randint(2, size - 1)
                seq.append(d - d % 2)
            if is_valid_graph_sequence(seq):
                break

        g = SimpleGraph().from_graph_sequence(seq)
        while True:
            if g.is_connected_graph():
                break
            g.randomize(size)
        return g

    def get_k_regular_graph(self, size, k, connected=False):
        """Graf z wierzchołkami o tym samym stopniu"""
        seq = [k for _ in range(size)]
        g = SimpleGraph().from_graph_sequence(seq)
        if connected:
            if k < 2:
                raise ValueError("Twój argument jest inwalidą.")
            while True:
                if g.is_connected_graph():
                    break
                g.randomize(size)
        return g
