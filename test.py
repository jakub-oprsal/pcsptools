from structure import *
from reductions import *
import pycosat

def neq(n):
    yield from ( (i,j) for i in range(n) for j in range(n) if i != j )

def fac(n):
    if n <= 0:
        return 1
    else:
        return fac(n-1)*n

assert(domain_of(neq(4)) == frozenset({0,1,2,3}))

n = 4
clique = Structure(range(n),(neq(n),))
assert(len(clique.relations[0]) == n*(n-1))

k = 3
powr = power_structure(clique,k)
assert(len(powr.relations[0]) == (n*(n-1))**k)

assert(powr.domain == domain_of(powr.relations[0]))
assert(powr.type == (2,))

bigger_clique = Structure(range(n+1),(neq(n+1),))

sat_instance, decode = csp_to_sat((bigger_clique, clique))
solution = pycosat.solve(sat_instance)
assert(solution == "UNSAT")

sat_instance, decode = csp_to_sat((powr, clique))
solutions = tuple(map(decode,pycosat.itersolve(sat_instance)))

assert(len(solutions) == k*fac(n))
