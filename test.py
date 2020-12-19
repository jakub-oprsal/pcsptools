from pcsptools import *
from math import factorial
import pycosat


solver = csp_solver(pycosat.itersolve)

n = 3
nclique = clique(n)
nclique.check()
assert(not nclique.is_similar(onein(3)))
assert(nclique.is_similar(Structure(range(2), ())))
assert(domain_of(nclique.relations[0]) == set(range(n)))
assert(len(nclique.relations[0]) == n*(n-1))
assert(nclique.type == (2,))

k = 3
powr = nclique.power(k)
assert(set(powr.domain) == set(domain_of(powr.relations[0])))
assert(len(powr.relations[0]) == (n*(n-1))**k)
assert(powr.type == (2,))
assert(powr.is_similar(nclique))

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
    pass

try:
    solution = next(test_identities(
        onein(3), nae(2), parse_identities("p(xxy) = p(yxx) = p(yxy) = p(yyy)"), solver))
except StopIteration:
    assert(False)

rigid_clique = nclique.singleton_expansion()
assert(rigid_clique.type == (2,) + tuple(1 for a in rigid_clique.domain))
solutions = tuple(solver(rigid_clique.power(k), rigid_clique))
assert(len(solutions) == k)

try:
    solution = next(test_identities(
        affine(2), affine(2),
        parse_identities(
            "u(xxy) = u(xyx) = u(yxx) = d(xy)",
            "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)"),
        solver))
    assert(False)
except StopIteration:
    pass

try:
    solution = next(test_identities(
        hornsat(), hornsat(),
        parse_identities(
            "d(xy) = d(yx) = t(xxy) = t(xyy)",
            "t(xyz) = t(yzx)"),
        solver))
except StopIteration:
    assert(False)
