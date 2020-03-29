#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import ne
from collections import deque
import functools
from copy import deepcopy
import numpy as np


#Definimos la clase de Restricción
class Restriccion:
    def __init__(self, scope, predicado):
        self.scope = scope
        self.predicado = predicado

    def __call__(self, assigment):
        """ assigment es un diccionario de variable: valor """
        return self.predicado(*tuple(assigment[v] for v in self.scope))

#Definimos la clase CSP (Constrain Satisfying problem)
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

#Funciones auxiliares
def dict_union(d1, d2):
    """ Simplifica la unión de dos diccionarios """
    d = dict(d1)
    d.update(d2)
    return d

def generar_vecinos(csp, nodo):
    """ nodo es un un diccionario variable: valor """
    variable = list(csp.variables)[len(nodo)]
    vecinos = []
    for value in csp.dominios[variable]:
        assigment = dict_union(nodo, {variable:value})
        if csp.consistente(assigment):
            vecinos.append(assigment)
    return vecinos


def backtracking(csp):
    def goal(csp, nodo):
        return len(nodo) == len(csp.variables)

    mejor_path = []

    start = {}

    frontera = deque()  # En BFS la frontera es una pila

    # Agrego por a derecha, ya que es una cola
    frontera.append((start, [start])) # nodo y path

    while frontera:
        nodo, path = frontera.popleft() # Extraigo por la izquierda
        print(nodo)
        if goal(csp, nodo):
            mejor_path = path
            mejor_solucion = nodo
            yield mejor_solucion, mejor_path
        else:
            vecinos = reversed(generar_vecinos(csp, nodo))
            for vecino in vecinos:
                frontera.appendleft((vecino, path+[vecino]))


def trivial_coloring(node_count, edge_count, edges):
    """ every node has its own color """
    colores = range(0, node_count)

    # Convertimos la solución en el formato esperado
    output_data = str(node_count) + '\n'
    output_data += ' '.join(map(str, colores))

    return output_data

def gac(node_count, edge_count, edges):
    # inicializa el número de colores en el dominio de la variable
    num_colors = 2
    # crea diccionario con las variables y sus respectivos dominios iniciales
    variables = {i:{i for i in range(num_colors)} for i in range(node_count)}
    # crea conjunto de aristas por checar
    aux = {(tup[1],tup[0]) for tup in edges}
    aristas = aux.union(set(edges))

    return gac2(variables, aristas, aristas_checadas)

def gac2(variables, aristas, to_do):
    
    # loop sigue mientras haya aristas por checar
    while bool(to_do):
        #print("------------------- NUEVA ITERACIÓN-----------------------\n\n")
        #print(variables)
        #print("------------------- ARISTAS POR CHECAR----------------")
        #print(to_do)
        #print("----------------------------------------------------------")
        # obtiene una arista para checar
        #print("------------------- ARISTA A REVISAR ---------------------")
        checa = to_do.pop()
        #print(checa)
        #print("----------------------------------------------------------")
        # indica los nodos que corresponden a la arista
        #print("------------------- VARIABLES X Y EN ARISTA---------------")
        nodo_a = checa[0]
        nodo_b = checa[1]
        #print(nodo_a)
        #print(nodo_b)
        #print("----------------------------------------------------------")
        # se crea el nuevo dominio de nodo_a
        #print("--------------- DOM X y DOM de Y------------------")
        nd = variables[nodo_a].copy()
        dom_b = variables[nodo_b]
        #print(nd)
        #print(dom_b)
        #print("-----------------------------------------------------------")
        # para cada elemento del dominio del nodo_a revisamos que haya una asignación posible para el nodo_b
        for x in variables[nodo_a]:
            # si el dominio del nodo_b sin x es vacío, entonces no hay asignación posible y x se elimina del nuevo dominio de nodo_a
            #print("------------------- ELEMENTO DEL DOMINIO DE X POR CHECAR -------")
            #print(x)
            if(not bool(dom_b.difference({x}))):
                nd.remove(x)
            
        # Si se eliminaron elementos del dominio del nodo_a, todas las aristas checadas que conciernen a nodo_a deben ser agregadas a aristas nuevamente
        if not bool(nd):
            variables[nodo_a] = nd
            break
        if nd != variables[nodo_a]:
            #print("------------------------ NUEVO DOMINIO ES DIFERENTE AL VIEJO-----------")
            #print(nd)
            # Volvemos a agregar las aristas que pueden no ser consistentes a to_do
            new_constr = set()
            for ar in aristas:
                if ar[1] == nodo_a:
                    new_constr.add(ar)
            to_do = to_do.union(new_constr)
            variables[nodo_a] = nd
    

    return variables

def CSP_Solver(node_count, edge_count, edges):
    num_colors = 2
    # crea diccionario con las variables y sus respectivos dominios iniciales
    variables = {i:{i for i in range(num_colors)} for i in range(node_count)}
    # crea conjunto de aristas por checar
    aux = {(tup[1],tup[0]) for tup in edges}
    aristas = aux.union(set(edges))

    sol = Solve2({i:{i for i in range(num_colors)} for i in range(node_count)}, aux.union(set(edges)), aux.union(set(edges)))

    while sol == False:
        num_colors = num_colors +1
        sol = Solve2({i:{i for i in range(num_colors)} for i in range(node_count)}, aristas, aristas.copy())
    return (num_colors,sol)

def Solve2(variables, aristas, to_do):
    #print("--------- ENTRADAs SOL2------------------------")
    #print(variables)
    #print(aristas)
    #print(to_do)
    copia_var = deepcopy(variables)
    copia_to_do = to_do.copy()
    dom0 = gac2(copia_var, aristas, copia_to_do)

    # Checamos si hay alguna variable con dominio vacío
    if not functools.reduce(lambda x,y: x and y,list(map(lambda x: bool(x), dom0.values()))):
        return False
    # Checamos si es una asignación completa
    elif functools.reduce(lambda x,y: x+y, list(map(lambda x: len(x), dom0.values()))) == len(variables):
        return dom0
    else:
        # Seleccionamos una variable para asignar (en este caso la que tenga la mayor cantidad de colores disponibles)
        #print("----------------------- NO SE HA RESUELTO EL PROBLEMA -------------------")
        cols_disp = list(map(lambda x: len(x), dom0.values()))
        selected_var = cols_disp.index(next(x for x in cols_disp if x >1))

        # Reintroducimos las aristas que será necesario volver a revisar
        new_constr = set()
        for ar in aristas:
            if ar[1] == selected_var:
                new_constr.add(ar)
        aux = {(tup[1],tup[0]) for tup in new_constr}
        new_constr = aux.union(new_constr)
        
        #print("------------- LAS NUEVAS RESTRICCIONES A CONSIDERAR-------------------")
        #print(new_constr)


        valores = variables[selected_var]

        while(bool(valores)):
            #print("-------------- INTENTO CON ASIGNACIÓN ------------------")
            dom0[selected_var]= {valores.pop()}
            #print("variable: " + str(selected_var) + ", con asignación: " + str(dom0[selected_var]))
            dominio = deepcopy(dom0)
            res = Solve2(dominio, aristas, new_constr)
            #print("------------- RESULTADO DE INTENTO ---------------------")
            #print(res)

            if res != False:
                break
    return res
    
def incremental(node_count, edge_count, edges):

    asig = {i:1 for i in range(node_count)}
    color = 2
    deficit = 3 * edge_count
    #print("------------- ESTADOS INCICIALES--------------")
    matriz = np.zeros((node_count,node_count), dtype=int)
    for ar in edges:
        matriz[ar[0]][ar[1]] = 1
        matriz[ar[1]][ar[0]] = 1
    for i in range(node_count):
        matriz[i][i] = 1
    #print(asig)
    #print(color)
    #print(deficit)
    #print(matriz)

    def pinta(var, nuevo_col):
        for i in range(node_count):
            if matriz[i][var] > 0:
                matriz[i][var] = nuevo_col

    def calc_def():
        lista = [0]*node_count
        for i in range(node_count):
            color = matriz[i][i]
            cont = 0
            for j in range(node_count):
                if matriz[i][j] > 0 and matriz[i][j] == color:
                    cont = cont + 1
            lista[i] = cont -1
        return functools.reduce(lambda x,y: x+y, lista)

    # Calcula el número de restricciones violadas si la variable var se pintara de nuevo color
    def calc_def2(nuevo_color, var):
        copia_color = matriz[var][var]

        pinta(var, nuevo_color)
        #print("--------------- MATRIZ PINTADA DE COLOR NUEVO-------------")
        #print(matriz)
        
        nuevo_def = [0]*node_count

        for i in range(node_count):
            color = matriz[i][i]
            cont = 0
            for j in range(node_count):
                if matriz[i][j] > 0 and matriz[i][j] == color:
                    cont = cont + 1
            nuevo_def[i] = cont -1
        
        pinta(var, copia_color)

        return functools.reduce(lambda x,y: x+y, nuevo_def)

    def checa_color(defi, col):
        minimum = 1.1*defi
        min_var = -1
        for var in range(node_count):
            #print("--------------- VARIABLE Y NUEVO DEFICIT-----------------")
            n_def = calc_def2(col, var)
            #print(var)
            #print(n_def)
            if( n_def < minimum ):
                minimum = n_def
                min_var = var
        return min_var, minimum


    def sig_paso(defi, col):
        var, minimum = checa_color(defi, col)
        #print("------------------- VALORES VAR Y MINIMUM DEF----------")
        #print(var)
        #print(minimum)
        if(var != -1):        
            pinta(var, color)
            defi = minimum
            asig[var] = color
        return defi
        
    
    while(deficit != 0):
        #print("------------------- DEFICIT DE ENTRADA------------------------")
        #print(deficit)
        deficit = sig_paso(deficit, color)
        color = color +1
        print(deficit)

    print(color-1)
    return asig
    
    

## TODO: Modifica este diccionario
algorithms = {
    'trivial_coloring': trivial_coloring,
    'gac':gac,
    'd_split': CSP_Solver,
    'inc':incremental
}

def solve_it(input_data, algorithm=trivial_coloring):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    node_count = int(firstLine[0])
    edge_count = int(firstLine[1])

    edges = []

    for i in range(1, edge_count+1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    output_data = algorithm(node_count, edge_count, edges)

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        file_location = sys.argv[1].strip()
        algorithm = algorithms[sys.argv[2].strip()]

        print(f"Ejecutando el algoritmo {algorithm} en {file_location}")
        
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data, algorithm))
    else:
        print("""Este script requiere dos argumentos: \n"""
              """El archivo con los datos del problema y el nombre del algoritmo que diseñaste.\n"""
              """i.e. python solver.py ./data/gc_4_1 trivial_coloring""")
