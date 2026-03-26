"""Driver script demonstrating the full query evaluation pipeline.

This script shows how the pieces fit together:
1. Define a conjunctive query.
2. Compute a tree decomposition (student-implemented).
3. Evaluate the tree decomposition (student-implemented).

Run: python evaluate.py
"""

from query import ConjunctiveQuery, Relation
from student import compute_tree_decomposition, evaluate_tree_decomposition


def triangle_query_example():
    """Triangle query on a small graph: Q(x,y,z) :- R(x,y), S(y,z), T(x,z)"""
    print("=" * 60)
    print("Triangle Query Example")
    print("=" * 60)

    # Create a small graph database
    # Graph: 0-1, 0-2, 0-3, 1-2, 1-3, 2-3 (complete graph K4)
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    # Make edges bidirectional
    all_edges = edges + [(b, a) for a, b in edges]
    
    R = Relation("R", ["x", "y"])
    R.add_data([{"x": a, "y": b} for a, b in all_edges])
    S = Relation("S", ["y", "z"])
    S.add_data([{"y": a, "z": b} for a, b in all_edges])
    T = Relation("T", ["x", "z"])
    T.add_data([{"x": a, "z": b} for a, b in all_edges])

    # Define the query
    query = ConjunctiveQuery(["x", "y", "z"], [R, S, T])
    print(f"Query: {query}")

    # Step 1: Compute tree decomposition (student implementation)
    print("\nComputing tree decomposition...")
    td = compute_tree_decomposition(query)
    print(td)

    # Step 2: Evaluate query (student implementation)
    print("\nEvaluating query...")
    result = evaluate_tree_decomposition(query, td)
    print(f"\nResult: {len(result)} tuples")
    for row in sorted(result, key=lambda r: tuple(r[v] for v in query.head)):
        print(f"  {row}")


def path_query_example():
    """Path query: Q(x,z) :- R(x,y), S(y,z)"""
    print("\n" + "=" * 60)
    print("Path Query Example")
    print("=" * 60)

    R = Relation("R", ["x", "y"])
    R.add_data([{"x": 1, "y": 10}, {"x": 2, "y": 10}, {"x": 3, "y": 20}])
    S = Relation("S", ["y", "z"])
    S.add_data([{"y": 10, "z": 100}, {"y": 10, "z": 200}, {"y": 20, "z": 300}])
    query = ConjunctiveQuery(["x", "z"], [R, S])
    print(f"Query: {query}")

    print("\nComputing tree decomposition...")
    td = compute_tree_decomposition(query)
    print(td)

    print("\nEvaluating query...")
    result = evaluate_tree_decomposition(query, td)
    print(f"\nResult: {len(result)} tuples")
    for row in sorted(result, key=lambda r: tuple(r[v] for v in query.head)):
        print(f"  {row}")


def csv_example():
    """Load data from CSV files (if available)."""
    import os

    triangle_dir = os.path.join("data", "triangle")
    if not os.path.exists(triangle_dir):
        print("\n(Skipping CSV example — data/triangle/ not found)")
        return

    print("\n" + "=" * 60)
    print("CSV Triangle Query Example")
    print("=" * 60)

    R = Relation("R", ["x", "y"])
    R.load_csv("data/triangle/R.csv",)
    S = Relation("S", ["y", "z"])
    S.load_csv("data/triangle/S.csv",)
    T = Relation("T", ["x", "z"])
    T.load_csv("data/triangle/T.csv",)
    query = ConjunctiveQuery(["x", "y", "z"], [R, S, T])
    print(f"Query: {query}")

    print("\nComputing tree decomposition...")
    td = compute_tree_decomposition(query)
    print(td)

    print("\nEvaluating query...")
    result = evaluate_tree_decomposition(query, td)
    print(f"\nResult: {len(result)} tuples")


if __name__ == "__main__":
    try:
        triangle_query_example()
    except NotImplementedError as e:
        print(f"\n  >> {e}")
        print("  >> Implement the functions in student.py to see results!\n")

    try:
        path_query_example()
    except NotImplementedError as e:
        print(f"\n  >> {e}")

    try:
        csv_example()
    except NotImplementedError as e:
        print(f"\n  >> {e}")
