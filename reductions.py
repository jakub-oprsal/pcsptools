##
# REDUCTIONS
#
# Tools to provide reductions between CSP, label cover, and SAT. The goal is to
# allow encoding of a CSP instance into a SAT instance, so that we can use
# external SAT-solvers to solve CSP instances.
#
# A reduction is a function that:
# - inputs (in_instance)
# - returns (out_instance, out_decode)
#
# where `decode` a function that decodes a solution to `out_instance` to a
# solution of `in_instance` (this gives that the reduction is sound), and of
# course, if `out_instance` is not solvable, then `in_instance` is not solvable
# either (the reduction is complete).
#
# We also provide a helper function `csp_solver(sat_solver)` which produces a
# csp_solver from a sat_solver.
#
from itertools import combinations
from structure import transpose


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
        (c, size)
        for rel, size in zip(Input.relations, rel_sizes)
        for c in rel)
    variables = csp_variables + csp_constraints

    def projections(relation):
        return transpose(
            tuple((i, inverse[a]) for a in edge)
            for i, edge in enumerate(relation))

    def constraints():
        for in_rel, rel in zip(Input.relations, Template.relations):
            projs = projections(rel)
            for vs in in_rel:
                for v, pi in zip(vs, projs):
                    yield ((vs, v), pi)

    def decode(solution):
        return {v: Template.domain[solution[v]] for v, dom in csp_variables}

    return (variables, constraints()), decode


def lc_to_sat(in_instance):
    """ converts a LC instance to a list of SAT clauses
        returns an iterator over clauses and a decode function """
    lc_vars, lc_constraints = in_instance

    variables = (-1,) + tuple((v, a) for v, d in lc_vars for a in range(d))
    table = {va: i for i, va in enumerate(variables) if i > 0}

    def exactly_one(pairs):
        scope = tuple(table[va] for va in pairs)
        yield scope
        for a, b in combinations(scope, 2):
            yield (-a, -b)

    def dnfs():
        for v, d in lc_vars:
            yield from exactly_one((v, a) for a in range(d))
        for pair, pi in lc_constraints:
            vs, v = pair
            for x, pix in pi:
                yield (-table[(vs, x)], table[(v, pix)])

    def decode(solution):
        return dict(variables[x] for x in solution if x > 0)

    return dnfs(), decode


def compose(reduction1, reduction2):
    def composed_reduction(instance):
        instance1, decode1 = reduction1(instance)
        instance2, decode2 = reduction2(instance1)
        return (instance2, lambda solution2: decode1(decode2(solution2)))

    return composed_reduction


def csp_solver(sat_solver):
    def solver(*csp_instance):
        lc_instance, decode_lc = csp_to_lc(csp_instance)
        sat_instance, decode_sat = lc_to_sat(lc_instance)
        yield from map(
            lambda solution: decode_lc(decode_sat(solution)),
            sat_solver(sat_instance))
    return solver
