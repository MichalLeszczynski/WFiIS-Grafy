#!/usr/bin/env python3
from __future__ import annotations

import itertools
import os
import random
from typing import Set, Dict, List, Any, Union
from dataclasses import dataclass
import abc 
from abc import ABC, abstractmethod 

from .functions import is_valid_graph_sequence  # type: ignore

Weight = int
AdjencyList = Dict[int, Set[int]]
AdjencyMatrix = List[List[int]]
IncidenceMatrix = List[List[int]]


@dataclass
class Node:
    index: int = 0

    def __str__(self) -> str:
        return str(self.index)

    def __hash__(self) -> Any:
        return hash(str(self))


@dataclass
class Edge:
    begin: Node
    end: Node
    weight: Weight = 1

    def __str__(self) -> str:
        s = f"{self.begin} -> {self.end} w: {self.weight}"
        return s

    def __hash__(self) -> Any:
        return hash(str(self))

    def sort(self): # tylko do grafów prostych!
        if self.begin.index > self.end.index:
            self.begin, self.end = self.end, self.begin


class Graph(ABC):
    nodes: Set[Node] = set()
    edges: Set[Edge] = set()

    def __init__(self, size=0):
        self.clear()
        self.add_nodes(count=size)

    def add_nodes(self, count=1) -> None:
        """Tworzy nowe wierzchołki"""
        for i in range(len(self) + 1, len(self) + 1 + count):
            self.nodes.add(Node(i))

    def __len__(self) -> int:
        return len(self.nodes)

    def node_degree(self, node: Node) -> int:
        """Returns degree of a selected node """
        pass

    def node_edges(self, node: Node) -> Set[Edge]:
        """Returns set of edges adjacent to the given node """
        pass

    def connect(
        self, node1: Union[Node, int], node2: Union[Node, int], weight: Weight = 1
    ) -> None:
        """Tworzy krawędż między wierzchołkiem node1 a node2"""
    
    @abstractmethod
    def disconnect(self, node1: Union[Node, int], node2: Union[Node, int]) -> None:
        """Usuwa krawędż między wierzchołkiem node1 a node2"""
        pass

    @abstractmethod
    def is_connected(self, node1: Union[Node, int], node2: Union[Node, int]) -> bool:
        """Czy stnieje krawędź node1 -- node2"""
        pass

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()

    @abstractmethod
    def to_adjacency_list(self) -> AdjencyList:
        """Zwraca graf w postaci listy sąsiedztwa"""
        pass
    @abstractmethod
    def to_adjacency_matrix(self) -> AdjencyMatrix:
        """Zwraca graf w postaci macierzy sąsiedztwa"""
        pass
    @abstractmethod
    def to_incidence_matrix(self) -> IncidenceMatrix:
        """Zwraca graf w postaci macierzy incydencji"""
        pass

    def fill_from_adjacency_list(self, adj_l: AdjencyList) -> Graph:
        """Wypełnianie grafu z lsity sąsiedztwa"""
        self.clear()

        size = len(adj_l)
        self.add_nodes(size)

        for node, neighbours in adj_l.items():
            for neighbour in neighbours:
                self.connect(node, neighbour)
        return self

    @abstractmethod
    def fill_from_adjacency_matrix(self, adj_m: AdjencyMatrix) -> Graph:
        """Wypełnianie grafu z macierzy sąsiedztwa"""
        pass

    @abstractmethod
    def fill_from_incidence_matrix(self, inc_m: IncidenceMatrix) -> Graph:
        """Wypełnianie grafu z macierzy incydencji"""
        pass

    def __str__(self) -> str:
        s = ""
        for k, v in self.to_adjacency_list().items():
            s += f"{k}: {v}\n"
        return s

    def get_edges(self) -> str:
        l = [f"{edge.begin} -> {edge.end} w:{edge.weight}\n" for edge in self.edges]
        return "".join(l)

    @abstractmethod
    def save(
        self, filename: str, file_format: str = "g", engine: str = "circo"
    ) -> None:
        """Zapisz graf w różnych formatach
            g - lista sąsiedztwa
            gv - dot format
            png - plik graficzny http://www.graphviz.org/
                engine = dot, neato, circo ...
        """
        pass

    def load(self, filename: str) -> None:
        """Wczytaj graf z pliku w formacie .g"""
        print('Wczytywanie grafu z pliku "{}"'.format(filename))
        self.clear()

        with open(filename, "r") as f:
            # Pierwsza linia - liczba wierzchołków
            size = int(f.readline())
            self.add_nodes(size)

            # Pozostałe linie - krawędzie
            for l in f:
                l1, l2 = l.split(" ")
                self.connect(int(l1), int(l2))

    def add_random_edges(self, count=1):
        """Tworzy określoną ilość losowych krawędzi"""
        if len(self.edges) + count > len(self) * (len(self) - 1) / 2:
            raise ValueError(
                f"Zbyt duża liczba krawędzi dla grafu prostego o {len(self)} wierzchołkach"
            )
        c = 0
        while c < count:
            n1 = random.randint(1, len(self))
            n2 = random.randint(1, len(self))

            if n1 != n2 and not self.is_connected(n1, n2):
                self.connect(n1, n2)
                c += 1

    def connect_random(self, p):
        """
        Łączy wierzchołki tak, aby prawdopodobieństwo istnienia krawędzi
        między dowolnymi dwoma wierzchołkami wynosiło p
        iteracja po każdej kombinacji bez powtórzeń 2 wierzchołków
        """
        for n1, n2 in itertools.combinations(self.nodes, 2):
            if random.random() < p:
                self.connect(n1, n2)

    def graph_sequence(self):
        """Zwraca ciąg graficzny"""
        return sorted([len(v) for v in self.to_adjacency_list().values()], reverse=True)

    def components(self):
        """Zwraca słownik złożony z wierzchołków i spójnych składowych do których należą"""
        g = self.to_adjacency_list()

        nr = 0  # nr spójnej składowej
        comp = {v: -1 for v in g}
        for v in g:
            if comp[v] == -1:
                nr += 1
                comp[v] = nr
                self.components_r(nr, v, comp, g)
        return comp

    def components_r(self, nr, v, comp, g):
        """Rekursywne przeszukiwanie wgłąb"""
        for u in g[v]:
            if comp[u] == -1:
                comp[u] = nr
                self.components_r(nr, u, comp, g)

    def largest_component(self):
        """Zwraca największą spójną składową"""
        comp = self.components()
        comp_list = [[] for _ in range(max(comp.values()))]
        for v, c in comp.items():
            comp_list[c - 1].append(v)
        return max(comp_list, key=len)

    def fill_from_graph_sequence(self, seq):
        """Tworzenie grafu z ciągu graficznego"""
        if is_valid_graph_sequence(seq):
            self.__init__(len(seq))
            degree_list = [[v + 1, d] for v, d in enumerate(seq)]
            while True:
                degree_list.sort(key=lambda x: x[1], reverse=True)
                degree_list = [[v, d] for v, d in degree_list if d != 0]
                if len(degree_list) == 0:
                    break
                for i in range(1, degree_list[0][1] + 1):
                    self.connect(degree_list[0][0], degree_list[i][0])
                    degree_list[0][1] -= 1
                    degree_list[i][1] -= 1
            return self
        else:
            raise ValueError("Niepoprawny ciąg graficzny")

    def randomize(self, n_switches):
        """Losowo zamienia krawędzie: a-b c-d -> a-d b-c"""
        while n_switches > 0:
            # edges = tuple(self.edges)
            r1 = random.choice(tuple(self.edges))
            a, b = r1.begin, r1.end
            r2 = random.choice(tuple(self.edges))
            c, d = r2.begin, r2.end
            if a == d or b == c:
                continue
            if self.is_connected(a, d) or self.is_connected(b, c):
                continue
            self.disconnect(a, b)
            self.disconnect(c, d)
            self.connect(a, d)
            self.connect(b, c)
            n_switches -= 1

    def is_connected_graph(self):
        """Czy jest to graf spójny"""
        comp = self.components()
        for v in comp.values():
            if v != 1:
                return False
        return True

    def is_eulerian(self):
        """Czy jest to graf Eulerowski"""
        if self.is_connected_graph():
            for d in self.graph_sequence():
                if d % 2 == 1:
                    return False
            return True
        else:
            return False


class SimpleGraph(Graph):

    def node_neighbours(self, node: Node) -> Set[Node]:
        """Returns Nodes adjecent to a given node """
        return set([edge.end for edge in self.node_edges(node)])

    def node_edges(self, node: Node) -> Set[Edge]:
        """Returns set of edges adjacent to the given node """
        return set([edge for edge in self.get_all_possible_edges() if edge.begin == node])
    
    def node_degree(self, node: Node) -> int:
        """Returns degree of a selected node """
        return len(self.node_edges(node))

    def get_all_possible_edges(self) -> Set[Edge]:
        all_possible = set()
        all_possible.update(self.edges)
        all_possible.update(
            [Edge(edge.end, edge.begin, edge.weight) for edge in self.edges]
        )
        return all_possible

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
