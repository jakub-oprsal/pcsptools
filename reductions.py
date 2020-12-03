from itertools import *
import structure

# A REDUCTION
#
# inputs (in_instance)
# returns (out_instance, out_decode)
#
# where *out_instance* is a P2 instance, and *decode* a function that decodes
# *out_solution* to *in_solution*
#

def csp_to_lc(in_instance):
    Input, Template = in_instance

    csp_variables = tuple( (v, Template.domain) for v in Input.domain )
    csp_constraints = tuple( (c, rel_T)
        for rel_I, rel_T in zip(Input.relations, Template.relations) for c in rel_I )
    variables = csp_variables + csp_constraints

    def constraints():
        for vs, relation in csp_constraints:
            for i in range(len(vs)):
                yield ((vs, vs[i]),
                    tuple(map(lambda edge: (edge, edge[i]), relation)))

    def decode(solution):
        return { v: solution[v] for v, dom in csp_variables }

    return ((variables, constraints()), decode)


def lc_to_sat(in_instance):
    lc_vars, lc_constraints = in_instance 

    variables = (-1,) + tuple((v, a) for v, domain in lc_vars for a in domain) 
    table = { va: i for i, va in enumerate(variables) if i>0 }

    def exactly_one(pairs):
        scope = tuple( table[va] for va in pairs )
        yield scope
        for a, b in combinations(scope, 2):
            yield (-a, -b)

    def dnfs():
        for v, domain in lc_vars:
            yield from exactly_one( (v, a) for a in domain )
        for pair, pi in lc_constraints:
            vs, v = pair
            for x, pix in pi:
                yield (-table[(vs, x)], table[(v, pix)])

    def decode(solution):
        lc_solution = dict()
        for x in solution:
            if x > 0:
                v, value = variables[x]
                lc_solution[v] = value
        return lc_solution

    return (dnfs(), decode)


def compose(reduction1, reduction2):
    def composed_reduction(instance):
        in_after1, decode1 = reduction1(instance)
        in_after2, decode2 = reduction2(in_after1)
        decode = lambda x: decode1(decode2(x))
        return (in_after2, decode)

    return composed_reduction

csp_to_sat = compose(csp_to_lc, lc_to_sat)
