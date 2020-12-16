from structure import *
from reductions import *
from identities import *
from math import factorial
import pycosat


solver = csp_solver(pycosat.itersolve)

n = 3
nclique = clique(n)
assert(domain_of(nclique.relations[0]) == set(range(n)))
assert(len(nclique.relations[0]) == n*(n-1))
assert(nclique.type == (2,))

k = 3
powr = nclique.power(k)
assert(set(powr.domain) == set(domain_of(powr.relations[0])))
assert(len(powr.relations[0]) == (n*(n-1))**k)
assert(powr.type == (2,))

prod = product_structure(clique(3), clique(4))
assert(set(prod.domain) == set(domain_of(prod.relations[0])))
assert(len(prod.relations[0]) == 6*12)
assert(prod.type == (2,))

solutions = tuple(solver(clique(n+1), nclique))
assert(len(solutions) == 0)

solutions = tuple(solver(powr, nclique))
assert(len(solutions) == k*factorial(n))

try:
    solution = next(test_identities(
        cycle(5), clique(4), parse_identities("c(xyz) = c(yzx)"), solver))
    assert(False)
except StopIteration:
    assert(True)

solver = csp_solver(pycosat.itersolve)
try:
    solution = next(test_identities(
        cycle(9), clique(3), parse_identities("c(xyz) = c(yzx)"), solver))
    assert(True)
except StopIteration:
    assert(False)
