class CSP:
    def __init__(self, dominios, restricciones):
        self.variables = set(dominios) # quizá sea más eficiente que dominios.keys()
        self.dominios = dominios
        self.restricciones = restricciones
        # Diccionario inverso
        self.variables_restricciones = {variable:set() for variable in self.variables}
        for restriccion in self.restricciones:
            for variable in restriccion.scope:
                self.variables_restricciones[variable].add(restriccion)

    def consistente(self, assigment):
        """assigment es un diccionario de variable: valor """
        return all(c(assigment)
                   for c in self.restricciones
                   if all(variable in assigment for variable  in c.scope))
    
    def __str__(self):
        return str(self.dominios)

    def __repr__(self):
        return f"CSP({self.dominios}, {str([str(c) for c in self.restricciones])})"

class Restriccion:
    def __init__(self, scope, predicado):
        self.scope = scope
        self.predicado = predicado

    def __call__(self, assigment):
        """ assigment es un diccionario de variable: valor """
        return self.predicado(*tuple(assigment[v] for v in self.scope))