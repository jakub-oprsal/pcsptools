from pcsptools import *


# 1-in-3- vs NAE-SAT has a Pixley polymorphism
try:
    solution = next(test_identities(
        onein(3), nae(2), parse_identities("p(xxy) = p(yxx) = p(yxy) = p(yyy)")))
except StopIteration:
    assert(False)

# Equations don't have BW hence they cannot satisfy the Barto-Kozik condition
try:
    solution = next(test_identities(
        affine(2), affine(2),
        parse_identities(
            "u(xxy) = u(xyx) = u(yxx) = d(xy)",
            "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)")))
    assert(False)
except StopIteration:
    pass

# Horn-Sat has a set function which satisfies the identities below.
try:
    solution = next(test_identities(
        hornsat(), hornsat(),
        parse_identities(
            "d(xy) = d(yx) = t(xxy) = t(xyy)",
            "t(xyz) = t(yzx)")))
except StopIteration:
    assert(False)

# I am not aware of any non-trivial condition satisfied in Pol(C_5, K_4).
# The same test is run twice to check that loop_condition produces what we
# expect.
try:
    solution = next(test_identities(
        cycle(5), clique(4), parse_identities("c(xyz) = c(yzx)")))
    assert(False)
except StopIteration:
    pass

try:
    solution = next(test_identities(
        cycle(5), clique(4),
        loop_condition(ocycle(3))
        ))
    assert(False)
except StopIteration:
    pass

# Linear equations mod 2 have a Siggers.
try:
    solution = next(test_identities(
        affine(2), affine(2),
        loop_condition(clique(3))
        ))
except StopIteration:
    assert(False)

# K_3 has 12 binary polymorphisms (6 dictators for each coordinate)
solutions = test_identities(clique(3), clique(3),
        parse_identities("p(x,y) = p(x,y)"))
assert(len(list(solutions)) == 12)
