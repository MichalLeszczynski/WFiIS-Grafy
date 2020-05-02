import random
from spacja.directed_graph import DirectedGraph
from spacja.functions import is_valid_graph_sequence
from spacja.simple_graph import SimpleGraph


class GraphBuilder:
    """Tworzy różne rodzaje grafów"""

    @staticmethod
    def get_eulerian_graph(size=None):
        """Losowy graf Eulerowski"""
        if size is None:
            size = random.randint(2, 16)
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

    @staticmethod
    def get_k_regular_graph(size, k, connected=False):
        """Graf z wierzchołkami o tym samym stopniu"""
        seq = [k for _ in range(size)]
        g = SimpleGraph().from_graph_sequence(seq)
        if connected:
            if k < 2 and size != 2:
                raise ValueError("Nie da się stworzyć zadanego grafu.")
            while True:
                if g.is_connected_graph():
                    break
                g.randomize(size)
        return g

    @staticmethod
    def get_random_graph(max_size=20):
        """Losowy graf"""
        size = random.randint(2, max_size)
        g = SimpleGraph(size)
        g.connect_random(random.random())
        return g

    @staticmethod
    def get_random_connected_graph(max_size=20):
        """Losowy graf spojny"""
        g = GraphBuilder.get_random_graph(max_size)
        while not g.is_connected_graph():
            g = GraphBuilder.get_random_graph(max_size)
        return g

    @staticmethod
    def get_random_weighted_graph(max_size=20):
        """Losowy graf"""
        g = GraphBuilder.get_random_graph(max_size)
        g.assign_random_weights()
        return g

    @staticmethod
    def get_random_weighted_connected_graph(max_size=20):
        """Losowy graf"""
        g = GraphBuilder.get_random_connected_graph(max_size)
        g.assign_random_weights()
        return g

    @staticmethod
    def get_random_flow_network(N):
        """
        Losowa sieć przepływu
        N - liczba warstw sieci
        źródło - Node #1
        ujście - Node #len(graph)
        """
        assert N >= 2

        print(f'liczba warstw: {N}')

        # krok 1: tworzenie warstw
        node_count_in_layer = [1] + [random.randint(2, N) for _ in range(N)] + [1]

        node_layer = [None]
        layer_nodes = []

        total = 1
        for i, count in enumerate(node_count_in_layer):
            node_layer.extend([i] * count)
            layer_nodes.append(list(range(total, total + count)))
            total += count

        print(f"liczba wierzchołków w warstwie: {node_count_in_layer}")
        print(f"wierzchołki w warstwie: {layer_nodes}")

        # krok 2: losowanie krawędzi między warstwami
        g = DirectedGraph(size=sum(node_count_in_layer))

        for i in range(1, N + 1):
            for node in layer_nodes[i]:
                # losowa krawędź wchodząca
                g.connect(random.choice(layer_nodes[i - 1]), node)
                # losowa krawędź wychodząca
                g.connect(node, random.choice(layer_nodes[i + 1]))

        # krok 3: odajemy 2N losowych łuków

        edges_added = 0
        while edges_added < 2 * N:
            # brak krawędzi wychodzącej z ujścia
            n1 = random.randint(1, len(g) - 1)
            # brak krawędzi wchodzącej do źródła
            n2 = random.randint(2, len(g))
            print('wylosowano krawędź {} -> {}'.format(n1, n2))
            if n1 == n2 or g.is_connected(n1, n2) or g.is_connected(n2, n1):
                print('odrzucono')
                continue
            g.connect(n1, n2)
            edges_added += 1
            print('połączono')
        # krok 4: przypisanie każdej krawędzi losowej przepustowości
        g.assign_random_weights()

        return g
