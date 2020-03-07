import copy
import random
from .simple_graph import SimpleGraph


# TODO fix
def find_eulerian_trail(g):
    """Znajduje losowy cykl Eulera w grafie"""
    g = copy.deepcopy(g)
    if g.is_eulerian():
        solution = []
        stack = []
        v = random.randint(1, len(g))
        first = v
        while True:
            while len(g.g[v]) != 0:
                w = random.choice(tuple(g.g[v]))
                stack.append(w)
                g.disconnect(v, w)
                v = w
            if len(stack) != 0:
                v = stack.pop()
                solution.append(v)
            else:
                break
        solution.append(first)
        return solution
    else:
        raise ValueError("Nie jest to graf Eulerowski\n{}".format(g))


def find_hamiltonian_circuit(g):
    """Znajduje losowy cykl Hamiltona w grafie"""
    g = copy.deepcopy(g)
    if not g.is_connected_graph():
        raise ValueError("Graf nie jest spójny")
    # TODO implement

