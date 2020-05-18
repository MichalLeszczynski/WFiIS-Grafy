"""Algorytmy działające na grafach"""
import copy
import collections
import math
import random
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt


from spacja.functions import get_trail_to_node, stopwatch
from spacja.graph import Graph
from spacja.simple_graph import SimpleGraph
from spacja.directed_graph import DirectedGraph
from spacja.helper_structures import Matrix, Node


def find_eulerian_trail(g: SimpleGraph) -> List[Node]:
    """Znajduje losowy cykl Eulera w grafie"""
    if not g.is_eulerian():
        raise ValueError(f"Nie jest to graf Eulerowski\n{g}")

    solution = []
    stack = [random.choice(tuple(g.nodes))]
    while len(stack) != 0:
        current_vertex = stack[-1]
        if g.node_degree(current_vertex) == 0:
            solution.append(current_vertex)
            stack.pop()
        else:
            next_vertex = random.choice(tuple(g.node_edges(current_vertex))).end
            g.disconnect(current_vertex, next_vertex)
            stack.append(next_vertex)
    return solution


def find_hamiltonian_circuit(g: SimpleGraph) -> List[Node]:
    """Znajduje losowy cykl Hamiltona w grafie"""
    g = copy.deepcopy(g)
    if not g.is_connected_graph():
        raise ValueError(f"Graf nie jest spójny:\n{g}")
    stack = [random.choice(tuple(g.nodes))]
    solution = hamilton_search_r(g, stack)
    return solution


def hamilton_search_r(g: SimpleGraph, stack: List[Node]) -> List[Node]:
    # Zawiera wszystkie wierzcholki
    if set(stack) == g.nodes:
        # Istnieje połączenie między pierwszym a ostatnim
        if g.is_connected(stack[0], stack[-1]):
            return stack
        else:
            stack.pop
            return []
    else:
        for neighbour in g.node_neighbours(stack[-1]):
            if neighbour in stack:
                continue
            stack.append(neighbour)
            if hamilton_search_r(g, stack):
                return stack
    raise ValueError(f"Graf nie jest Hamiltonowski:\n{g}")


def find_shortest_path_dijkstra(
    g: SimpleGraph, source: Node
) -> Tuple[Dict[int, float], Dict[int, int]]:
    """ Przyjmuje graf i zrodlo (wierzcholek).
        Zwraca:
        - slownik odleglosci od zrodla
        - slownik poprzednikow
    """
    predecessors = {}
    distance = {}
    # kolejka priorytetowa dla wierzchołkow grafu (klucz: aktualnie wyliczona odleglosc)
    Q = []
    for node in g.nodes:
        distance[node] = float("inf")
        predecessors[node] = None
        Q.append(node)
    distance[source] = 0

    while Q:
        Q.sort(key=lambda n: distance[n])
        u = Q.pop(0)
        for v in g.node_neighbours(u):
            if v in Q:
                new_distance = distance[u] + g.edge_to_node(u, v).weight
                old_distance = distance[v]
                if new_distance < old_distance:
                    distance[v] = new_distance
                    predecessors[v] = u

    d = {node: distance[node] for node in g.nodes}
    p = {node: predecessors[node] for node in g.nodes}

    return d, p


def get_distances_to_nodes_matrix(g: Graph) -> Matrix:
    distances_matrix = [[0 for _ in g.nodes] for _ in g.nodes]
    for node in g.nodes:
        distances, _ = find_shortest_path_dijkstra(g, node)
        for to_node, distance in distances.items():
            distances_matrix[node - 1][to_node - 1] = distance

    return distances_matrix


def get_graph_center(g: Graph) -> Node:
    distances_matrix = get_distances_to_nodes_matrix(g)
    summary_distances = [
        sum(distances_from_node) for distances_from_node in distances_matrix
    ]
    graph_center = summary_distances.index(min(summary_distances)) + 1
    return graph_center


def get_minimax_graph_center(g: Graph) -> Node:
    distances_matrix = get_distances_to_nodes_matrix(g)
    max_distances = [
        max(distances_from_node) for distances_from_node in distances_matrix
    ]
    minimax_graph_center = max_distances.index(min(max_distances)) + 1
    return minimax_graph_center


def get_minimum_spanning_tree_kruskal(g: SimpleGraph) -> SimpleGraph:
    """
    Przyjmuje graf
    Zwraca jego minimalne drzewo rozpinające
    Korzysta z algorytmu kruskala
    """
    # minimum spanning tree
    mst = SimpleGraph(len(g))
    Q = []
    for edge in g.edges:
        Q.append(edge)

    while Q and not mst.is_connected_graph():
        Q.sort(key=lambda e: e.weight)
        current_edge = Q.pop(0)
        comps = mst.components()
        if comps[current_edge.begin] != comps[current_edge.end]:
            mst.edges.add(current_edge)
    return mst


def find_shortest_path_bellman_ford(
    g: DirectedGraph, source: Node
) -> Tuple[Dict[Node, int], Dict[Node, Node]]:
    """ Przyjmuje graf i zrodlo (wierzcholek).
        Zwraca:
        - slownik odleglosci od zrodla
        - slownik poprzednikow
    """
    predecessors = {}
    distance = {}

    for node in g.nodes:
        distance[node] = float("inf")
        predecessors[node] = None
    distance[source] = 0

    for _ in range(1, len(g)):
        for edge in g.edges:
            u = edge.begin
            v = edge.end
            new_distance = distance[u] + g.edge_to_node(u, v).weight
            old_distance = distance[v]
            if new_distance < old_distance:
                distance[v] = new_distance
                predecessors[v] = u

    # sprawdz, czy nie ma cykli o ujemnych wagach:
    for edge in g.edges:
        u = edge.begin
        v = edge.end
        if distance[v] > distance[u] + g.edge_to_node(u, v).weight:
            print("Wystepuje cykl o ujemnych wagach.")
            import sys

            sys.exit(-1)

    d = {node: int(distance[node]) for node in g.nodes}
    p = {node: predecessors[node] for node in g.nodes}

    return d, p


def johnson_get_distances_to_nodes_matrix(g: Graph) -> Matrix:
    # dodaj wierzchołek s na potrzeby algorytmu
    g_p = copy.deepcopy(g)
    g_p.add_nodes()
    s = max(g_p.nodes)
    for node in g.nodes:
        g_p.connect(s, node, weight=0)

    # sprawdź, czy nie ma cyklów o ujemnej sumie wag
    d, _ = find_shortest_path_bellman_ford(g_p, s)

    h = {}
    from pprint import pprint

    for v in g_p.nodes:
        h[v] = d[v]

    for edge in g_p.edges:
        edge.weight = edge.weight + h[edge.begin] - h[edge.end]

    distances_matrix = [[0 for _ in g.nodes] for _ in g.nodes]
    for u in g.nodes:
        distances, _ = find_shortest_path_dijkstra(g_p, u)
        for v in g.nodes:
            distances_matrix[u - 1][v - 1] = distances[v] - h[u] + h[v]
    return distances_matrix


def breadth_first_search(
    g: Graph, source: Node, target: Node = None
) -> Dict[int, None]:
    """Przeszukiwanie wszerz. Na podstawie alg_5.pdf"""
    # tablica odległości
    d = {n: math.inf for n in g.nodes}
    d[source] = 0
    # tablica poprzedników
    p = {n: None for n in g.nodes}

    q = collections.deque()
    q.append(source)

    while q:
        v = q.popleft()
        for u in g.node_neighbours(v):
            if d[u] == math.inf:
                d[u] = d[v] + 1
                p[u] = v
                q.append(u)
                if u == target:
                    break
    return p


def ford_fulkerson(
    g: DirectedGraph, verbose: bool = False
) -> Dict[Tuple[int, int], int]:
    """Edmonds–Karp implementation"""
    # sieć rezydualna
    gf = copy.deepcopy(g)
    # źródło
    s: Node = 1
    # ujście
    t: Node = len(g)
    # przepływ krawędzi
    f = {(e.begin, e.end): 0 for e in g.edges}

    step = 0

    while True:
        p = get_trail_to_node(breadth_first_search(gf, s, t), t)
        if p == [t]:
            if verbose:
                print("nie istnieje kolejna ścieżka rozszerzająca")
            break
        if verbose:
            print(f"ścieżka rozszerzająca: {p}")
        p_edges = [gf.edge_to_node(p[i - 1], p[i]) for i in range(1, len(p))]
        cf_p = min(e.weight for e in p_edges)
        if verbose:
            print(f"przepustowość rezydualna ścieżki: {cf_p}")
        for edge in p_edges:
            u = edge.begin
            v = edge.end
            if g.is_connected(u, v):
                f[(u, v)] = f[(u, v)] + cf_p
            else:
                f[(v, u)] = f[(v, u)] - cf_p
                if verbose:
                    print(f"kasowanie przepływu, krawędź: ({u}, {v})")
        # update residual network weights
        gf.edges = set()
        for u, v, c in {(e.begin, e.end, e.weight) for e in g.edges}:
            w1 = c - f[(u, v)]
            w2 = f[(u, v)]
            if w1 != 0:
                gf.connect(u, v, w1)
            if w2 != 0:
                gf.connect(v, u, w2)
        step += 1
    return f


def page_rank(g: DirectedGraph, d=0.15, algorithm="matrix") -> Dict[int, float]:
    """
    Zwraca ranking węzłów w grafie skierowanym
    d - prawdopodobieństwo teleportacji
    """
    if d < 0 or d > 1:
        raise ValueError("Nieprawidłowa wartość dla prawdopodobieństwa")

    if g.has_dangling_nodes():
        raise ValueError(
            "Nieprawidłowy graf: posiada wierzchołki bez krawędzi wyjściowych."
        )

    if algorithm == "random_walk":
        return _page_rank_random_walk(g, d=d)
    elif algorithm == "matrix":
        return _page_rank_matrix(g, d=d)
    else:
        raise ValueError("Nieprawidłowy wybór algorytmu.")


def _page_rank_random_walk(g: DirectedGraph, d) -> Dict[int, float]:
    adj_l = g.to_adjacency_list()
    visited = {n: 0 for n in g.nodes}
    current_node = random.choice(list(g.nodes))
    N = 0
    while N < 100000:
        if random.random() > d and len(adj_l[current_node]) != 0:
            current_node = random.choice(list(adj_l[current_node]))
        else:
            current_node = random.choice(list(g.nodes))

        visited[current_node] += 1
        N += 1
    return {n: v / sum(visited.values()) for n, v in visited.items()}


def _page_rank_matrix(g: DirectedGraph, d) -> Dict[int, float]:
    n = len(g.nodes)
    P = np.zeros((n, n))
    A = np.array(g.to_adjacency_matrix())
    for i in range(n):
        for j in range(n):
            P[i][j] = (1.0 - d) * A[i][j] / g.node_degree(i + 1) + d / float(n)

    p0 = np.full(n, 1 / n)
    p1 = np.zeros(n)
    i = 0
    err = float("inf")
    while err > 1e-11:
        p1 = p0.dot(P)
        diff = p1 - p0
        err = sum(x ** 2 for x in diff)
        p0 = p1
        i += 1

    print(f"Zbieżność uzyskano po {i} iteracjach.")
    return {k: p1[k - 1] for k in range(1, n + 1)}


def simulated_annealing(g: SimpleGraph, MAX_IT=None, P: List[int] = None, save=False):
    if not g.is_complete():
        return ValueError("Do tego algorytmu graf musi być pełny.")

    if P is None:
        P = [n for n in range(1, len(g) + 1)]
        random.shuffle(P)

    if MAX_IT is None:
        MAX_IT = len(g)

    adj_m = g.to_adjacency_matrix()
    d = circuit_length(adj_m, P)
    for i in range(100, 0, -1):
        T = 0.001 * i ** 2
        for _ in range(MAX_IT):
            # switch: a-b c-d --> a-c b-d
            _, b, c, _ = _choose_nodes(P)
            P[b], P[c] = P[c], P[b]

            d_new = circuit_length(adj_m, P)
            if d_new < d:
                d = d_new
            else:
                r = random.random()
                if r < math.exp(-(d_new - d) / T):
                    d = d_new
                else:
                    # switch back
                    P[b], P[c] = P[c], P[b]

    if save:
        x = [g.x[n - 1] for n in P]
        y = [g.y[n - 1] for n in P]

        # connect first and last point
        x.append(g.x[P[0] - 1])
        y.append(g.y[P[0] - 1])

        plt.plot(x, y, "-o")
        plt.title(f"MAX_IT={MAX_IT}, d={d:.3f}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.savefig("SA.png")
        plt.clf()

    return P


def _choose_nodes(P: List[int]) -> Tuple[int, int, int, int]:
    while True:
        a = random.randrange(len(P))
        b = (a - 1) % len(P) if random.getrandbits(1) else (a + 1) % len(P)
        c = random.randrange(len(P))
        d = (c - 1) % len(P) if random.getrandbits(1) else (c + 1) % len(P)
        nodes = [P[a], P[b], P[c], P[d]]
        if len(set(nodes)) == len(nodes):
            return a, b, c, d


def circuit_length(adj_m, P: List[int]) -> float:
    length = 0.0
    for i in range(len(P)):
        length += adj_m[P[i] - 1][P[(i + 1) % len(P)] - 1]
    return length
