import csv

class Relation:
    """A relation in a conjunctive query.

    Attributes:
        name: The relation name (e.g., "R", "Edge").
        variables: List of variable names (e.g., ["x", "y"]).
        data: List of row dicts, where each dict maps variable name -> value.
    """

    def __init__(self, name, variables):
        self.name = name
        self.variables = list(variables)
        self.data = []

    def __str__(self):
        return f"{self.name}({', '.join(self.variables)})"

    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        """Allow iteration over the relation's data rows."""
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)

    def add_data(self, rows):
        """Add data rows to the relation.

        Args:
            rows: A list of dicts mapping variable name -> value, e.g.
                [{"x": 1, "y": 2}, {"x": 1, "y": 3}]
        """
        self.data.extend(rows)

    def load_csv(self, filepath, value_type=int):
        """Load a CSV file into a table.

        Args:
            filepath: Path to the CSV file.
            value_type: Type to cast values to (default: int).
        """
        rows = []
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append({col: value_type(val) for col, val in zip(self.variables, row)})
        self.data = rows


class ConjunctiveQuery:
    """A conjunctive query of the form: head :- body.

    Example: Q(x, z) :- R(x, y), S(y, z)

    Attributes:
        head: List of variables in the query head (output variables).
        relations: List of Relation objects forming the query body.
    """

    def __init__(self, head, relations):
        self.head = list(head)
        self.relations = list(relations)

    def get_variables(self):
        """Return the set of all variables appearing in the query body."""
        variables = set()
        for rel in self.relations:
            variables.update(rel.variables)
        return variables

    def get_relations_for_variable(self, variable):
        """Return list of Relations that contain the given variable."""
        return [rel for rel in self.relations if variable in rel.variables]

    def __str__(self):
        head_str = f"Q({', '.join(self.head)})"
        relations_str = ', '.join(str(rel) for rel in self.relations)
        return f"{head_str} :- {relations_str}"

    def __repr__(self):
        return self.__str__()
