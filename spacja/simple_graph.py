from __future__ import annotations

import os
from typing import Set, Union

from spacja.graph import (
    Graph,
    Node,
    Edge,
    Weight,
    AdjencyList,
    AdjencyMatrix,
    IncidenceMatrix,
)


class SimpleGraph(Graph):
    def get_all_possible_edges(self) -> Set[Edge]:
        all_possible = set()
        all_possible.update(self.edges)
        all_possible.update(
            [Edge(edge.end, edge.begin, edge.weight) for edge in self.edges]
        )
        return all_possible

    def node_neighbours(self, node: Node) -> Set[Node]:
        """Returns Nodes adjecent to a given node """
        return set([edge.end for edge in self.node_edges(node)])

    def node_edges(self, node: Node) -> Set[Edge]:
        """Returns set of edges adjacent to the given node """
        return set(
            [edge for edge in self.get_all_possible_edges() if edge.begin == node]
        )

    def node_degree(self, node: Node) -> int:
        """Returns degree of a selected node """
        return len(self.node_edges(node))

    def edge_to_node(self, begin: Node, end: Node) -> Edge:
        """Get edge that connects given two nodes """
        edge = [
            e
            for e in self.get_all_possible_edges()
            if e.begin == begin and e.end == end
        ][0]
        return edge

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

        if node1.index > node2.index:
            node1, node2 = node2, node1
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
        ] + [edge for edge in self.edges if node1 == edge.end and node2 == edge.begin]

        edge_to_be_deleted = edges_to_be_deleted[0]
        self.edges.remove(edge_to_be_deleted)

    def is_connected(self, node1: Union[Node, int], node2: Union[Node, int]) -> bool:
        """Czy stnieje krawędź node1 -- node2"""
        if isinstance(node1, int):
            node1 = Node(node1)
        if isinstance(node2, int):
            node2 = Node(node2)
        return node2 in [
            edge.end for edge in self.get_all_possible_edges() if edge.begin == node1
        ]

    def to_adjacency_list(self) -> AdjencyList:
        """Zwraca graf w postaci listy sąsiedztwa"""
        adj_l = {
            (node.index): (
                set(
                    [
                        edge.end.index
                        for edge in self.get_all_possible_edges()
                        if edge.begin == node
                    ]
                )
            )
            for node in self.nodes
        }
        return adj_l

    def to_adjacency_matrix(self) -> AdjencyMatrix:
        """Zwraca graf w postaci macierzy sąsiedztwa"""
        adj_m = [[0 for _ in range(len(self))] for _ in range(len(self))]
        for edge in self.edges:
            n1 = edge.begin.index
            n2 = edge.end.index

            adj_m[n1 - 1][n2 - 1] = edge.weight
            adj_m[n2 - 1][n1 - 1] = edge.weight

        return adj_m

    def to_incidence_matrix(self) -> IncidenceMatrix:
        """Zwraca graf w postaci macierzy incydencji"""
        inc_m = [[0 for _ in range(len(self.edges))] for _ in range(len(self))]
        for i, edge in enumerate(self.edges):
            n1 = edge.begin.index
            n2 = edge.end.index

            inc_m[n1 - 1][i] = edge.weight
            inc_m[n2 - 1][i] = edge.weight

        return inc_m

    def fill_from_adjacency_matrix(self, adj_m: AdjencyMatrix) -> SimpleGraph:
        """Wypełnianie grafu z macierzy sąsiedztwa"""
        self.clear()

        size = len(adj_m)
        self.add_nodes(size)

        for n1 in range(len(self)):
            for n2 in range(len(self)):
                if n1 < n2 and adj_m[n1][n2]:
                    # mapowanie numerów wierzchołków: n-1 -> n
                    self.connect(n1 + 1, n2 + 1, weight=adj_m[n1][n2])
        return self

    def fill_from_incidence_matrix(self, inc_m: IncidenceMatrix) -> SimpleGraph:
        """Wypełnianie grafu z macierzy incydencji"""
        self.clear()

        nodes_count = len(inc_m)
        self.add_nodes(nodes_count)

        edges_count = len(inc_m[0])
        for i in range(edges_count):  # il. krawedzi
            edge_nodes = []
            weight = 0
            for n in range(nodes_count):
                # szukamy niezerowej wartosci w kolumnie
                if inc_m[n][i]:
                    edge_nodes.append(n)
                    weight = inc_m[n][i]
            # mapowanie numerów wierzchołków: n-1 -> n
            self.connect(
                Node(edge_nodes[0] + 1), Node(edge_nodes[1] + 1), weight=weight
            )
        return self

    def save(
        self, filename: str, file_format: str = "g", engine: str = "circo"
    ) -> None:
        """Zapisz graf w różnych formatach
            g - lista sąsiedztwa
            gv - dot format
            png - plik graficzny http://www.graphviz.org/
                engine = dot, neato, circo ...
        """
        if file_format == "g":
            filename += ".g"
            print(f'Zapisywanie grafu do pliku "{filename}"')
            with open(filename, "w") as f:
                f.write(f"{len(self)}\n")
                for edge in self.edges:
                    n1 = edge.begin.index
                    n2 = edge.end.index
                    f.write(f"{n1} {n2}\n")

        elif file_format == "gv":
            with open(f"{filename}.{file_format}", "w") as f:
                f.write("graph g {\n")
                for edge in self.edges:
                    n1 = edge.begin.index
                    n2 = edge.end.index
                    f.write(f"{n1} -- {n2}\n")
                connected_nodes = [edge.begin for edge in self.get_all_possible_edges()]
                not_connected_nodes = [
                    node for node in self.nodes if node not in connected_nodes
                ]
                for node in not_connected_nodes:
                    f.write(f"{node.index}\n")

                f.write("}\n")

        elif file_format == "png":
            self.save(filename, file_format="gv")
            filename += ".gv"
            os.system(f"dot -T png -K {engine} -O {filename}")
            os.system(f"rm {filename}")
