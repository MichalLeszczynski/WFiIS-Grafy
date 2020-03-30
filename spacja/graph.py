from __future__ import annotations

import itertools
import random
import os
from typing import Set, Dict, List, Any, Union
from abc import ABC, abstractmethod
from spacja.helper_structures import Node, Edge, Weight
from spacja.functions import is_valid_graph_sequence  # type: ignore

AdjacencyList = Dict[int, Set[int]]
AdjacencyMatrix = List[List[int]]
IncidenceMatrix = List[List[int]]


class Graph(ABC):
    def __init__(self, size=0) -> None:
        self.nodes: Set[Node] = set()
        self.edges: Set[Edge] = set()
        self.separator = ""

        self.clear()
        self.add_nodes(count=size)

    def add_nodes(self, count=1) -> None:
        """Tworzy nowe wierzchołki"""
        for i in range(len(self) + 1, len(self) + 1 + count):
            self.nodes.add(Node(i))

    def __len__(self) -> int:
        return len(self.nodes)

    def __str__(self) -> str:
        s = ""
        for k, v in self.to_adjacency_list().items():
            s += f"{k}: {v}\n"
        return s

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()

    def is_weighted_graph(self) -> bool:
        return any(edge.weight != 1 for edge in self.edges)

    @abstractmethod
    def get_all_possible_edges(self) -> Set[Edge]:
        """Returns edges that are all possible moves from edge.begin to edge.end
            Especially usable in simple graphs
        """

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

    @abstractmethod
    def connect(
        self, node1: Union[Node, int], node2: Union[Node, int], weight: Weight = 1
    ) -> None:
        """Tworzy krawędż między wierzchołkiem node1 a node2"""

    @abstractmethod
    def disconnect(self, node1: Union[Node, int], node2: Union[Node, int]) -> None:
        """Usuwa krawędż między wierzchołkiem node1 a node2"""

    @abstractmethod
    def is_connected(self, node1: Union[Node, int], node2: Union[Node, int]) -> bool:
        """Czy stnieje krawędź node1 -- node2"""

    def to_adjacency_list(self) -> AdjacencyList:
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

    @abstractmethod
    def to_adjacency_matrix(self) -> AdjacencyMatrix:
        """Zwraca graf w postaci macierzy sąsiedztwa"""

    @abstractmethod
    def to_incidence_matrix(self) -> IncidenceMatrix:
        """Zwraca graf w postaci macierzy incydencji"""

    def fill_from_adjacency_list(self, adj_l: AdjacencyList) -> Graph:
        """Wypełnianie grafu z lsity sąsiedztwa"""
        self.clear()

        size = len(adj_l)
        self.add_nodes(size)

        for node, neighbours in adj_l.items():
            for neighbour in neighbours:
                self.connect(node, neighbour)
        return self

    @abstractmethod
    def fill_from_adjacency_matrix(self, adj_m: AdjacencyMatrix) -> Graph:
        """Wypełnianie grafu z macierzy sąsiedztwa"""

    @abstractmethod
    def fill_from_incidence_matrix(self, inc_m: IncidenceMatrix) -> Graph:
        """Wypełnianie grafu z macierzy incydencji"""

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
                    label = (
                        f'[label="{edge.weight}",weight="{edge.weight}"]'
                        if self.is_weighted_graph()
                        else ""
                    )
                    n1 = edge.begin.index
                    n2 = edge.end.index
                    f.write(f"{n1} {self.separator} {n2}{label}\n")
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

    def add_random_edges(self, count: int = 1) -> None:
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

    def connect_random(self, p: int):
        """
        Łączy wierzchołki tak, aby prawdopodobieństwo istnienia krawędzi
        między dowolnymi dwoma wierzchołkami wynosiło p
        iteracja po każdej kombinacji bez powtórzeń 2 wierzchołków
        """
        for n1, n2 in itertools.combinations(self.nodes, 2):
            if random.random() < p:
                self.connect(n1, n2)

    def graph_sequence(self) -> List[int]:
        """Zwraca ciąg graficzny"""
        return sorted([len(v) for v in self.to_adjacency_list().values()], reverse=True)

    def components(self) -> Dict[int, int]:
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

    def components_r(
        self, nr: int, v: int, comp: Dict[int, int], g: AdjacencyList
    ) -> None:
        """Rekursywne przeszukiwanie wgłąb"""
        for u in g[v]:
            if comp[u] == -1:
                comp[u] = nr
                self.components_r(nr, u, comp, g)

    def largest_component(self) -> List[int]:
        """Zwraca największą spójną składową"""
        comp = self.components()
        comp_list: List[List[int]] = [[] for _ in range(max(comp.values()))]
        for v, c in comp.items():
            comp_list[c - 1].append(v)
        return max(comp_list, key=len)

    def fill_from_graph_sequence(self, seq: List[int]) -> Graph:
        """Tworzenie grafu z ciągu graficznego"""
        if is_valid_graph_sequence(seq):
            self.clear()
            self.add_nodes(len(seq))
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

    def randomize(self, n_switches: int) -> None:
        """Losowo zamienia krawędzie: a-b c-d -> a-d b-c"""
        while n_switches > 0:
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

    def is_connected_graph(self) -> bool:
        """Czy jest to graf spójny"""
        comp = self.components()
        for v in comp.values():
            if v != 1:
                return False
        return True

    def is_eulerian(self) -> bool:
        """Czy jest to graf Eulerowski"""
        if self.is_connected_graph():
            for d in self.graph_sequence():
                if d % 2 == 1:
                    return False
            return True
        else:
            return False

    def give_random_weights(self, max_weight=10):
        for edge in self.edges:
            edge.weight = random.randint(1, max_weight)
