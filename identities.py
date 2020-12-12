from itertools import product
from structure import *

class Components:
    """ a data structure holding connected components of a graph """

    def __init__(self, domain):
        self.tree = {a: a for a in domain}

    def __call__(self, a, same_as=None):
        """ returns the current representative from the same class as `a`
            same_as is used for bookeeping """
        if same_as is None:
            same_as = []
        if self.tree[a] == a:
            for e in same_as:
                self.tree[e] = a
            return a
        same_as.append(a)
        return self(self.tree[a], same_as)

    def add(self, a, b):
        """ add an edge to the graph possibly collapsing two components"""
        self.tree[self(a)] = self(b)

    def __iter__(self):
        """ iterates through representatives of the classes """
        for a in self.tree:
            if self.tree[a] == a:
                yield a


def indicator_structure(Template, LC_instance):
    """ given a Template A and a LC instance Sigma
        builds the indicator structure of Sigma over A
        and passes the identification object """
    in_vars, in_cons = LC_instance

    arities = dict(in_vars)
    domain = set()
    for f, arity in arities.items():
        for x in product(Template.domain, repeat=arity):
            domain.add((f, x))

    identify = Components(domain)
    for scope, relation in in_cons:
        f, g = scope
        pi = {x: y for x, y in relation}
        for x in product(Template.domain, repeat=arities[g]):
            x_pi = tuple(x[pi[i]] for i in range(arities[f]))
            identify.add((f, x_pi), (g, x))

    def constraint_from_rel(relation):
        for f in arities:
            for xs in product_relation(relation, repeat=arities[f]):
                yield tuple(identify((f, x)) for x in xs)

    constraints = (
        constraint_from_rel(relation) for relation in Template.relations)
    variables = iter(identify)

    def decode(homomorphism):
        polymorphisms = dict()
        for f, arity in arities.items():
            polymorphisms[f] = {
                x: homomorphism[identify((f, x))]
                for x in product(Template.domain, repeat=arity)}
        return polymorphisms

    return (Structure(variables, constraints), decode)
