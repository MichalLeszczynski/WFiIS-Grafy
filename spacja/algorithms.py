"""Algorytmy działające na grafach"""
import copy
import random
from typing import List
from .graph import Node
from .simple_graph import SimpleGraph


def find_eulerian_trail(g) -> List[Node]:
    """Znajduje losowy cykl Eulera w grafie"""
    if not g.is_eulerian():
        raise ValueError("Nie jest to graf Eulerowski\n{}".format(g))

    solution = []
    stack = []
    stack.append(random.choice(tuple(g.nodes)))
    while len(stack) != 0:
        current_vertex = stack[-1]
        if g.node_degree(current_vertex) == 0:
            solution.append(current_vertex)
            stack.pop()
        else:
            next_vertex = random.choice(tuple(g.node_edges(current_vertex))).end
            g.disconnect(current_vertex, next_vertex)
            stack.append(next_vertex)
    return solution


def find_hamiltonian_circuit(g) -> List[Node]:
    """Znajduje losowy cykl Hamiltona w grafie"""
    g = copy.deepcopy(g)
    if not g.is_connected_graph():
        raise ValueError("Graf nie jest spójny")
    stack = []
    stack.append(random.choice(tuple(g.nodes)))
    solution = hamilton_search_r(g, stack)
    return solution


def hamilton_search_r(g, stack) -> List[Node]:
    # Zawiera wszystkie wierzcholki
    if set(stack) == g.nodes:
        # Istnieje połączenie między pierwszym a ostatnim
        if g.is_connected(stack[0], stack[-1]):
            return stack
        else:
            stack.pop
            return None
    else:
        for neighbour in g.node_neighbours(stack[-1]):
            if neighbour in stack:
                continue
            stack.append(neighbour)
            if hamilton_search_r(g, stack):
                return stack
    raise ValueError("Nie jest to graf Hamiltonowski\n{}".format(g))
