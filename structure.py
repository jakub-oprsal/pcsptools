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
    def __init__(self, domain, relations):
        self.domain = frozenset(domain)
        self.relations = tuple(frozenset(relation) for relation in relations)

    @cached_property
    def type(self):
        return tuple(map(arity_of, self.relations))

    def ___or___(self, other):
        return product_structure(self, other)


def product_relation(*args, repeat=1):
    yield from map(transpose, itertools.product(*args, repeat=repeat))


def product_structure(*args):
    prod_domain = itertools.product(*(struc.domain for struc in args))
    prod_rels = tuple(
        product_relation(*arg_rels)
        for arg_rels in zip(*(struc.relations for struc in args)))

    return Structure(prod_domain, prod_rels)


def power_structure(structure, k):
    power_domain = itertools.product(structure.domain, repeat=k)
    power_rels = tuple(
        map(lambda rel: product_relation(rel, repeat=k), structure.relations))

    return Structure(power_domain, power_rels)
