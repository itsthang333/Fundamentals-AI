from itertools import combinations

"""Represents a logical literal."""
class Literal:
    def __init__(self, symbol ="", negation=False):
        """
        Initialize a literal with a symbol and negation state.
        Args:
            symbol (str): The symbol of the literal.
            negation (bool): The negation state of the literal.
        """
        self.symbol = symbol
        self.negation = negation

    def __repr__(self):
        """Return the string representation of the literal."""
        return '-{}'.format(self.symbol) if self.negation else self.symbol
    
    def __eq__(self, literal):
        """Check if two literals are equal."""
        return self.symbol == literal.symbol and self.negation == literal.negation
    
    def __hash__(self):
        """Return the hash value of the literal."""
        return hash('-'+self.symbol if self.negation else self.symbol)
    
    def __lt__(self, literal):
        """Compare two literals."""
        if self.symbol != literal.symbol:
            return self.symbol < literal.symbol
        return self.negation < literal.negation
    
    def negate(self):
        self.negation = not self.negation
    
    def is_opposite(self, literal):
        """Check if two literals are opposite."""
        return self.negation != literal.negation and self.symbol == literal.symbol
    
    def parse_literal(string_literal):
        """
        Parse a string representation of a literal.
        Args:
            string_literal (str): The string representation of the literal.
        Returns:
            Literal: The parsed literal object.
        """
        string_literal = string_literal.strip()
        if string_literal[0] == '-':
            return Literal(symbol=string_literal[1], negation=True)
        else:
            return Literal(symbol=string_literal[0], negation=False)
   
"""Represents a logical clause."""
class Clause:
    def __init__(self):
        """Initialize an empty clause."""
        self.literals = []

    def __repr__(self):
        """Return the string representation of the clause."""
        return ' OR '.join(str(literal) for literal in self.literals) if self.literals else '{}'
    
    def __eq__(self, clause):
        return set(self.literals) == set(clause.literals)
    
    def __hash__(self):
        return hash(tuple(self.literals))
    
    def __lt__(self, clause):
        """Compare two clauses."""
        if len(self.literals) != len(clause.literals):
            return len(self.literals) < len(clause.literals)
        for index in range(len(self.literals)):
            if self.literals[index] != clause.literals[index]:
                return self.literals[index] < clause.literals[index]
        return False
    
    def is_empty(self):
        return len(self.literals) == 0
    
    def is_meaningless(self):
        """Check if the clause is meaningless."""
        for index in range(len(self.literals) - 1):   
            if self.literals[index].is_opposite(self.literals[index + 1]):
                return True
        return False

    def add_literal(self, literal):
        self.literals.append(literal)
    
    def clean(self):
        """Remove duplicate literals and sort the literals."""
        self.literals = sorted(set(self.literals))

    def negate_literals(self):
        """Negate all literals in the clause."""
        for literal in self.literals:
            literal.negate()

    def parse_clause(string_clause):
        """
        Parse a string representation of a clause.
        Args:
            string_clause (str): The string representation of the clause.
        Returns:
            Clause: The parsed clause object.
        """
        new_clause = Clause()
        string_clause = string_clause.strip()
        string_literals = string_clause.split('OR')
        for string_literal in string_literals:
            literal = Literal.parse_literal(string_literal)
            new_clause.add_literal(literal)
        new_clause.clean()
        return new_clause

    def clone_without_literal(self, literal=None):
        """
        Create a clone of a clause without a specific literal.
        Args:
            clause (Clause): The original clause.
            literal (Literal): The literal to be excluded.
        Returns:
            Clause: The cloned clause without the specified literal.
        """
        new_clause = Clause()
        for lit in self.literals:
            if lit != literal:
                new_clause.add_literal(lit)
        return new_clause
    
    def merge(clause1, clause2):
        new_clause = Clause()
        new_clause.literals = clause1.literals + clause2.literals
        new_clause.clean()
        return new_clause
    
    def resolve(clause1, clause2):
        """
        Resolve two clauses and generate resolvents.
        Args:
            clause1 (Clause): The first clause.
            clause2 (Clause): The second clause.
        Returns:
            set: A set of resolvents.
            bool: True if an empty clause is generated, otherwise False.
        """
        is_empty = False
        resolvents = set()

        for literal1 in clause1.literals:
            for literal2 in clause2.literals:
                if literal1.is_opposite(literal2):
                    new_clause = Clause.merge(clause1.clone_without_literal(literal1), 
                                              clause2.clone_without_literal(literal2))
                    if new_clause.is_meaningless():
                        continue
                    if new_clause.is_empty():
                        is_empty = True
                    resolvents.add(new_clause)

        return resolvents, is_empty
    

class KnowledgeBase:
    """Represents a knowledge base of logical clauses."""
    def __init__(self):
        """Initialize an empty knowledge base."""
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def build_knowledge_base(self, alpha_string, clause_strings):
        """
        Build the knowledge base from alpha and clause strings.
        Args:
            alpha_string (str): The string representation of alpha clause.
            clause_strings (list): A list of string representations of clauses.
        """
        alpha_string = alpha_string.strip()
        alpha_literals = alpha_string.split('OR')
        for alpha_literal in alpha_literals:
            clause = Clause.parse_clause(alpha_literal)
            clause.negate_literals()
            self.add_clause(clause)
        for clause_str in clause_strings:
            clause = Clause.parse_clause(clause_str)
            clause.clean()
            self.add_clause(clause)
    
    def pl_resolution(self):
        input_clauses = set(self.clauses)
        output_clauses = []
        is_unsatisfiable = False
        
        while True:
            new = set()
            for (clause1, clause2) in combinations(input_clauses, 2):
                resolvents, is_empty = Clause.resolve(clause1, clause2)
                new.update(resolvents)
                is_unsatisfiable |= is_empty

            diff_clauses = new.difference(input_clauses)
            output_clauses.append(diff_clauses)
            input_clauses.update(new)
            
            if is_unsatisfiable:
                return True, output_clauses
            if not diff_clauses:
                return False, output_clauses 

def read_input(input_file):
    with open(input_file, 'r') as file:
        alpha = file.readline().strip()
        num_clauses = int(file.readline().strip())
        clauses = [file.readline().strip() for _ in range(num_clauses)]
    return alpha, clauses

def write_output(output_file, output_clauses, is_entailed):
    with open(output_file, 'w') as file:
        for clauses in output_clauses:
            file.write('{}\n'.format(len(clauses)))
            for clause in clauses:
                file.write('{}\n'.format(clause))
        if is_entailed:
            file.write("YES\n")  
        else:
            file.write("NO\n")  

def main(input_file, output_file):
    alpha, clauses = read_input(input_file)
    kb = KnowledgeBase()
    kb.build_knowledge_base(alpha, clauses)
    is_entailed, output_clauses = kb.pl_resolution()
    write_output(output_file, output_clauses, is_entailed)

main("input1.txt", "output1.txt")
main("input2.txt", "output2.txt")
main("input3.txt", "output3.txt")
main("input4.txt", "output4.txt")
main("input5.txt", "output5.txt")
