import itertools
from functools import cached_property


def transpose(matrix):
    return tuple(zip(*matrix))


def arity_of(relation):
    rel = iter(relation)
    try:
        arity = len(next(rel))
    except StopIteration:
        return None

    if not all(arity == len(edge) for edge in rel):
        raise IndexError
    return arity


def domain_of(relation):
    domain = set()
    for edge in relation:
        domain = domain.union(edge)
    return domain


class Structure:
    def __init__(self, *relations, domain=None):
        self.relations = tuple(tuple(relation) for relation in relations)
        if domain is not None:
            self.domain = tuple(domain)
        else:
            self.domain = tuple(set().union(*map(domain_of, self.relations)))

    @cached_property
    def type(self):
        return tuple(map(arity_of, self.relations))

    def power(self, exponent):
        return product_structure(self, repeat=exponent)

    def product(self, other):
        return product_structure(self, other)


def product_relation(*args, repeat=1):
    yield from map(transpose, itertools.product(*args, repeat=repeat))


def product_structure(*args, repeat=1):
    return Structure(
        *itertools.starmap(
            lambda *rels: product_relation(*rels, repeat=repeat),
            transpose(struc.relations for struc in args)),
        domain=itertools.product(*(struc.domain for struc in args), repeat=repeat))


# STRUCTURE 'CONSTANTS'

def clique(k):
    return Structure(
        ((i, j) for i in range(k) for j in range(k) if i != j),
        domain=range(k))


def cycle(n):
    if n==1:
        return loop(2)
    if n==2:
        return clique(2)
    def edges():
        for a in itertools.chain(range(0, n, 2), range(1, n, 2)):
            yield (a, (a-1) % n)
            yield (a, (a+1) % n)
    return Structure(edges(), domain=range(n))


def nae(n, arity=3):
    return Structure(
        (x for x in product(range(n), repeat=arity) if len(set(x)) > 1),
        domain=range(n))


def onein(n):
    return Structure(
        (tuple((1 if i == k else 0) for i in range(n)) for k in range(n)),
        domain=(0, 1))


def loop(*reltype, name=0):
    return Structure(
        *((tuple(name for i in range(arity)),) for arity in reltype),
        domain=(name,))
