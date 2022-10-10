import pytest
from pcsptools import *
from pcsptools.solver import pyco_solver as solver
from pcsptools.structure import domain_of, product_structure
from math import factorial


def test_structuretypes():
    n = 4
    nclique = clique(n)
    assert nclique.check()
    assert not nclique.is_similar(onein(3))
    assert nclique.is_similar(Structure(range(2), ()))
    assert domain_of(nclique.relations[0]) == set(range(n))
    assert len(nclique.relations[0]) == n*(n-1)
    assert nclique.type == (2,)

def test_power():
    powr = clique(3).power(3)
    assert set(powr.domain) == set(domain_of(powr.relations[0]))
    assert len(powr.relations[0]) == 6**3
    assert powr.type == (2,)
    assert powr.is_similar(clique(3))

def test_product():
    prod = product_structure(clique(3), clique(4))
    assert set(prod.domain) == set(domain_of(prod.relations[0]))
    assert len(prod.relations[0]) == 6*12
    assert prod.type == (2,)

def test_solver_false():
    with pytest.raises(StopIteration):
        _ = next(solver(clique(5), clique(4)))

def test_solver_true():
    n, k = 4, 3
    solutions = tuple(solver(clique(n).power(k), clique(n)))
    assert len(solutions) == k*factorial(n)

def test_singleton_expansion():
    rigid_clique = clique(3).singleton_expansion()
    assert rigid_clique.type == (2,) + tuple(1 for a in rigid_clique.domain)
    solutions = tuple(solver(rigid_clique.power(3), rigid_clique))
    assert len(solutions) == 3
