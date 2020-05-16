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
        with open("P.tmp", "a") as f:
            f.write(f"{length:.3f}, {P}\n")


def example06():
    g = gb.get_random_2D_graph(size=50)
    P = None
    for _ in range(100):
        P = simulated_annealing(g, save=True, P=P)
        length = circuit_length(g.to_adjacency_matrix(), P)
        print(f"{length:.3f}")


def example07():
    g = SimpleGraph().from_coordinates("input.dat")
    P = [
        45,
        180,
        181,
        106,
        14,
        115,
        174,
        9,
        22,
        135,
        125,
        42,
        28,
        90,
        182,
        46,
        70,
        149,
        98,
        168,
        148,
        66,
        123,
        200,
        30,
        11,
        27,
        117,
        109,
        20,
        146,
        78,
        167,
        175,
        57,
        55,
        141,
        192,
        136,
        1,
        58,
        39,
        93,
        31,
        119,
        33,
        19,
        122,
        82,
        65,
        12,
        131,
        6,
        195,
        29,
        40,
        16,
        69,
        114,
        159,
        177,
        52,
        153,
        152,
        18,
        8,
        110,
        130,
        108,
        162,
        196,
        102,
        140,
        197,
        47,
        170,
        41,
        126,
        101,
        133,
        188,
        164,
        134,
        50,
        112,
        184,
        37,
        49,
        95,
        34,
        44,
        186,
        61,
        120,
        169,
        178,
        97,
        100,
        43,
        77,
        150,
        85,
        68,
        198,
        80,
        63,
        25,
        75,
        13,
        137,
        160,
        138,
        38,
        79,
        183,
        185,
        48,
        92,
        132,
        54,
        24,
        36,
        72,
        53,
        127,
        144,
        94,
        113,
        194,
        23,
        2,
        67,
        74,
        26,
        179,
        156,
        64,
        158,
        166,
        89,
        143,
        187,
        190,
        103,
        139,
        91,
        151,
        142,
        165,
        62,
        154,
        161,
        71,
        171,
        173,
        7,
        35,
        84,
        105,
        88,
        59,
        193,
        83,
        145,
        147,
        5,
        124,
        15,
        128,
        4,
        104,
        99,
        111,
        157,
        60,
        87,
        199,
        189,
        116,
        96,
        86,
        51,
        56,
        155,
        118,
        129,
        17,
        176,
        32,
        10,
        172,
        121,
        73,
        21,
        76,
        191,
        107,
        3,
        81,
        163,
    ]
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
