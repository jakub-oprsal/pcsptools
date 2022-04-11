'''
REDUCTIONS

Tools to provide reductions between CSP, label cover, and SAT.  One of the
goals is to allow encoding of a CSP instance into a SAT instance, so that we
can use external SAT-solvers to solve CSP instances. But these reducitons can
be used for things like: checking whether a minor condition is satisfied by
polymorphisms, whether it is trivial, constructing reductions between CSPs,
etc.

For us a reduction is a function that inputs an instance of one problem, and
ouputs an instance of another problem and a way to decode a solution to the
second instance into a solution of the first instance. The output is encoded
in a monad which is an abstraction that will allow us easily compose
reductions by using `bind`.

We also provide a helper function `csp_solver(sat_solver)` which produces a
csp_solver from a sat_solver.
'''
from itertools import combinations, count
from .structure import transpose


class DelayDecode():
    """ A monad for delayed computation. We use it to delay decoding a solution
        after reducing to another problem. """

    def __init__(self, instance, decode=lambda x: x):
        """ pure or identity, depending on arguments """
        self.instance = instance
        self.decode = decode

    def bind(self, reduction):
        out = reduction(self.instance)
        return DelayDecode(
            out.instance,
            lambda x: self.decode(out.decode(x)))

    def solve(self, solver):
        yield from map(self.decode, solver(self.instance))


def csp_to_lc(in_instance):
    """ converts a CSP instance fiven as (Input, Template) to an LC instance
        returns: LC instance (variables, constraints), and a decode function.
        Note that constraints are given as iterator. """
    Input, Template = in_instance

    inverse = {a: i for i, a in enumerate(Template.domain)}
    dom_size = len(Template.domain)
    rel_sizes = tuple(len(rel) for rel in Template.relations)

    csp_variables = tuple((v, dom_size) for v in Input.domain)
    csp_constraints = tuple(
        ((c, symb), size)
        for symb, rel, size in zip(count(), Input.relations, rel_sizes)
        for c in rel)
    variables = csp_variables + csp_constraints

    def projections(relation):
        return transpose(
            tuple((i, inverse[a]) for a in edge)
            for i, edge in enumerate(relation))

    def constraints():
        for symb, in_rel, rel in zip(
                count(), Input.relations, Template.relations):
            projs = projections(rel)
            for vs in in_rel:
                for v, pi in zip(vs, projs):
                    yield (((vs, symb), v), pi)

    def decode(solution):
        return {v: Template.domain[solution[v]] for v, dom in csp_variables}

    return DelayDecode((variables, constraints()), decode)


def lc_to_sat(in_instance):
    """ converts a LC instance to a list of SAT clauses
        returns an iterator over clauses and a decode function """
    lc_vars, lc_constraints = in_instance

    variables = (False,) + tuple((v, a) for v, d in lc_vars for a in range(d))
    table = {va: i for i, va in enumerate(variables) if i > 0}

    def exactly_one(pairs):
        scope = tuple(table[va] for va in pairs)
        yield scope
        for a, b in combinations(scope, 2):
            yield (-a, -b)

    def cnfs():
        for v, d in lc_vars:
            yield from exactly_one((v, a) for a in range(d))
        for pair, pi in lc_constraints:
            vs, v = pair
            for x, pix in pi:
                yield (-table[(vs, x)], table[(v, pix)])

    def decode(solution):
        return dict(variables[x] for x in solution if x > 0)

    return DelayDecode(cnfs(), decode)


def csp_solver(sat_solver):
    def solver(*csp_instance):
        yield from csp_to_lc(csp_instance).bind(lc_to_sat).solve(sat_solver)
    return solver
