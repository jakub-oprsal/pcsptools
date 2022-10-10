'''
STRUCTURE

The `Structure` class and severel predefined structures.
'''
from itertools import product, starmap
from functools import cached_property


def transpose(matrix):
    return tuple(zip(*matrix))


def arity_of(relation):
    rel = iter(relation)
    try:
        arity = len(next(rel))
    except StopIteration:
        return None     # Empty Relation

    if not all(arity == len(edge) for edge in rel):
        raise ValueError('Ambiguous arity!')
    return arity


def domain_of(relation):
    return set().union(*relation)


class Structure:
    """ A class holding a relational structure.

        Initialises by giving as arguments (domain, relation_1, etc.). Each
        relation is supposed to be an iterative through tuples of elements of
        the domain."""
    def __init__(self, domain, *relations):
        self.domain = tuple(domain)
        self.relations = tuple(tuple(relation) for relation in relations)

    @cached_property
    def type(self):
        return tuple(map(arity_of, self.relations))

    def check(self):
        _ = self.type  # Checks that arities are well-defined
        for relation in self.relations:
            if not domain_of(relation).issubset(self.domain):
                raise ValueError('Relation defined on a bigger domain.')
        return True

    def is_similar(self, other):
        if len(self.type) != len(other.type):
            return False        # Different number of relations
        for n, m in zip(self.type, other.type):
            if n != m and (None not in (n, m)):
                return False    # Arities do not match
        return True

    def power(self, exponent):
        return product_structure(self, repeat=exponent)

    def product(self, other):
        return product_structure(self, other)

    def expand(self, *relations):
        """ Returns an expanded structure. """
        return Structure(
            self.domain,
            *self.relations,
            *relations)

    def singleton_expansion(self):
        """ Adds singletons so that the resulting structure has a single
            automorphism. """
        return self.expand(*(((a,),) for a in self.domain))

    def __pow__(self, exponent):
        return self.power(exponent)

    def __mul__(self, other):
        return self.product(other)


def product_relation(*args, **cwargs):
    yield from map(transpose, product(*args, **cwargs))


def product_structure(*args, **cwargs):
    return Structure(
        product(*(struc.domain for struc in args), **cwargs),
        *starmap(
            lambda *rels: product_relation(*rels, **cwargs),
            transpose(struc.relations for struc in args)))
