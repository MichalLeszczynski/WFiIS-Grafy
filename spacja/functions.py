"""Pomocnicze funkcje które nie używają klasy SimpleGraph"""
from typing import List, Dict
from spacja.graph import Node

def is_valid_graph_sequence(seq):
    """Sprawdza czy z podanej listy da się utworzyć graf"""
    # Jeśli liczba wierzchołków o nieparzystym stopniu jest nieparzysta to nie jest to ciąg graficzny
    seq = list(seq)
    odds = sum(1 for d in seq if d % 2 == 1)
    if odds % 2 == 1:
        return False

    while True:
        seq.sort(reverse=True)
        # Jeśli ciąg składa się z samych zer to jest graficzny
        for d in seq:
            if d != 0:
                break
        else:
            return True

        # Niemożliwa liczba krawędzi
        if seq[0] < 0 or seq[0] >= len(seq):
            return False

        # Ujemne stopnie wierzchołków
        for d in seq:
            if d < 0:
                return False

        for i in range(1, seq[0] + 1):
            seq[i] -= 1
        del seq[0]
    return True

def get_all_trails_from_predecessors(predecessors: Dict[Node, Node]) -> Dict[Node, List[Node]]:
    trails = {}
    for node in predecessors.keys():
        trails[node] = get_trail_to_node(predecessors, node)

def get_trail_to_node(predecessors: Dict[Node, Node], node: Node) -> List[Node]:
    if predecessors[node] is None:
        return [node]
    return get_trail_to_node(predecessors, predecessors[node]) + node
