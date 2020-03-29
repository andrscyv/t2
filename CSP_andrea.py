class Constraint:
    def __init__(self, scope, predicate):
        self.scope = scope
        self.predicate = predicate

    def __call__(self, assigment):
        """ assigment es un diccionario de variable: valor """
        return self.predicate(*tuple(assigment[v] for v in self.scope))

    def __str__(self):
        return f'SCOPE: {self.scope}, PREDICATE: {self.predicate}'

class CSP:
    def __init__(self, domain, constraints, variables = None):
        self.variables = variables
        self.domain = domain
        self.constraints = constraints


        # Diccionario inverso
        self.variable_constraints = {variable:set() for variable in self.variables}
        for constraint in self.constraints:
            for variable in constraint.scope:
                self.variable_constraints[variable].add(constraint)

    def consistent(self, assigment):
        """assigment es un diccionario de variable: valor """
        return all(c(assigment)
                   for c in self.constraints
                   if all(variable in assigment for variable  in c.scope))
    
    def consistent_var(self, assignment, var):
        """ assigment es un diccionario de variable:valor
            solo se revisa las restricciones que incluyen a var"""

        return all(c(assignment)
                    for c in self.constraints
                    if (var in c.scope and all(variable in assignment for variable in c.scope)) )

    def update_domain(self, domain):
        self.domain = domain

    def __str__(self):
        return str('Colors:', self.domain)

    def __repr__(self):
        return f"CSP({self.domain}, {str([str(c) for c in self.constraints])})"
