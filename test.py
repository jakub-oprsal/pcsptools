from structure import *
from reductions import *
from functools import cache
import pycosat


@cache
def fac(n):
    return 1 if n <= 0 else fac(n-1)*n


def neq(n):
    return ((i, j) for i in range(n) for j in range(n) if i != j)


n = 3
clique = Structure(range(n), (neq(n),))
assert(domain_of(neq(n)) == set(range(n)))
assert(len(clique.relations[0]) == n*(n-1))
assert(clique.type == (2,))

k = 3
powr = power_structure(clique, k)
assert(set(powr.domain) == set(domain_of(powr.relations[0])))
assert(len(powr.relations[0]) == (n*(n-1))**k)
assert(powr.type == (2,))

bigger_clique = Structure(range(n+1), (neq(n+1),))
sat_instance, decode = csp_to_sat((bigger_clique, clique))
solution = pycosat.solve(sat_instance)
assert(solution == "UNSAT")

sat_instance, decode = csp_to_sat((powr, clique))
solutions = tuple(map(decode, pycosat.itersolve(sat_instance)))
assert(len(solutions) == k*fac(n))
