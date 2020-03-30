from __future__ import annotations

import os
from typing import Set, Union

from spacja.graph import (
    Graph,
    Node,
    Edge,
    Weight,
    AdjacencyList,
    AdjacencyMatrix,
    IncidenceMatrix,
)


class DirectedGraph(Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = "->"

    def get_all_possible_edges(self) -> Set[Edge]:
        return self.edges

    def connect(
        self, node1: Union[Node, int], node2: Union[Node, int], weight: Weight = 1
    ) -> None:
        """Tworzy krawędż między wierzchołkiem node1 a node2"""

        if isinstance(node1, int):
            node1 = Node(node1)
        if isinstance(node2, int):
            node2 = Node(node2)

        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError

        new_edge = Edge(node1, node2, weight)

        self.edges.add(new_edge)

    def disconnect(self, node1: Union[Node, int], node2: Union[Node, int]) -> None:
        """Usuwa krawędż między wierzchołkiem node1 a node2"""
        if isinstance(node1, int):
            node1 = Node(node1)
        if isinstance(node2, int):
            node2 = Node(node2)

        if node1 not in self.nodes or node2 not in self.nodes or node1 == node2:
            raise ValueError

        edges_to_be_deleted = [
            edge for edge in self.edges if node1 == edge.begin and node2 == edge.end
        ]
        edge_to_be_deleted = edges_to_be_deleted[0]
        self.edges.remove(edge_to_be_deleted)

    def is_connected(self, node1: Union[Node, int], node2: Union[Node, int]) -> bool:
        """Czy stnieje krawędź node1 -- node2"""
        if isinstance(node1, int):
            node1 = Node(node1)
        if isinstance(node2, int):
            node2 = Node(node2)
        return node2 in [edge.end for edge in self.edges if edge.begin == node1]

    def to_adjacency_matrix(self) -> AdjacencyMatrix:
        """Zwraca graf w postaci macierzy sąsiedztwa"""
        adj_m = [[0 for _ in range(len(self))] for _ in range(len(self))]
        for edge in self.edges:
            n1 = edge.begin.index
            n2 = edge.end.index

            adj_m[n1 - 1][n2 - 1] = edge.weight

        return adj_m

    def to_incidence_matrix(self) -> IncidenceMatrix:
        """Zwraca graf w postaci macierzy incydencji"""
        inc_m = [[0 for _ in range(len(self.edges))] for _ in range(len(self))]
        for i, edge in enumerate(self.edges):
            n1 = edge.begin.index
            n2 = edge.end.index

            inc_m[n1 - 1][i] = -edge.weight
            inc_m[n2 - 1][i] = edge.weight

        return inc_m

    def fill_from_adjacency_matrix(self, adj_m: AdjacencyMatrix) -> DirectedGraph:
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

    def fill_from_incidence_matrix(self, inc_m: IncidenceMatrix) -> DirectedGraph:
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
            self.connect(Node(begin + 1), Node(end + 1), weight=weight)
        return self
