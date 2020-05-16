#!/usr/bin/env python3
import sys
import re
import time
from ast import literal_eval

sys.path.insert(0, "../..")

from spacja.directed_graph import DirectedGraph
from spacja.simple_graph import SimpleGraph
from spacja.graph_builder import GraphBuilder as gb
from spacja.algorithms import page_rank, simulated_annealing, circuit_length
from spacja.functions import number_to_alpha


def alpha_to_adjacency_list(l):
    l = re.sub(r"\d", "", l)
    l = re.sub(r":(.*)\n", r":{\g<1>},\n", l)
    l = re.sub(r"\s", "", l)
    l = f"{{{l}}}"
    return literal_eval(alpha_to_numbers(l))


def alpha_to_numbers(string):
    alph = "ABCDEFGHIJKLMNOPQRSTUWXYZ"
    result = ""
    for c in string:
        if c in alph:
            result += str(alph.index(c) + 1)
        else:
            result += c
    return result


def display_pagerank(rank):
    rank_list = sorted(rank.items(), key=lambda x: x[1], reverse=True)
    for node, score in rank_list:
        print(f"{number_to_alpha(node)} ==> PageRank = {score:.6f}")


def example01():
    g = DirectedGraph().from_adjacency_list(adjacency_list_1)
    print(g)
    rank = page_rank(g, algorithm="random_walk")
    display_pagerank(rank)
    g.save(
        "pr_random_walk_1",
        "png",
        engine="dot",
        color_components=True,
        alphabetical=True,
    )


def example02():
    g = DirectedGraph().from_adjacency_list(adjacency_list_2)
    print(g)
    rank = page_rank(g, algorithm="random_walk")
    display_pagerank(rank)
    g.save(
        "pr_random_walk_2",
        "png",
        engine="dot",
        color_components=True,
        alphabetical=True,
    )


def example03():
    g = DirectedGraph().from_adjacency_list(adjacency_list_1)
    print(g)
    rank = page_rank(g, algorithm="matrix")
    display_pagerank(rank)
    g.save("pr_matrix_1", "png", engine="dot", color_components=True, alphabetical=True)


def example04():
    g = DirectedGraph().from_adjacency_list(adjacency_list_2)
    print(g)
    rank = page_rank(g, algorithm="matrix")
    display_pagerank(rank)
    g.save("pr_matrix_2", "png", engine="dot", color_components=True, alphabetical=True)


def example05():
    g = SimpleGraph().from_coordinates("input.dat")
    P = None
    for MAX_IT in range(10, 201, 5):
        P = simulated_annealing(g, MAX_IT, save=True, P=P)
        length = circuit_length(g.to_adjacency_matrix(), P)
        with open("P_5.tmp", "a") as f:
            f.write(f"{length:.3f}, {P}\n")


def example06():
    g = gb.get_random_2D_graph(size=50)
    P = None
    for _ in range(100):
        P = simulated_annealing(g, save=True, P=P)
        length = circuit_length(g.to_adjacency_matrix(), P)
        with open("P_6.tmp", "a") as f:
            f.write(f"{length:.3f}, {P}\n")


def example07():
    g = SimpleGraph().from_coordinates("input.dat")
    P = None
    for _ in range(250):
        P = simulated_annealing(g, MAX_IT=20, save=True, P=P)
        length = circuit_length(g.to_adjacency_matrix(), P)
        with open("P.dat", "a") as f:
            f.write(f"{length:.3f}, {P}\n")


if __name__ == "__main__":
    with open("alpha_list_1") as f:
        alpha_list_1 = f.read()
    with open("alpha_list_2") as f:
        alpha_list_2 = f.read()

    adjacency_list_1 = alpha_to_adjacency_list(alpha_list_1)
    adjacency_list_2 = alpha_to_adjacency_list(alpha_list_2)

    examples = [
        None,
        example01,
        example02,
        example03,
        example04,
        example05,
        example06,
        example07,
    ]
    if len(sys.argv) == 2:
        example = int(sys.argv[1])
        examples[example]()
    else:
        print("Nieprawidłowa liczba argumentów:\n./lab06 <numer przykładu>")
