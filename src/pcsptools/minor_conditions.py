from .polymorphisms import loop_condition, sigma
from .structure import Structure
from .structures import onein, ocycle, clique


def wnu(n):
    """weak near unanimity of arity n"""
    return loop_condition(onein(n), names="w")


def qnu(n):
    """quasi near-unanimity of arity n"""
    qnu_structure = Structure(
        (0, 1),
        (tuple((1 if i == k else 0) for i in range(n)) for k in range(n + 1)),
    )
    return loop_condition(qnu_structure, names="m")


def hageman_mitschke(n):
    """Ternary Hageman-Mitschke terms for congruence n-permutability."""
    leq = Structure((0, 1), ((0, 0), (0, 1), (1, 1))).singleton_expansion()
    return sigma(path(n).expand((1,), (0,)), leq)


def siggers(n):
    """Siggers operation of arity n = 4 or 6, named 's'."""
    if n == 4:
        return loop_condition(Structure("are", zip("area", "rare")), names="s")
    elif n == 6:
        return loop_condition(clique(3), names="s")
    else:
        raise Exception("What do you mean by Siggers of arity {n}?!")


def olsak(n=2, k=3):
    """the (n^k - 2)-ary Olšák identity, the default is:
    *o(x, x, y, y, y, x) = o(x, y, x, y, x, y) = o(x, x, y, y, y, x)*."""
    return loop_condition(nae(n, arity=k), names="o")


def cyclic(p):
    """Cyclic term of arity 'p'."""
    return loop_condition(ocycle(p), names="c")
