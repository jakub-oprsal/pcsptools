from pcsptools import *


try:
    solution = next(test_identities(
        cycle(5), clique(4), parse_identities("c(xyz) = c(yzx)")))
    assert(False)
except StopIteration:
    pass

try:
    solution = next(test_identities(
        onein(3), nae(2), parse_identities("p(xxy) = p(yxx) = p(yxy) = p(yyy)")))
except StopIteration:
    assert(False)

try:
    solution = next(test_identities(
        affine(2), affine(2),
        parse_identities(
            "u(xxy) = u(xyx) = u(yxx) = d(xy)",
            "v(xxxy) = v(xxyx) = v(xyxx) = v(yxxx) = d(xy)")))
    assert(False)
except StopIteration:
    pass

try:
    solution = next(test_identities(
        hornsat(), hornsat(),
        parse_identities(
            "d(xy) = d(yx) = t(xxy) = t(xyy)",
            "t(xyz) = t(yzx)")))
except StopIteration:
    assert(False)
