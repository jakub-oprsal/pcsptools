'''
STRUCTURE

The `Structure` class and severel predefined structures.
'''
from itertools import product, starmap, chain
from functools import cached_property


def transpose(matrix):
    return tuple(zip(*matrix))


def arity_of(relation):
    rel = iter(relation)
    try:
        arity = len(next(rel))
    except StopIteration:
        return None #Empty Relation

    if not all(arity == len(edge) for edge in rel):
        raise ValueError('Ambiguous arity!')
    return arity


def domain_of(relation):
    return set().union(*relation)


class Structure:
    def __init__(self, domain, *relations):
        self.domain = tuple(domain)
        self.relations = tuple(tuple(relation) for relation in relations)

    @cached_property
    def type(self):
        return tuple(map(arity_of, self.relations))

    def check(self):
        type_ = type(self)  # Checks that arities are well-defined
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

    def singleton_expansion(self):
        """ Adds singletons so that the resulting structure has a single
            automorphism. """
        return Structure(
            self.domain,
            *self.relations, *(((a,),) for a in self.domain))


def product_relation(*args, **cwargs):
    yield from map(transpose, product(*args, **cwargs))


def product_structure(*args, **cwargs):
    return Structure(
        product(*(struc.domain for struc in args), **cwargs),
        *starmap(
            lambda *rels: product_relation(*rels, **cwargs),
            transpose(struc.relations for struc in args)))


##
# Pre-defined structures
#
def clique(k):
    """ The k-clique graph. """
    return Structure(
        range(k),
        ((i, j) for i in range(k) for j in range(k) if i != j))


def cycle(n):
    """ The unoriented n-cycle graph. """
    if n==1:
        return loop(2)
    if n==2:
        return clique(2)
    def edges():
        for a in chain(range(0, n, 2), range(1, n, 2)):
            yield (a, (a-1) % n)
            yield (a, (a+1) % n)
    return Structure(range(n), edges())


def ocycle(n):
    """ The oriented n-cycle graph. """
    if n==1:
        return loop(2)
    return Structure(
            range(n),
            ((i, (i+1) % n) for i in range(n)))


def nae(n, arity=3):
    """ NAE on an `n`-element set,
        optinally the arity of the relation is given. """
    return Structure(
        range(n),
        (x for x in product(range(n), repeat=arity) if len(set(x)) > 1))


def onein(n):
    """ The generalisation of 1in3-SAT to `n`-ary relations.
        The domain is Boolean anyway. """
    return Structure(
        (0, 1),
        (tuple((1 if i == k else 0) for i in range(n)) for k in range(n)))


def tinn(t,n):
    """ The generalisation of t-in-n-SAT. """
    return Structure(
        (0, 1),
        (tuple((1 if i in xs else 0)
            for i in range(n)) for xs in combinations(range(n), t)))


def loop(*reltype, name=0):
    """ The one-element loop structure with the given type
        (all relations are non-empty). Type has to be fully defined. """
    return Structure(
        (name,),
        *((tuple(name for i in range(arity)),) for arity in reltype))


def affine(p, arity=3):
    """ Affine equations over Z_p. """
    relations = tuple([] for i in range(p))
    for xs in product(range(p), repeat=arity):
        relations[sum(xs) % p].append(xs)
    return Structure(range(p), *relations)


def hornsat():
    relations = (
        (xs for xs in product((0, 1), repeat = 3) if xs != (0, 0, 1)),
        (xs for xs in product((0, 1), repeat = 3) if xs != (0, 0, 0)),
        ((0,),), ((1,),))
    return Structure((0, 1), *relations)
