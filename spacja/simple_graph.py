#!/usr/bin/env python3

import itertools
import os
import random
import numpy as np
from .functions import is_valid_graph_sequence


class SimpleGraph:
    """
    Graf prosty, wewnętrznie reprezentowany jako lista sąsiedztwa.
    Wierzchołki numerowane od 1 zgodnie z konwencją matematyczną.
    """

    def __init__(self, size=0):
        # Tworzymy słownik, gdzie kluczem jest numer wierzchołka
        # a wartością zbiór numerów wierzchołków, z którymi sąsiaduje
        self.g = {}

        # Tworzymy zadaną liczbę wierzchołków
        self.add_nodes(count=size)

    def __len__(self):
        return len(self.g)

    def __str__(self):
        s = ""
        for k, v in self.g.items():
            s += "{}: {}\n".format(k, v)
        return s

    def clear(self):
        self.g = {}

    def save(self, filename, file_format="g", engine="circo"):
        """Zapisz graf w różnych formatach
            g - lista sąsiedztwa
            gv - dot format
            png - plik graficzny http://www.graphviz.org/
                engine = dot, neato, circo ...
        """
        if file_format == "g":
            filename += ".g"
            print('Zapisywanie grafu do pliku "{}"'.format(filename))
            with open(filename, "w") as f:
                f.write("{}\n".format(len(self)))
                for n1, n2 in self.edges():
                    f.write("{} {}\n".format(n1, n2))

        elif file_format == "gv":
            filename += ".gv"
            with open(filename, "w") as f:
                f.write("graph g {\n")
                for n1, n2 in self.edges():
                    f.write("{} -- {}\n".format(n1, n2))
                f.write("}\n")

        elif file_format == "png":
            self.save(filename, file_format="gv")
            os.system("dot -T png -K {} -O {}".format(engine, filename + ".gv"))
            os.system("rm {}".format(filename + ".gv"))

    def load(self, filename):
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

    def edges(self):
        """Zbiór wszystkich istniejących krawędzi"""
        edges = set()
        for vertex in self.g:
            for neighbour in self.g[vertex]:
                # Graf nieskierowany, nie podajemy duplikatów
                if vertex < neighbour:
                    edges.add((vertex, neighbour))
        return edges

    def add_nodes(self, count=1):
        """Tworzy nowe wierzchołki"""
        for i in range(len(self) + 1, len(self) + 1 + count):
            self.g[i] = set()

    def connect(self, node1, node2):
        """Tworzy krawędż między wierchołkiem node1 a node2"""
        if node1 not in self.g or node2 not in self.g or node1 == node2:
            raise ValueError

        self.g[node1].add(node2)
        self.g[node2].add(node1)

    def disconnect(self, node1, node2):
        """Usuwa krawędż między wierzchołkiem node1 a node2"""
        if node1 not in self.g or node2 not in self.g or node1 == node2:
            raise ValueError

        self.g[node1].remove(node2)
        self.g[node2].remove(node1)

    def add_random_edges(self, count=1):
        """Tworzy określoną ilość losowych krawędzi"""
        if len(self.edges()) + count > len(self) * (len(self) - 1) / 2:
            raise ValueError(
                "Zbyt duża liczba krawędzi dla grafu prostego o {} wierzchołkach".format(
                    len(self)
                )
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
        for n1, n2 in itertools.combinations(self.g.keys(), 2):
            if random.random() < p:
                self.connect(n1, n2)

    def is_connected(self, node1, node2):
        """Czy stnieje krawędź node1 -- node2"""
        return node2 in self.g[node1]

    def adjacency_matrix(self):
        """Zwraca graf w postaci macierzy sąsiedztwa"""
        adj_m = np.zeros(shape=(len(self), len(self)))
        for n1, n2 in self.edges():
            adj_m[n1 - 1][n2 - 1] = 1
            adj_m[n2 - 1][n1 - 1] = 1
        return adj_m

    def incidence_matrix(self):
        """Zwraca graf w postaci macierzy incydencji"""
        edges = self.edges()
        inc_m = np.zeros(shape=(len(self), len(edges)))

        for i, (n1, n2) in enumerate(edges):
            inc_m[n1 - 1][i] = 1
            inc_m[n2 - 1][i] = 1
        return inc_m

    def graph_sequence(self):
        """Zwraca ciąg graficzny"""
        return [len(v) for v in self.g.values()]

    def components(self):
        """Zwraca słownik złożony z wierzchołków i spójnych składowych do których należą"""
        nr = 0  # nr spójnej składowej
        comp = {v: -1 for v in self.g}
        for v in self.g:
            if comp[v] == -1:
                nr += 1
                comp[v] = nr
                self.components_r(nr, v, comp)
        return comp

    def components_r(self, nr, v, comp):
        """Rekursywne przeszukiwanie wgłąb"""
        for u in self.g[v]:
            if comp[u] == -1:
                comp[u] = nr
                self.components_r(nr, u, comp)

    def largest_component(self):
        """Zwraca największą spójną składową"""
        comp = self.components()
        comp_list = [[] for _ in range(max(comp.values()))]
        for v, c in comp.items():
            comp_list[c - 1].append(v)
        return max(comp_list, key=len)

    def from_adjacency_matrix(self, adj_m):
        """Wypełnianie grafu z macierzy sąsiedztwa"""
        self.clear()

        size = len(adj_m)
        self.add_nodes(size)

        for n1 in range(len(self)):
            for n2 in range(len(self)):
                # patrzymy tylko na elementy pod przekątną
                if n1 < n2 and adj_m[n1][n2]:
                    # mapowanie numerów wierzchołków: n-1 -> n
                    self.connect(n1 + 1, n2 + 1)
        return self

    def from_incidence_matrix(self, inc_m):
        """Wypełnianie grafu z macierzy incydencji"""
        self.clear()

        size = len(inc_m)
        self.add_nodes(size)

        for i in range(len(inc_m[0])):
            edge = []
            for n in range(len(self)):
                # szukamy 1 w kolumnie
                if inc_m[n][i]:
                    edge.append(n)
            # mapowanie numerów wierzchołków: n-1 -> n
            self.connect(edge[0] + 1, edge[1] + 1)
        return self

    def from_graph_sequence(self, seq):
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
            edges = tuple(self.edges())
            a, b = random.choice(edges)
            c, d = random.choice(edges)
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
