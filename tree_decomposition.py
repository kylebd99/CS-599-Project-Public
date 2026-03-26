from collections import defaultdict


class TreeDecomposition:
    """A tree decomposition of a hypergraph/query.

    Attributes:
        tree_edges: List of (bag_id, bag_id) tuples forming the tree structure.
        bag_to_variables: Dict mapping bag_id -> set of variables in that bag.
        bag_to_relations: Dict mapping bag_id -> list of relation names covered by that bag.
        variables_to_bags: Dict mapping variable -> set of bag_ids containing it.
        adjacency: Dict mapping bag_id -> set of neighboring bag_ids.
    """

    def __init__(self, tree_edges, bag_to_variables, bag_to_relations=None):
        """
        Args:
            tree_edges: List of (bag_id, bag_id) tuples. For a single-bag
                decomposition, pass an empty list.
            bag_to_variables: Dict mapping bag_id -> set/list of variables.
            bag_to_relations: Dict mapping bag_id -> list of relation names
                that are covered by this bag. If None, defaults to empty lists.
        """
        self.tree_edges = tree_edges
        self.bag_to_variables = {b: set(vs) for b, vs in bag_to_variables.items()}
        self.bag_to_relations = bag_to_relations or {b: [] for b in bag_to_variables}
        self.variables_to_bags = self._invert_bag_to_variables()
        self.adjacency = self._build_adjacency()

    def _invert_bag_to_variables(self):
        variables_to_bags = defaultdict(set)
        for bag, variables in self.bag_to_variables.items():
            for variable in variables:
                variables_to_bags[variable].add(bag)
        return dict(variables_to_bags)

    def _build_adjacency(self):
        adj = defaultdict(set)
        for u, v in self.tree_edges:
            adj[u].add(v)
            adj[v].add(u)
        # Ensure all bags appear even if they have no edges (single-bag TD)
        for bag in self.bag_to_variables:
            if bag not in adj:
                adj[bag] = set()
        return dict(adj)

    @property
    def bags(self):
        """Return the set of all bag IDs."""
        return set(self.bag_to_variables.keys())

    def get_neighbors(self, bag):
        """Return the set of bags adjacent to the given bag."""
        return self.adjacency.get(bag, set())

    def get_leaves(self):
        """Return the set of leaf bags (degree <= 1)."""
        return {b for b in self.bags if len(self.adjacency.get(b, set())) <= 1}

    def get_root(self, preferred=None):
        """Return a root bag. Uses preferred if given, otherwise picks an arbitrary bag."""
        if preferred is not None and preferred in self.bags:
            return preferred
        return next(iter(self.bags))

    def rooted_order(self, root=None):
        """Return bags in BFS order from root, along with parent mapping.

        Returns:
            (order, parent): order is a list of bag_ids in BFS order,
                parent is a dict mapping bag_id -> parent_bag_id (root maps to None).
        """
        if root is None:
            root = self.get_root()
        visited = {root}
        queue = [root]
        order = [root]
        parent = {root: None}
        while queue:
            current = queue.pop(0)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    order.append(neighbor)
                    parent[neighbor] = current
        return order, parent

    def __str__(self):
        lines = ["TreeDecomposition:"]
        for bag in sorted(self.bag_to_variables.keys()):
            vars_str = ", ".join(sorted(self.bag_to_variables[bag]))
            rels_str = ", ".join(self.bag_to_relations.get(bag, []))
            lines.append(f"  Bag {bag}: vars={{{vars_str}}}, rels=[{rels_str}]")
        if self.tree_edges:
            lines.append("  Edges: " + ", ".join(f"({u},{v})" for u, v in self.tree_edges))
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()
