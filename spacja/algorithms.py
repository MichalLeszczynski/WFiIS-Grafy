"""Algorytmy działające na grafach"""
import copy
import random
from .simple_graph import SimpleGraph


def find_eulerian_trail(g):
    """Znajduje losowy cykl Eulera w grafie"""
    g = copy.deepcopy(g)
    if g.is_eulerian():
        solution = []
        stack = []
        stack.append(random.randint(1, len(g)))
        while len(stack) != 0:
            v = stack[-1]
            if len(g.g[v]) == 0:
                solution.append(v)
                stack.pop()
            else:
                w = random.choice(tuple(g.g[v]))
                g.disconnect(v, w)
                stack.append(w)
        return solution
    else:
        raise ValueError("Nie jest to graf Eulerowski\n{}".format(g))


def find_hamiltonian_circuit(g):
    """Znajduje losowy cykl Hamiltona w grafie"""
    g = copy.deepcopy(g)
    if not g.is_connected_graph():
        raise ValueError("Graf nie jest spójny")
    stack = []
    stack.append(random.randint(1, len(g)))
    solution = hamilton_search_r(g, stack)
    return solution


def hamilton_search_r(g, stack):
    # Zawiera wszystkie wierzcholki
    if sorted(stack) == sorted([v for v, _ in g.g.items()]):
        # Istnieje połączenie między pierwszym a ostatnim
        if g.is_connected(stack[0], stack[-1]):
            return stack
        else:
            stack.pop
            return None
    else:
        for neighbour in g.g[stack[-1]]:
            if neighbour in stack:
                continue
            stack.append(neighbour)
            if hamilton_search_r(g, stack):
                return stack
    raise ValueError("Nie jest to graf Hamiltonowski\n{}".format(g))
