# CS599 Final Project: Hypertree Decompositions for Conjunctive Query Evaluation

In this project you will implement three core algorithms that together form an efficient pipeline for evaluating conjunctive queries:

1. **`compute_tree_decomposition`** — find an optimal fractional hypertree decomposition of a query using variable elimination.
2. **`worst_case_optimal_join`** — evaluate a set of relations using the Generic Join algorithm.
3. **`evaluate_tree_decomposition`** — evaluate a full conjunctive query via Yannakakis' algorithm on a tree decomposition.

All of your work goes in **`student.py`**. Tests go in **`test_student.py`**.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Repository Structure

```
.
├── student.py            # YOUR CODE GOES HERE
├── test_student.py       # YOUR TESTS GO HERE
│
├── query.py              # Relation and ConjunctiveQuery classes (provided)
├── tree_decomposition.py # TreeDecomposition class (provided)
├── trie.py               # Trie data structure (provided)
├── utils.py              # Fractional edge cover LP solver (provided)
│
├── evaluate.py           # Example driver script
├── data/                 # CSV graph data for testing
│   ├── triangle/         # R.csv, S.csv, T.csv
│   └── four_cycle/       # R.csv, S.csv, T.csv, U.csv
└── requirements.txt
```

---

## Provided Code

### `query.py`

**`Relation(name, variables)`** — represents a database relation.
- `rel.variables` — list of variable names, e.g. `["x", "y"]`
- `rel.data` — list of row dicts, e.g. `[{"x": 1, "y": 2}, ...]`
- `rel.add_data(rows)` — append rows
- `rel.load_csv(filepath)` — load data from a CSV file

**`ConjunctiveQuery(head, relations)`** — represents a query `Q(head) :- R1(...), R2(...), ...`
- `query.head` — list of output variable names
- `query.relations` — list of `Relation` objects
- `query.get_variables()` — returns the set of all variables in the query body

### `tree_decomposition.py`

**`TreeDecomposition(tree_edges, bag_to_variables, bag_to_relations)`**
- `tree_edges` — list of `(bag_id, bag_id)` tuples
- `bag_to_variables` — dict mapping `bag_id -> set of variables`
- `bag_to_relations` — dict mapping `bag_id -> list of relation names`
- `td.bags` — set of all bag IDs
- `td.rooted_order(root=None)` — returns `(order, parent)`: a BFS traversal order and a dict mapping each bag to its parent (`None` for the root)
- `td.get_neighbors(bag)` — returns the set of adjacent bags
- `td.variables_to_bags` — dict mapping `variable -> set of bag_ids` containing it

### `trie.py`

**`Trie(relation, variable_order)`** — builds a trie index over the rows of a `Relation`.
- `trie.lookup(prefix)` — returns the set of values at the next level given a list of prefix values
- `trie.contains(values)` — returns `True` if the full tuple exists

### `utils.py`

**`fractional_edge_cover_value(variables, query)`** — returns the cover number ρ* (minimum total weight).

---

## Your Tasks

### 1. `student.py` — Implement three functions

Search for `raise NotImplementedError` to find each stub.

#### `validate_tree_decomposition(query, tree_decomposition) -> bool`

Test whether `tree_decomposition` satisfies the necessary properties of a TD.

#### `compute_tree_decomposition(query) -> TreeDecomposition`

Compute an **optimal hypertree decomposition** (i.e. a TD with optimal fractional hypertree width).

#### `worst_case_optimal_join(relations) -> list[dict]`

Implement the **Generic Join** algorithm.

#### `evaluate_tree_decomposition(query, tree_decomposition) -> list[dict]`

Evaluate the tree decomposition by materializing the bags then running Yannakakis' algorithm.

### 2. `test_student.py` — Write tests

The test file contains three empty test classes with `TODO` comments:

- **`TestValidateTreeDecomposition`** - test `validate_tree_decomposition` with few examples of valid and invalid TDs.
- **`TestTreeDecomposition`** — test `compute_tree_decomposition`. Use `validate_tree_decomposition` to check structural correctness. Consider also checking that the fractional hypertree width is optimal for known queries.
- **`TestWCOJ`** — test `worst_case_optimal_join` directly with small hand-crafted examples.
- **`TestEvaluateQuery`** — end-to-end tests. The helper `brute_force_join(query)` is provided as a correctness oracle.

Run your tests with:

```bash
python -m pytest test_student.py -v
```

---

## Example

```bash
python evaluate.py
```

This runs two example queries (triangle and path) end-to-end and prints the results.

## Useful References

For the core tree decomposition optimizer, there are a few approaches to take:
1. Variable Elimination (also known as Bucket Elimination): In this approach, we choose an order on the variables in our query that don't appear in the head. In order, we try to project them out one-at-a-time, and this corresponds to a TD where each bag projects away one variable. The tricky part is identifying which relations correspond to which bag and how to arrange the bags into a tree. Section 3.1 of [this paper](https://www.vldb.org/pvldb/vol17/p4655-he.pdf) provides a good description as does Section 2 of [this paper](https://d1wqtxts1xzle7.cloudfront.net/51134088/Heuristic_Methods_for_Hypertree_Decompos20161231-6639-1i3s7zc-libre.pdf?1483214495=&response-content-disposition=inline%3B+filename%3DHeuristic_Methods_for_Hypertree_Decompos.pdf&Expires=1774554232&Signature=NP-9yXEmRY12SrXlucmjhHYel8VHz7QT8svpMRObnXTqYG5HnDdDfHNLb33vJY9XAyn1XbphyFDRM3o2~tCPSOeVnlZ~QmhyO58x5DbVpDpFLEHs9KQ9KJJ5VxhARFdXadWoKtrdHntsnI1i0RxstNzBtZOENT6lnItu6EdIved2wxFET1nly2fZIIFxq2qOnKsj1AhIqZ0V1SpInJ8z4lqII9H-aMNJ6kpd1xSvAHsj9Iq9b9su6XDnxNASWs~-1Pnz~F-TUemYmoYSJ~LMpFXjqMP0mPPcwzXh-YHYqMfK2UF5FYPcNbSGYrxpylbI07riqx2QLJzYzq-Askx9Ew__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA).

2. Candidate Bag -> Candidate Tree Decomposition: In this approach, we start by selecting a set of candidate bags (e.g. bags which have an AGM bound of <c), then we try to construct a TD from that set of bags. If no TD can be constructed, we create a larger candidate set and try again. Here, the algorithm has two phases 1) the candidate set generation and 2) the tree construction algorithm. This paper takes that approach and describes it in Section 3 of [this paper](https://dl.acm.org/doi/pdf/10.1145/3725251).

3. Hypergraph Separators: In this approach, we start by identifying all "balanced separators" of the hypergraph. These are variable sets that split the query into roughly equal sized pieces. We treat each balanced separator as the root node of a TD, then we recurse on the now disconnected sub-queries. Their balanced separators connected as child bags of the first one, and so on. This is described in [this paper](https://dl.acm.org/doi/pdf/10.1145/3638758).

I would recommend variable elimination as a starting place, but all of these algorithms are cool!

For Generic Join, the following resources are available:
1. The lecture slides from our join algorithms lecture
2. These two blog posts ([1](https://remy.wang/blog/wcoj.html), [2](https://finnvolkel.com/wcoj-generic-join))
3. [The original paper ](https://dl.acm.org/doi/pdf/10.1145/2590989.2590991)

## Grading

I will run an additional test suite to grade your implementation's correctness & optimality. 50% of 
the grade will be based on this check. In addition, we will schedule short in-person code reviews
to discuss your implementation and the design decisions. 50% of your grade will be based on the 
code reviews. 

Further, extensions to this work that go significantly beyond the required implementation will be
eligible for up to 25% extra credit! These extensions could:
1. Apply the technique to another problem (e.g. optimizing linear algebra/tensor algebra).
2. Significantly improve the scalability of the optimizer.
3. Significantly improve the runtime of the execution layer (e.g. the WCOJ and Yannakakis' Algorithm).
4. Use an improved cost function to guide the selection of the tree decomposition. For example,
this could leverage better statistics about the input relations like degree constraints.
5. Provide detailed benchmarks for the runtime of the optimization and evaluation on different
queries and datasets.
6. Whatever else you can think of! 
