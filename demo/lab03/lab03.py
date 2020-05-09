#!/usr/bin/env python3

import sys
import copy
import argparse
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import (
    find_shortest_path_dijkstra,
    get_distances_to_nodes_matrix,
    get_graph_center,
    get_minimax_graph_center,
    get_minimum_spanning_tree_kruskal,
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

    print("\nDijkstra:")
    distances, predecessors = find_shortest_path_dijkstra(g, tuple(g.nodes)[0])

    print("Odleglosci od wierzcholka:")
    pprint(distances)
    print("\nPoprzednicy wierzcholkow:")
    pprint(predecessors)
    print("\nSciezki:")
    pprint(get_all_trails_from_predecessors(predecessors))

    print("\nMacierz odleglosci:")
    distances_matrix = get_distances_to_nodes_matrix(g)
    for l in distances_matrix:
        print(*l, sep="\t")

    print(f"\nCentrum grafu: {get_graph_center(g)}")

    print(f"\nMinimaxowe centrum grafu: {get_minimax_graph_center(g)}")

    mst = get_minimum_spanning_tree_kruskal(g)
    print("\nMinimalne drzewo rozpinające (szukane algorytmem kruskala):")
    print(mst)

    mst.save("lab03_mst", "am")
    mst.save("lab03_mst", "png", color_components=True)


def load_graph_to_work_on(args):
    g = SimpleGraph()

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
            g.save("lab03", file_format=format, color_components=True)


if __name__ == "__main__":
    main()
