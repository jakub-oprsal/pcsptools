"""
PCSPTOOLS

Module for quick computations for CSPs and PCSPs, and tools for producing a
CSP solver from a SAT solver.
"""
from .structure import Structure
from .structures import *
from .minor_conditions import *
from .polymorphisms import (
    polymorphisms,
    check_minor_condition,
    solve_minor_condition,
    parse_identities,
    loop_condition,
    sigma,
)
