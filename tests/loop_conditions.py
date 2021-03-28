from pcsptools import *

try:
    solution = next(test_identities(
        cycle(5), clique(4),
        loop_condition(ocycle(3))
        ))
    assert(False)
except StopIteration:
    pass

try:
    solution = next(test_identities(
        affine(2), affine(2),
        loop_condition(clique(3))
        ))
except StopIteration:
    assert(False)
