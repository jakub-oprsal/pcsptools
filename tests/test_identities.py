import pytest
from pcsptools import *


def test_pixley():
    # 1-in-3- vs NAE-SAT has a Pixley polymorphism
    solution = next(check_identities(
        onein(3), nae(2),
        parse_identities("p(xxy) = p(yxx) = p(yxy) = p(yyy)")))
    assert solution

def test_bw():
    # Equations don't have BW hence they cannot satisfy the Barto-Kozik
    # condition
    with pytest.raises(StopIteration):
        solution = next(check_identities(
            affine(2), affine(2),
            parse_identities(
                "u(xxy) = u(xyx) = u(yxx) = d(xy)",
                "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)")))

def test_horn():
    # Horn-Sat has a set function which satisfies the identities below.
    assert next(check_identities(
        hornsat(), hornsat(),
        parse_identities(
            "d(xy) = d(yx) = t(xxy) = t(xyy)",
            "t(xyz) = t(yzx)")))

def test_cycle_colouring():
    # I am not aware of any non-trivial condition satisfied in Pol(C_5, K_4).
    # The same test is run twice to check that loop_condition produces what we
    # expect.
    with pytest.raises(StopIteration):
        _ = next(check_identities(
            cycle(5), clique(4), parse_identities("c(xyz) = c(yzx)")))

def test_loop_condition_false():
    with pytest.raises(StopIteration):
        _ = next(check_identities(
            cycle(5), clique(4),
            loop_condition(ocycle(3))))

def test_loop_condition_true():
    assert next(check_identities(
        affine(2), affine(2),
        loop_condition(clique(3))))

def test_count():
    # K_3 has 12 binary polymorphisms (6 dictators for each coordinate)
    solutions = check_identities(clique(3), clique(3),
            parse_identities("p(x,y) = p(x,y)"))
    assert len(list(solutions)) == 12
