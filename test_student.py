"""Tests for student implementations.

Run with: python -m pytest test_student.py -v

Tests are organized by function:
- test_tree_decomposition_* : Tests for compute_tree_decomposition
- test_wcoj_*               : Tests for worst_case_optimal_join
- test_evaluate_*           : Tests for evaluate_tree_decomposition (end-to-end)
"""

import os
import pytest

from query import ConjunctiveQuery, Relation
from trie import Trie
from utils import fractional_edge_cover_value
from student import compute_tree_decomposition, evaluate_tree_decomposition


# ---------------------------------------------------------------------------
# Helper: brute-force join for verification
# ---------------------------------------------------------------------------

def brute_force_join(query):
    """Compute the query result by nested-loop join (for testing only)."""
    # Start with the first relation
    result = query.relations[0].data

    for rel in query.relations[1:]:
        shared_vars = set(result[0].keys()) & set(rel.variables) if result else set()
        new_result = []
        for r1 in result:
            for r2 in rel.data:
                if all(r1[v] == r2[v] for v in shared_vars):
                    merged = {**r1, **r2}
                    new_result.append(merged)
        result = new_result

    # Project to head variables
    projected = [{v: row[v] for v in query.head} for row in result]
    # Deduplicate
    seen = set()
    deduped = []
    for row in projected:
        key = tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    return deduped


def rows_to_set(rows):
    """Convert list of row dicts to a set of frozensets for comparison."""
    return {frozenset(row.items()) for row in rows}


# ---------------------------------------------------------------------------
# Test: Provided utilities (sanity checks — these should always pass)
# ---------------------------------------------------------------------------

class TestProvidedUtilities:
    """Verify that the provided utilities work correctly."""

    def test_trie_basic(self):
        relation = Relation("R", ["x", "y"])
        relation.add_data([{"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 2, "y": 3}])
        t = Trie(relation, ["x", "y"])
        assert t.lookup([]) == {1, 2}
        assert t.lookup([1]) == {2, 3}
        assert t.lookup([2]) == {3}
        assert t.contains([1, 2])
        assert t.contains([2, 3])
        assert not t.contains([2, 2])

    def test_trie_single_variable(self):
        relation = Relation("R", ["x"])
        relation.add_data([{"x": 1}, {"x": 2}, {"x": 3}])
        t = Trie(relation, ["x"])
        assert t.lookup([]) == {1, 2, 3}

    def test_fractional_edge_cover_triangle(self):
        R = Relation("R", ["x", "y"])
        S = Relation("S", ["y", "z"])
        T = Relation("T", ["x", "z"])
        value = fractional_edge_cover_value({"x", "y", "z"}, ConjunctiveQuery(["x", "y", "z"], [R, S, T]))
        assert abs(value - 1.5) < 1e-6, f"Triangle fec should be 1.5, got {value}"

    def test_fractional_edge_cover_path(self):
        R = Relation("R", ["x", "y"])
        S = Relation("S", ["y", "z"])
        value = fractional_edge_cover_value({"x", "y", "z"}, ConjunctiveQuery(["x", "y", "z"], [R, S]))
        assert abs(value - 2.0) < 1e-6, f"Path fec should be 2.0, got {value}"


# ---------------------------------------------------------------------------
# Test: validate_tree_decomposition
# ---------------------------------------------------------------------------

class TestValidateTreeDecomposition:
    """Tests for the student's validate_tree_decomposition function."""
    # TODO: YOU SHOULD INSERT TESTS HERE!
    pass

# ---------------------------------------------------------------------------
# Test: compute_tree_decomposition
# ---------------------------------------------------------------------------

class TestTreeDecomposition:
    """Tests for the student's compute_tree_decomposition function."""
    # TODO: YOU SHOULD INSERT TESTS HERE!
    pass


# ---------------------------------------------------------------------------
# Test: worst_case_optimal_join
# ---------------------------------------------------------------------------

class TestWCOJ:
    """Tests for the student's worst_case_optimal_join function."""\
    
    # TODO: YOU SHOULD INSERT TESTS HERE!
    pass



# ---------------------------------------------------------------------------
# Test: evaluate_tree_decomposition (end-to-end)
# ---------------------------------------------------------------------------

class TestEvaluateQuery:
    """End-to-end tests using all three student functions together."""
    # TODO: YOU SHOULD INSERT TESTS HERE!
    pass


# ---------------------------------------------------------------------------
# Test: CSV-based larger examples
# ---------------------------------------------------------------------------

class TestCSVExamples:
    """Larger tests using CSV data files."""

    @pytest.mark.skipif(
        not os.path.exists("data/triangle/R.csv"),
        reason="CSV test data not found"
    )
    def test_triangle_csv(self):
        """Triangle query on CSV graph data."""
        R = Relation("R", ["x", "y"])
        R.load_csv("data/triangle/R.csv")
        S = Relation("S", ["y", "z"])
        S.load_csv("data/triangle/S.csv",)
        T = Relation("T", ["x", "z"])
        T.load_csv("data/triangle/T.csv")
        query = ConjunctiveQuery(["x", "y", "z"], [R, S, T])

        td = compute_tree_decomposition(query)
        result = evaluate_tree_decomposition(query, td)

        expected = brute_force_join(query)
        assert rows_to_set(result) == rows_to_set(expected)

    @pytest.mark.skipif(
        not os.path.exists("data/triangle/R.csv"),
        reason="CSV test data not found"
    )
    def test_boolean_triangle_csv(self):
        """Triangle query on CSV graph data."""
        R = Relation("R", ["x", "y"])
        R.load_csv("data/triangle/R.csv")
        S = Relation("S", ["y", "z"])
        S.load_csv("data/triangle/S.csv",)
        T = Relation("T", ["x", "z"])
        T.load_csv("data/triangle/T.csv")
        query = ConjunctiveQuery([], [R, S, T])
        td = compute_tree_decomposition(query)
        result = evaluate_tree_decomposition(query, td)

        expected = brute_force_join(query)
        assert rows_to_set(result) == rows_to_set(expected)

    @pytest.mark.skipif(
        not os.path.exists("data/four_cycle/R.csv"),
        reason="CSV test data not found"
    )
    def test_four_cycle_csv(self):
        """Q(w,x,y,z) :- R(w,x), S(x,y), T(y,z), U(w,z) on CSV data."""
        R = Relation("R", ["w", "x"])
        R.load_csv("data/four_cycle/R.csv")
        S = Relation("S", ["x", "y"])
        S.load_csv("data/four_cycle/S.csv")
        T = Relation("T", ["y", "z"])
        T.load_csv("data/four_cycle/T.csv")
        U = Relation("U", ["w", "z"])
        U.load_csv("data/four_cycle/U.csv")
        query = ConjunctiveQuery(["w", "x", "y", "z"], [R, S, T, U])

        td = compute_tree_decomposition(query)
        result = evaluate_tree_decomposition(query,td)

        expected = brute_force_join(query)
        assert rows_to_set(result) == rows_to_set(expected)
