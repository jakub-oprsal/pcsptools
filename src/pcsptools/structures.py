""" Library of predefined structures. """
from .structure import Structure
from itertools import chain, product, combinations


def clique(k):
    """The k-clique graph."""
    return Structure(
        range(k), ((i, j) for i in range(k) for j in range(k) if i != j)
    )


def cycle(n):
    """The unoriented n-cycle graph."""
    if n == 1:
        return loop(2)
    if n == 2:
        return clique(2)

    def edges():
        for a in chain(range(0, n, 2), range(1, n, 2)):
            yield (a, (a - 1) % n)
            yield (a, (a + 1) % n)

    return Structure(range(n), edges())


def ocycle(n):
    """The oriented n-cycle graph."""
    if n == 1:
        return loop(2)
    return Structure(range(n), ((i, (i + 1) % n) for i in range(n)))


def path(n):
    """The oriented path of length n."""
    return Structure(range(n + 1), ((i, (i + 1)) for i in range(n)))


def nae(n, arity=3):
    """NAE on an `n`-element set,
    optinally the arity of the relation is given."""
    return Structure(
        range(n),
        (x for x in product(range(n), repeat=arity) if len(set(x)) > 1),
    )


def onein(n):
    """The generalisation of 1in3-SAT to `n`-ary relations.
    The domain is Boolean anyway."""
    return Structure(
        (0, 1),
        (tuple((1 if i == k else 0) for i in range(n)) for k in range(n)),
    )


def tinn(t, n):
    """The generalisation of t-in-n-SAT."""
    return Structure(
        (0, 1),
        (
            tuple((1 if i in xs else 0) for i in range(n))
            for xs in combinations(range(n), t)
        ),
    )


def loop(*reltype, name=0):
    """The one-element loop structure with the given type
    (all relations are non-empty). Type has to be fully defined."""
    return Structure(
        (name,), *((tuple(name for i in range(arity)),) for arity in reltype)
    )


def affine(p, arity=3):
    """Affine equations over Z_p."""
    relations = tuple([] for i in range(p))
    for xs in product(range(p), repeat=arity):
        relations[sum(xs) % p].append(xs)
    return Structure(range(p), *relations)


def hornsat():
    relations = (
        (xs for xs in product((0, 1), repeat=3) if xs != (0, 0, 1)),
        (xs for xs in product((0, 1), repeat=3) if xs != (0, 0, 0)),
        ((0,),),
        ((1,),),
    )
    return Structure((0, 1), *relations)
