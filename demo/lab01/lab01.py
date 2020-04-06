#!/usr/bin/env python3

import argparse
import sys
from pprint import pprint

sys.path.insert(0, "../..")
from spacja.simple_graph import SimpleGraph


def main():
    parser = argparse.ArgumentParser(
        description="Utility to generate simple graphs, and load/safe them from/to file."
    )
    parser.add_argument("--load", help="Load a graph from file")
    parser.add_argument("-n", help="Generate graph with N vertices")

    parser.add_argument("-l", help="Generate graph with L edges")
    parser.add_argument(
        "-p", help="Generate graph with P probability of each edge existence"
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

    print("\nTo adjacency list:")
    pprint(g.to_adjacency_list())
    print("\nTo adjacency matrix:")
    pprint(g.to_adjacency_matrix())
    print("\nTo incidence matrix:")
    pprint(g.to_incidence_matrix())

    save_if_needed(g, args)


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
    return g


def save_if_needed(g, args):
    if args.save:
        for format in args.save[0]:
            g.save("lab01", file_format=format)


if __name__ == "__main__":
    main()
