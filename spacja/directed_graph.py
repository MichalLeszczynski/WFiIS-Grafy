from __future__ import annotations

import os
import random
import itertools
import copy
from typing import Set, Union, Dict, List

from spacja.graph import Graph
from spacja.helper_structures import (
    Node,
    Edge,
    Weight,
    AdjacencyList,
    AdjacencyMatrix,
    IncidenceMatrix,
)


class DirectedGraph(Graph):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.separator = "->"
        self.name = "digraph"

    def get_all_possible_edges(self) -> Set[Edge]:
        return self.edges

    def connect(self, node1: Node, node2: Node, weight: Weight = 1) -> None:
        """Tworzy krawędż między wierzchołkiem node1 a node2"""
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError

        new_edge = Edge(node1, node2, weight)

        self.edges.add(new_edge)

    def disconnect(self, node1: Node, node2: Node) -> None:
        """Usuwa krawędż między wierzchołkiem node1 a node2"""
        if node1 not in self.nodes or node2 not in self.nodes or node1 == node2:
            raise ValueError

        edges_to_be_deleted = [
            edge for edge in self.edges if node1 == edge.begin and node2 == edge.end
        ]
        edge_to_be_deleted = edges_to_be_deleted[0]
        self.edges.remove(edge_to_be_deleted)

    def is_connected(self, node1: Node, node2: Node) -> bool:
        """Czy stnieje krawędź node1 -- node2"""
        return node2 in [edge.end for edge in self.edges if edge.begin == node1]

    def to_adjacency_matrix(self) -> AdjacencyMatrix:
        """Zwraca graf w postaci macierzy sąsiedztwa"""
        adj_m = [[0 for _ in range(len(self))] for _ in range(len(self))]
        for edge in self.edges:
            n1 = edge.begin
            n2 = edge.end

            adj_m[n1 - 1][n2 - 1] = edge.weight

        return adj_m

    def to_incidence_matrix(self) -> IncidenceMatrix:
        """Zwraca graf w postaci macierzy incydencji"""
        inc_m = [[0 for _ in range(len(self.edges))] for _ in range(len(self))]
        for i, edge in enumerate(self.edges):
            n1 = edge.begin
            n2 = edge.end

            inc_m[n1 - 1][i] = -edge.weight
            inc_m[n2 - 1][i] = edge.weight

        return inc_m

    def from_adjacency_matrix(self, adj_m: AdjacencyMatrix) -> DirectedGraph:
        """Wypełnianie grafu z macierzy sąsiedztwa"""
        self.clear()

        size = len(adj_m)
        self.add_nodes(size)

        for n1 in range(len(self)):
            for n2 in range(len(self)):
                if adj_m[n1][n2]:
                    # mapowanie numerów wierzchołków: n-1 -> n
                    self.connect(n1 + 1, n2 + 1, weight=adj_m[n1][n2])
        return self

    def from_incidence_matrix(self, inc_m: IncidenceMatrix) -> DirectedGraph:
        """Wypełnianie grafu z macierzy incydencji"""
        self.clear()

        nodes_count = len(inc_m)
        self.add_nodes(nodes_count)

        edges_count = len(inc_m[0])
        for i in range(edges_count):  # il. krawedzi
            weight = 0
            for n in range(nodes_count):
                # szukamy niezerowej wartosci w kolumnie
                if inc_m[n][i]:
                    if inc_m[n][i] < 0:
                        begin = n
                    else:
                        end = n
                    weight = abs(inc_m[n][i])
            # mapowanie numerów wierzchołków: n-1 -> n
            self.connect(begin + 1, end + 1, weight=weight)
        return self

    def components(self) -> Dict[int, int]:
        """Zwraca słownik złożony z wierzchołków i spójnych składowych do których należą (przy pomocy algorytmu kosaraju)"""
        g = self.to_adjacency_list()

        d = {v: -1 for v in g}
        f = {v: -1 for v in g}
        t = 0

        for v in g:
            if d[v] == -1:
                t = self.dfs_visit(v, g, d, f, t)

        g_t = self.transposed().to_adjacency_list()

        nr = 0  # nr spójnej składowej
        comp = {v: -1 for v in g_t}
        for v in sorted(g_t, key=lambda x: f[x], reverse=True):
            if comp[v] == -1:
                nr += 1
                comp[v] = nr
                self.components_r(nr, v, comp, g_t)
        return comp

    def dfs_visit(
        self, v: Node, g: AdjacencyList, d: Dict[Node, int], f: Dict[Node, int], t: int
    ) -> int:
        t += 1
        d[v] = t
        for u in g[v]:
            if d[u] == -1:
                t = self.dfs_visit(u, g, d, f, t)
        t += 1
        f[v] = t
        return t

    def transposed(self) -> DirectedGraph:
        g_t = copy.deepcopy(self)
        for edge in g_t.edges:
            edge.begin, edge.end = edge.end, edge.begin
        return g_t

    def connect_random(self, p: float) -> None:
        """
        Łączy wierzchołki tak, aby prawdopodobieństwo istnienia krawędzi
        między dowolnymi dwoma wierzchołkami wynosiło p
        iteracja po każdej kombinacji bez powtórzeń 2 wierzchołków
        """
        for n1, n2 in itertools.product(self.nodes, repeat=2):
            if random.random() < p and n1 != n2:
                self.connect(n1, n2)

    def has_dangling_nodes(self) -> bool:
        adj_l = self.to_adjacency_list()
        for s in adj_l.values():
            if len(s) == 0:
                return True
        return False
