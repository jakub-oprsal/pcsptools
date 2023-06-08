"""
CSP SOLVER

This module provides a CSP solver. Currently, the only available solver is a
hook for pycosat using a reduction to SAT through label cover.
"""
import pycosat
from .reductions import csp_to_lc, lc_to_sat


def csp_solver(sat_solver):
    def solver(*csp_instance):
        yield from csp_to_lc(csp_instance).bind(lc_to_sat).solve(sat_solver)

    return solver


pyco_solver = csp_solver(pycosat.itersolve)
