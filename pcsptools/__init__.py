'''
PCSPTOOLS

Module for quick computations for CSPs and PCSPs, and tools for producing a
CSP solver from a SAT solver.
'''
from .structure import *
from .polymorphisms import (
        polymorphisms,
        test_identities,
        parse_identities,
        loop_condition,
        )
