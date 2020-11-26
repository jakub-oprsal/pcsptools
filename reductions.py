from itertools import *
import structure

# A REDUCTION
#
# inputs (in_instance, in_decode=lambda x: x)
# returns (out_instance, out_decode)
#
# where *out_instance* is a P2 instance, and *decode* a function that decodes
# *out_solution* to in_decode(*in_solution*)
#
# note. we keep the argument for decoding so that these can be easily composed,
# e.g.,
# comp_reduction = lambda x : reduction1(reduction2(x))
#

def csp_to_lc(in_instance):
    Input, Template = in_instance

    csp_variables = tuple( (v,Template.domain) for v in Input.domain )
    csp_constraints = tuple( (c,rel_T)
        for rel_I,rel_T in zip(Input.relations,Template.relations) for c in rel_I )


    variables = csp_variables + csp_constraints
    def constraints()
        for vs,relation in csp_constraints:
            for i in len(vs):
                yield ((vs,vs[i]), map(lambda edge: (edge,edge[i]), relation))

    def decode(solution):
        return { v: solution[v] for v,dom in csp_variables }

    return ((variables, constraints()), decode)


def lc_to_sat(in_instance):
    lc_vars, lc_constraints = in_instance 

    variables = (-1,) + tuple((v,a) for v,domain in in_variables for a in domain) 
    table = { va: i for i, va in enumerate(variables) if i>0 }

    def exactly_one( *pairs )
        scope = tuple( table[va] for va in pairs )
        yield scope
        for a,b in combinations(scope,2):
            yield (-a,-b)

    def dnfs():
        for v, domain in lc_vars:
            yield from exactly_one( (v,a) for a in domain )
        for pair,pi in lc_constraints:
            vs, v = pair
            for x, pix in pi:
                yield (-table[(vs, x)], table[(v, pix)])

    def decode(solution):
        lc_solution = dict()
        for x in solution:
            if x > 0:
                v, value = variables[x]
                lc_solution[v] = value

    return (dnfs(), decode)


def csp_to_sat(csp_instance):
    lc_instance, decode_lc = csp_to_lc(csp_instance)
    sat_instance, decode_sat = lc_to_sat(lc_instance)
    decode = lambda x: decode_lc(decode_sat(x))

    return (sat_instance, decode)
