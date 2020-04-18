#!/usr/bin/env python3

import argparse
import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.directed_graph import DirectedGraph
from spacja.algorithms import (
    find_shortest_path_bellman_ford,
    get_distances_to_nodes_matrix,
    johnson_get_distances_to_nodes_matrix,
)
from spacja.functions import get_all_trails_from_predecessors


def main():
    parser = argparse.ArgumentParser(
        description="Utility to generate directed graphs, and load/safe them from/to file."
    )
    parser.add_argument("--load", help="Load a graph from file")
    parser.add_argument("-n", help="Generate graph with N vertices")

    parser.add_argument("-l", help="Generate graph with L edges")
    parser.add_argument(
        "-p", help="Generate graph with P probability of each edge existence"
    )
    parser.add_argument(
        "-w",
        nargs="*",
        help="Add weights to graph (pass two numbers to set min and max weight)",
        action="append",
    )
    parser.add_argument(
        "-c", help="Ensure, that generated graph is connected", action="store_true"
    )

    parser.add_argument(
        "--save",
        nargs="*",
        help="Save graph to a specified format (am, al, im)",
        action="append",
    )

    args = parser.parse_args()
    print(args)

    g = load_graph_to_work_on(args)
    if args.c:
        while not g.is_connected_graph():
            g = load_graph_to_work_on(args)

    save_if_needed(g, args)

    print("\nTo adjacency list:")
    pprint(g.to_adjacency_list())
    print("\nTo adjacency matrix:")
    pprint(g.to_adjacency_matrix())
    print("\nTo incidence matrix:")
    pprint(g.to_incidence_matrix())

    print("\nComponent list:")
    print(g.component_list())

    print("\nBellman-Ford:")
    distances, predecessors = find_shortest_path_bellman_ford(g, tuple(g.nodes)[0])

    print("Odleglosci od wierzcholka:")
    pprint(distances)

    print("\nPoprzednicy wierzcholkow:")
    pprint(predecessors)

    print("\nSciezki:")
    pprint(get_all_trails_from_predecessors(predecessors))

    print("\nMacierz odleglosci:")
    distances_matrix = johnson_get_distances_to_nodes_matrix(g)
    for l in distances_matrix:
        print(*l, sep="\t")


def load_graph_to_work_on(args):
    g = DirectedGraph()

    if args.load:
        g.load(args.load)

    elif args.n:
        g.add_nodes(int(args.n))
        if args.l:
            g.add_random_edges(int(args.l))
        elif args.p:
            g.connect_random(float(args.p))

    if args.w is not None:
        if args.w[0]:
            g.assign_random_weights(int(args.w[0][0]), int(args.w[0][1]))
        else:
            g.assign_random_weights()
    return g


def save_if_needed(g, args):
    if args.save:
        for format in args.save[0]:
            g.save("lab04", file_format=format)


if __name__ == "__main__":
    main()
