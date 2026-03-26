"""Trie data structure for indexing relations in a worst-case optimal join.

A Trie indexes a set of tuples according to a given variable ordering.
At each level of the trie, you can efficiently retrieve the set of values
that extend a given prefix.

Example usage:
    relation = Relation("R", ["x", "y"])
    relation.add_data([{"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 2, "y": 3}])
    t = Trie(relation, ["x", "y"])

    # Get all values of x
    t.lookup([])          # returns {1, 2}

    # Get all values of y where x=1
    t.lookup([1])         # returns {2, 3}

    # Check if (x=2, y=3) exists
    t.lookup([2, 3])      # returns set() (leaf) or confirms existence
    t.contains([2, 3])    # returns True
"""


class TrieNode:
    """A single node in the trie."""

    def __init__(self):
        self.children = {}  # value -> TrieNode

    def child_values(self):
        """Return the set of values (keys) at this node."""
        return set(self.children.keys())


class Trie:
    """A trie that indexes rows (list-of-dicts) on a given variable ordering.

    Attributes:
        variable_order: The list of variables defining the trie levels.
        root: The root TrieNode.
    """

    def __init__(self, relation, variable_order):
        """Build a trie from rows according to the given variable ordering.

        Args:
            relation: A Relation object with data
            variable_order: List of variable names defining the trie depth order,
                e.g. ["x", "y"]. The first variable is at the root level.
        """
        self.variable_order = list(variable_order)
        self.root = TrieNode()
        for row in relation.data:
            self._insert(row)

    def _insert(self, row):
        """Insert a single row into the trie."""
        node = self.root
        for var in self.variable_order:
            val = row[var]
            if val not in node.children:
                node.children[val] = TrieNode()
            node = node.children[val]

    def lookup(self, prefix):
        """Return the set of values at the next level given a prefix.

        Args:
            prefix: A list of values corresponding to the first len(prefix)
                variables in variable_order. For example, if variable_order
                is ["x", "y", "z"] and prefix is [1, 2], this returns all
                values of z where x=1 and y=2.

        Returns:
            A set of values at the next trie level, or an empty set if
            the prefix reaches the bottom of the trie or doesn't exist.
        """
        node = self._traverse(prefix)
        if node is None:
            return set()
        return node.child_values()

    def contains(self, values):
        """Check if a full tuple exists in the trie.

        Args:
            values: A list of values corresponding to all variables in
                variable_order.

        Returns:
            True if the tuple exists in the trie.
        """
        node = self._traverse(values)
        return node is not None

    def _traverse(self, values):
        """Traverse the trie following the given values.

        Args:
            values: List of values for the first len(values) variables.

        Returns:
            The TrieNode reached, or None if the path doesn't exist.
        """
        node = self.root
        for val in values:
            if val not in node.children:
                return None
            node = node.children[val]
        return node
