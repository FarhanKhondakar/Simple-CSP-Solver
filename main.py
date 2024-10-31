import copy
from collections import deque

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints  # constraints are now expected to be a list of lambdas

    def ac3(self):
        # Extract variable pairs from constraints
        queue = deque([(var1, var2) for (var1, var2, _) in self.constraints])
        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False  # No valid values left
                for (var1, var2, _) in self.constraints:
                    if var1 == xi and var2 != xj:
                        queue.append((var2, xi))
                    elif var2 == xi and var1 != xj:
                        queue.append((var1, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi][:]:  # Copy to avoid modifying during iteration
            if not any(self.satisfies(x, y, xi, xj) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def satisfies(self, x, y, xi, xj):
        for (var1, var2, constraint) in self.constraints:
            if (xi == var1 and xj == var2) or (xi == var2 and xj == var1):
                return constraint(x, y)
        return True  # Default case if no specific constraint is found

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment  # All variables are assigned

        unassigned = [v for v in self.variables if v not in assignment]
        var = unassigned[0]

        for value in self.domains[var]:
            # Temporarily assign the value to the variable
            assignment[var] = value
            # Check if the assignment is consistent
            if self.is_consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            # Remove the variable from assignment
            del assignment[var]

        return None  # No valid assignment found

    def is_consistent(self, assignment):
        for (var1, var2, constraint) in self.constraints:
            if var1 in assignment and var2 in assignment:
                if not constraint(assignment[var1], assignment[var2]):
                    return False
        return True

    def enumerate_pairs(self, var1, var2):
        pairs = []
        for a in self.domains[var1]:
            for b in self.domains[var2]:
                if self.satisfies(a, b, var1, var2):
                    pairs.append((a, b))
        return pairs

def create_csp_instance(variables, initial_domains, constraints):
    return CSP(variables, copy.deepcopy(initial_domains), constraints)

def print_pairs(csp_instance, i):
    print("-" * 30)  # Removed the extra newline for closer formatting
    if i == 1:
        pairs = csp_instance.enumerate_pairs('A', 'B')
        print("Valid pairs for A < B:", pairs)
    elif i == 2:
        pairs = csp_instance.enumerate_pairs('B', 'C')
        print("Valid pairs for B = 2C:", pairs)
    elif i == 3:
        pairs = csp_instance.enumerate_pairs('B', 'D')
        print("Valid pairs for B <= D:", pairs)
    print("-" * 30)  # Divider after pairs output

def main():
    variables = ['A', 'B', 'C', 'D']
    initial_domains = {
        'A': [1, 2, 3],
        'B': [1, 2, 3],
        'C': [1, 2, 3],
        'D': [3, 4]
    }
    
    # Define constraints as lambdas
    constraints = [
        ('A', 'B', lambda x, y: x < y),          # A < B
        ('B', 'C', lambda x, y: x == 2 * y),     # B = 2C
        ('B', 'D', lambda x, y: x <= y)           # B <= D
    ]
    
    # Create CSP instances
    csp_instances = [
        create_csp_instance(['A', 'B'], initial_domains, [constraints[0]]),
        create_csp_instance(['B', 'C'], initial_domains, [constraints[1]]),
        create_csp_instance(['B', 'D'], initial_domains, [constraints[2]])
    ]

    # Check arc consistency and attempt to solve each CSP instance
    for i, csp_instance in enumerate(csp_instances, start=1):
        print("\n" + "=" * 30)  # Section divider for each instance
        if csp_instance.ac3():
            print(f"AC-3 made the CSP arc consistent for instance {i}.")
            solution = csp_instance.backtrack({})
            print(f"Solution for instance {i}: {solution}")
        else:
            print(f"CSP instance {i} is not arc consistent.")
        
        print_pairs(csp_instance, i)

if __name__ == "__main__":
    main()
