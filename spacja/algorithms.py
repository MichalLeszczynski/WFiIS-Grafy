"""Algorytmy działające na grafach"""
import copy
import random
from typing import List, Tuple, Dict
from spacja.graph import Node
from spacja.simple_graph import SimpleGraph
from spacja.helper_structures import Matrix


def find_eulerian_trail(g) -> List[Node]:
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


def find_hamiltonian_circuit(g) -> List[Node]:
    """Znajduje losowy cykl Hamiltona w grafie"""
    g = copy.deepcopy(g)
    if not g.is_connected_graph():
        raise ValueError(f"Graf nie jest spójny:\n{g}")
    stack = [random.choice(tuple(g.nodes))]
    solution = hamilton_search_r(g, stack)
    return solution


def hamilton_search_r(g, stack) -> List[Node]:
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
) -> Tuple[Dict[Node, int], Dict[Node, Node]]:
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

    d = {node: int(distance[node]) for node in g.nodes}
    p = {node: predecessors[node] for node in g.nodes}

    return d, p


def get_distances_to_nodes_matrix(g: SimpleGraph) -> Matrix:
    distances_matrix = [[0 for _ in g.nodes] for _ in g.nodes]
    for node in g.nodes:
        distances, _ = find_shortest_path_dijkstra(g, node)
        for to_node, distance in distances.items():
            distances_matrix[node - 1][to_node - 1] = distance

    return distances_matrix


def get_graph_center(g: SimpleGraph) -> Node:
    distances_matrix = get_distances_to_nodes_matrix(g)
    summary_distances = [
        sum(distances_from_node) for distances_from_node in distances_matrix
    ]
    graph_center = summary_distances.index(min(summary_distances)) + 1
    return graph_center


def get_minimax_graph_center(g: SimpleGraph) -> Node:
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
