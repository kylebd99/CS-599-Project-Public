"""Utility functions for the tree decomposition assignment.

Provides:
- Fractional edge cover computation via linear programming.
- Fractional hypertree width computation.
"""

import numpy as np
from scipy.optimize import linprog

from query import ConjunctiveQuery, Relation


def fractional_edge_cover(variables, query):
    """Compute the optimal fractional edge cover for a set of variables. 

    A fractional edge cover assigns a non-negative weight to each relation
    such that every variable is covered (the sum of weights of relations
    containing that variable is >= 1), and the total weight is minimized.

    Args:
        variables: A set/list of variables to cover.
        query: A ConjunctiveQuery object.

    Returns:
        A dict mapping relation name -> optimal weight (float).
        Only relations with non-zero weight are included.

    Example:
        >>> R = Relation("R", ["x", "y"])
        >>> S = Relation("S", ["y", "z"])
        >>> T = Relation("T", ["x", "z"])
        >>> cover = fractional_edge_cover({"x", "y", "z"}, query=ConjunctiveQuery([], [R, S, T]))
        >>> # For the triangle, optimal cover assigns 0.5 to each relation
    """
    variables = list(variables)
    n_vars = len(variables)
    n_rels = len(query.relations)

    if n_vars == 0:
        return {}

    # Objective: minimize sum of weights
    c = np.ones(n_rels)

    # Constraints: for each variable, sum of weights of relations containing it >= 1
    # linprog uses A_ub @ x <= b_ub, so we negate for >= constraints
    A_ub = np.zeros((n_vars, n_rels))
    for i, var in enumerate(variables):
        for j, rel in enumerate(query.relations):
            if var in rel.variables:
                A_ub[i, j] = -1.0
    b_ub = -np.ones(n_vars)

    # Bounds: weights >= 0
    bounds = [(0, None) for _ in range(n_rels)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if not result.success:
        raise ValueError(f"LP solver failed: {result.message}")

    # Build result dict (only include relations with non-negligible weight)
    cover = {}
    for j, rel in enumerate(query.relations):
        if result.x[j] > 1e-9:
            cover[rel.name] = float(result.x[j])
    return cover


def fractional_edge_cover_value(variables, query):
    """Compute the optimal fractional edge cover number (rho*).

    This is the minimum total weight of a fractional edge cover.
    Equivalently, this is the maximum weight of a fractional vertex
    packing.

    Args:
        variables: A set/list of variables to cover.
        query: A ConjunctiveQuery object.

    Returns:
        The fractional edge cover number (float).
    """
    cover = fractional_edge_cover(variables, query)
    return sum(cover.values())
