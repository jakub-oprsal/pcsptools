'''
PCSPTOOLS

Module for quick computations for CSPs and PCSPs, and tools for producing a
CSP solver from a SAT solver.
'''
from .structure import *
from .reductions import (
        csp_to_lc,
        lc_to_sat,
        csp_solver,
        )
from .identities import (
        indicator_structure,
        test_identities,
        parse_identities,
        loop_condition,
        )
