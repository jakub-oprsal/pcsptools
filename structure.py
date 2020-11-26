import itertools
from collections import namedtuple

Structure = namedtuple("Structure", ["domain","relations"])

## HELPERS

def transpose(matrix):
    return tuple(zip(*matrix))

def power_relation(relation, exponent):
    yield from map(transpose, itertools.product(relation, repeat=exponent))

def product_relation(*args, repeat=1):
    yield from map(transpose, itertools.product(*args, repeat=repeat))

## FUNCTIONS

def new(*args):
    return Structure(*args)

def power(structure, n):
    power_domain = itertools.product(structure.domain, repeat=n)
    power_rels = tuple(
        map(lambda rel: power_relation(rel,n), structure.relations))

    return Structure(power_domain,power_rels)

def product(*args):
    prod_domain = product(*[struc.domain for struc in args])
    prod_rels = tuple( map(transpose, product(*arg_rels))
        for arg_rels in zip(*[struc.relations for struc in args]) )

    return Structure(prod_domain, prod_rels)

def cache(structure):
    domain = set(structure.domain)
    relations = tuple(set(rel) for rel in structure.relations)

    return Structure(domain, relations)
