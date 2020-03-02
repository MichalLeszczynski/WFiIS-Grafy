#!/usr/bin/env python3
import itertools
import os
import random

# Propozycja biblioteki do obsługi grafów


def matrix2d(h, w):
    # zwraca macierz h x w wypełnioną zerami
    return [[0 for _ in range(w)] for _ in range(h)]


def print2d(m):
    # "ładne" wypisanie macierzy 2d
    for l in m:
        # aby użyć funkcji 'join' zamieniamy int na str
        print("\t".join([str(n) for n in l]))


class Graph:
    """Obiekt reprezentujący graf nieskierowany.
       Wewnętrznie jest przedstawiony jako lista sąsiedztwa."""

    def __init__(self, size=0):
        # size - liczba wierzchołków w grafie
        self.size = 0

        # tworzymy słownik, gdzie kluczem jest numer wierzchołka
        # a wartością zbiór numerów wierzchołków, z którymi sąsiaduje
        self.g = {}

        # tworzymy zadaną liczbę wierzchołków
        self.create_nodes(size)

    def __len__(self):
        return self.size

    def clear(self):
        # czyszczenie grafu
        self.g = {}
        self.size = 0

    def save(self, filename):
        print('zapisywanie grafu do pliku "{}"'.format(filename))
        with open(filename, "w") as f:
            f.write("{}\n".format(self.size))
            for n1, n2 in self.edges():
                f.write("{} {}\n".format(n1, n2))

    def load(self, filename):
        print('ładowanie grafu z pliku "{}"'.format(filename))
        self.clear()

        with open(filename, "r") as f:
            # pierwsza linia - liczba wierzchołków
            size = int(f.readline())
            self.create_nodes(size)

            # pozostałe linie - krawędzie
            for l in f:
                l1, l2 = l.split(" ")
                self.create_edge(int(l1), int(l2))

    def save_dot(self, filename, engine="dot"):
        # engine: http://www.graphviz.org/
        # dot, neato, circo
        with open(filename, "w") as f:
            f.write("graph g {\n")
            for n1, n2 in self.edges():
                f.write("{} -- {}\n".format(n1, n2))
            f.write("}\n")
        os.system("dot -Tpng -K{} -O {}".format(engine, filename))

    def edges(self):
        # zbiór wszystkich istniejących krawędzi
        edges = set()
        for n in self.g:
            for m in self.g[n]:
                # graf nieskierowany, nie podajemy duplikatów
                if n < m:
                    edges.add((n, m))
        return edges

    def create_nodes(self, count=1):
        # tworzy nowe wierzchołki
        for _ in range(count):
            self.size += 1
            self.g[self.size] = set()

    def create_edge(self, node1, node2):
        # tworzy krawędż między wierchołkiem node1 a node2
        assert node1 in self.g
        assert node2 in self.g
        assert node1 != node2

        self.g[node1].add(node2)
        self.g[node2].add(node1)

    def create_random_edges(self, count=1):
        # tworzy określoną ilość losowych krawędzi
        c = 0
        while c < count:
            n1 = random.randint(1, self.size)
            n2 = random.randint(1, self.size)

            if n1 != n2 and not self.has_edge(n1, n2):
                self.create_edge(n1, n2)
                c += 1

    def connect_random(self, p):
        # łączy wierzchołki tak, aby prawdopodobieńswto istanienia krawędzi
        # między dowolnymi dwoma wierzchołkami wynosiło p
        # iteracja po każdej kombinacji bez powtórzeń 2 wierzchołków
        for n1, n2 in itertools.combinations(self.g.keys(), 2):
            if random.random() < p:
                self.create_edge(n1, n2)

    def has_edge(self, node1, node2):
        # czy stnieje krawędź node1 -- node2
        return node2 in self.g[node1]

    def adj_matrix(self):
        # zwraca graf w postaci macierzy sąsiedztwa
        adj_m = matrix2d(self.size, self.size)
        for n1, n2 in self.edges():
            # mapowanie numerów wierzchołków z 1 do n na 0 do n - 1
            n1, n2 = n1 - 1, n2 - 1
            adj_m[n1][n2] = 1
            adj_m[n2][n1] = 1
        return adj_m

    def from_adj_matrix(self, adj_m):
        # wypełnianie grafu z macierzy sąsiedztwa
        self.clear()

        size = len(adj_m)
        self.create_nodes(size)

        for n1 in range(self.size):
            for n2 in range(self.size):
                # patrzymy tylko na elementy pod przekątną
                if n1 < n2 and adj_m[n1][n2]:
                    # mapowanie numerów wierzchołków: n-1 -> n
                    self.create_edge(n1 + 1, n2 + 1)

    def inc_matrix(self):
        # zwraca graf w postaci macierzy incydencji
        edges = self.edges()
        inc_m = matrix2d(self.size, len(edges))

        for i, (n1, n2) in enumerate(edges):
            # mapowanie numerów wierzchołków: n -> n-1
            n1, n2 = n1 - 1, n2 - 1
            inc_m[n1][i] = 1
            inc_m[n2][i] = 1
        return inc_m

    def from_inc_matrix(self, inc_m):
        # wypełnianie grafu z macierzy incydencji
        self.clear()

        size = len(inc_m)
        self.create_nodes(size)

        for i in range(len(inc_m[0])):
            edge = []
            for n in range(self.size):
                # szukamy 1 w kolumnie
                if inc_m[n][i]:
                    edge.append(n)
            # mapowanie numerów wierzchołków: n-1 -> n
            self.create_edge(edge[0] + 1, edge[1] + 1)
