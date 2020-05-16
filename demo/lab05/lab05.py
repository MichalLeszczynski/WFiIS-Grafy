#!/usr/bin/env python3
import os
import sys
from pprint import pprint

sys.path.insert(0, "../..")

from spacja.directed_graph import DirectedGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import ford_fulkerson


def generate_network(N):
    return gb.get_random_flow_network(N)


def prep_dir(save_dir):
    os.system(f"rm -rf {save_dir}")
    os.mkdir(save_dir)


def get_example():
    exg = DirectedGraph(11)

    s = 1
    a = 2
    b = 3
    c = 4
    d = 5
    e = 6
    f = 7
    g = 8
    h = 9
    i = 10
    t = 11

    exg.connect(s, a, 10)
    exg.connect(s, b, 3)
    exg.connect(s, c, 6)

    exg.connect(a, b, 8)
    exg.connect(a, d, 8)
    exg.connect(a, e, 6)

    exg.connect(b, e, 2)
    exg.connect(b, f, 10)

    exg.connect(c, d, 9)
    exg.connect(c, f, 1)

    exg.connect(d, h, 5)

    exg.connect(e, d, 1)
    exg.connect(e, i, 7)

    exg.connect(f, g, 9)

    exg.connect(g, t, 7)

    exg.connect(h, t, 5)

    exg.connect(i, t, 7)

    return exg


def main():
    print("Wywołanie:\n./lab05.py gen save_dir N\n./lab05.py ff save_dir")
    print("Sieć przykładowa: ./lab05.py gen example\n")

    if len(sys.argv) < 2:
        return

    if sys.argv[1] == "gen":
        save_dir = sys.argv[2]

        if save_dir == "example":
            print(f"Używanie sieci przykładowej (z input_5.pdf)")
            g = get_example()
        else:
            N = int(sys.argv[3])
            print(f"Generowanie sieci przepływowej, N={N}")
            g = generate_network(N=N)
        prep_dir(save_dir)
        g.save(save_dir + "/G", file_format="am")
        g.save(save_dir + "/G", file_format="png", engine="dot")
        print(f"Zapisano do katalogu {save_dir}")

    elif sys.argv[1] == "ff":
        save_dir = sys.argv[2]

        g = DirectedGraph()
        g.load(save_dir + "/G.am")
        # odświeżenie diagramu w razie ręcznej edycji macierzy sąsiedztwa
        g.save(save_dir + "/G", file_format="png", engine="dot")
        print(f"Odczytano sieć przepływową z katalogu {save_dir}")

        f = ford_fulkerson(g, verbose=True)

        f_max = sum(weight for ((begin, end), weight) in f.items() if begin == 1)
        print(f"maksymalny przepływ: {f_max}")

        labels = {
            (e.begin, e.end): f"{f[(e.begin, e.end)]}/{e.weight}" for e in g.edges
        }
        g.save(save_dir + "/G-ff", file_format="png", engine="dot", edge_labels=labels)


if __name__ == "__main__":
    main()
