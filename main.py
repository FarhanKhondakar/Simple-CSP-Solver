import copy
from collections import deque

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def ac3(self):
        queue = deque([(x, y) for (x, y) in self.constraints])
        while queue:
            (xi, xj) = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False  # No valid values left
                for xk in self.variables:
                    if xk != xi and (xi, xk) in self.constraints:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi][:]:  # Copy to avoid modifying during iteration
            if not any(self.satisfies(x, y, xi, xj) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def satisfies(self, x, y, xi, xj):
        if (xi, xj) == ('A', 'B'):
            return x < y
        
        if (xi, xj) == ('B', 'C'):
            return x == 2 * y
        
        if (xi, xj) == ('B', 'D'):
            return x <= y
        return True

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
        for (var1, var2) in self.constraints:
            if var1 in assignment and var2 in assignment:
                if not self.satisfies(assignment[var1], assignment[var2], var1, var2):
                    return False
        return True

    def enumerate_pairs(self, var1, var2):
        pairs = []
        for a in self.domains[var1]:
            for b in self.domains[var2]:
                if self.satisfies(a, b, var1, var2):
                    pairs.append((a, b))
        return pairs

def main():
    variables = ['A', 'B', 'C', 'D']
    initial_domains = {
        'A': [1, 2, 3],
        'B': [1, 2, 3],
        'C': [1, 2, 3],
        'D': [3, 4]
    }
    
    # Constraints as pairs (X1, X2)
    constraints1 = [
        ('A', 'B'),  # A < B
    ]
    
    constraints2 = [
        ('B', 'C')
    ]
    
    constraints3 = [
        ('B', 'D')
    ]
    
    # Create CSP instances with separate copies of domains
    csp = CSP(['A', 'B'], copy.deepcopy(initial_domains), constraints1)
    csp2 = CSP(['B', 'C'], copy.deepcopy(initial_domains), constraints2)
    csp3 = CSP(['B', 'D'], copy.deepcopy(initial_domains), constraints3)

    # Check arc consistency and attempt to solve each CSP instance
    for i, csp_instance in enumerate([csp, csp2, csp3], start=1):
        if csp_instance.ac3():
            print(f"AC-3 made the CSP arc consistent for instance {i}.")
            solution = csp_instance.backtrack({})
        else:
            print(f"CSP instance {i} is not arc consistent.")
        
        # Enumerate valid pairs for each constraint
        if i == 1:
            pairs = csp.enumerate_pairs('A', 'B')
            print("Valid pairs for A < B:", pairs)
        elif i == 2:
            pairs = csp2.enumerate_pairs('B', 'C')
            print("Valid pairs for B = 2C:", pairs)
        elif i == 3:
            pairs = csp3.enumerate_pairs('B', 'D')
            print("Valid pairs for B <= D:", pairs)

if __name__ == "__main__":
    main()
