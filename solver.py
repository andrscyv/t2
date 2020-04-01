#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import deque
from Csp import Restriccion, CSP
from Util import *
import sys
from functools import partial

def generalSearch(goal, expande):
    mejor_path = []

    start = {}

    frontera = deque()  # En BFS la frontera es una pila

    # Agrego por a derecha, ya que es una cola
    frontera.append((start, [start])) # nodo y path

    while frontera:
        # print('Tamaño de la frontera ', len(frontera))
        nodo, path = frontera.popleft() # Extraigo por la izquierda
        if goal(nodo):
            mejor_path = path
            mejor_solucion = nodo
            return mejor_solucion, mejor_path
        else:
            vecinos = expande(nodo)
            for vecino in vecinos:
                frontera.appendleft((vecino, path+[vecino]))

def greedy( node_count, edge_count, edges):
    grado = dict_grado(node_count, edges)
    nodos = sorted(list(grado.keys()), key=lambda n : grado[n])
    vecinos = dict_adya(node_count, edges)
    restricciones = { f'N{i}': [] for i in range(node_count)}
    sol={}
    def ordenaNodos(nodos, nodo_asignado):
        for vecino in vecinos[nodo_asignado]:
            grado[vecino]-=1
        nodos = sorted(list(grado.keys()), key=lambda n : grado[n])

    while nodos:
        #print(nodos)
        #print(grado)
        nodo = nodos.pop()
        #print(nodo)
        for i in range(node_count+1):
            if i not in restricciones[nodo]:
                sol[nodo] = i
                color = i
                break
        for vecino in vecinos[nodo]:
            restricciones[vecino].append(color)
        ordenaNodos(nodos, nodo)

    # print('Es solucion', es_sol(node_count, edges,sol))
    # print('Sol',sol)
    return output_string(sol)
    



def csp_greedy(node_count, edge_count, edges):
    debug = False
    num_colors = node_count
    restricciones = [ Restriccion([f'N{edge[0]}', f'N{edge[1]}'], lambda x, y : x != y) for edge in edges]
    grado = { f'N{i}': 0 for i in range(node_count)}
    for edge in edges:
        grado[f'N{edge[0]}']+=1
        grado[f'N{edge[1]}']+=1
    #print('Grado de nodos', grado)
    nodos_ordenados = sorted(set(grado), key=lambda n : grado[n], reverse=True)
    #print('Nodos ordenados por grado', nodos_ordenados)
    dominios = { f'N{i}':range(num_colors) for  i in range(node_count) }
    #print(dominios)
    csp = CSP(dominios, restricciones)

    def goal(nodo):
        return len(nodo) == node_count
    def expande(nodo):
        """ nodo es un un diccionario variable: valor """
        variable = nodos_ordenados[len(nodo)]
        max_color = max(nodo.values()) if len(nodo) > 0 else -1
        vecinos = []
        for value in range(min(max_color+1, num_colors), -1, -1):
            assigment = dict_union(nodo, {variable:value})
            #print('Assignment: ', assigment)
            if csp.consistente_var(assigment,variable):
                vecinos.append(assigment)
                if value <= max_color:
                    break
        # print('Genera vecinos :', len(vecinos) , ' para valores : ', range(min(max_color+2, num_colors )))
        sys.stdout.write(f"\rLleva {len(nodo)} nodos coloreados , var actual: {variable} , vecinos: {len(vecinos)} ")
        sys.stdout.flush()
        # print(vecinos)
        # print('Max_color', max_color)
        return vecinos

    res = generalSearch(goal, expande)
    print('\n\nResultado',res[0])
    print(f'Num colores{len(set(res[0].values()))}')

def csp(node_count, edge_count, edges, num_colors=1000):
    debug = False
    restricciones = [ Restriccion([f'N{edge[0]}', f'N{edge[1]}'], lambda x, y : x != y) for edge in edges]
    grado = { f'N{i}': 0 for i in range(node_count)}
    for edge in edges:
        grado[f'N{edge[0]}']+=1
        grado[f'N{edge[1]}']+=1
    #print('Grado de nodos', grado)
    nodos_ordenados = sorted(list(grado.keys()), key=lambda n : grado[n], reverse=True)
    #print('Nodos ordenados por grado', nodos_ordenados)
    dominios = { f'N{i}':range(num_colors) for  i in range(node_count) }
    #print(dominios)
    csp = CSP(dominios, restricciones)

    def goal(nodo):
        return len(nodo) == node_count
    def expande(nodo):
        """ nodo es un un diccionario variable: valor """
        variable = nodos_ordenados[len(nodo)]
        max_color = max(nodo.values()) if len(nodo) > 0 else -1
        vecinos = []
        for value in range(min(max_color+1, num_colors-1), -1, -1):
            assigment = dict_union(nodo, {variable:value})
            #print('Assignment: ', assigment)
            if csp.consistente_var(assigment,variable):
                vecinos.append(assigment)
        # print('Genera vecinos :', len(vecinos) , ' para valores : ', range(min(max_color+2, num_colors )))
        # sys.stdout.write(f"\rLleva {len(nodo)} nodos coloreados , var actual: {variable} , vecinos: {len(vecinos)} ")
        # sys.stdout.flush()
        # print(vecinos)
        # print('Max_color', max_color)
        return vecinos

    res = generalSearch(goal, expande)
    # print('\n\nResultado',res[0])
    # print('Es sol', es_sol(node_count,edges,res[0]))
    # print(f'Num colores{len(set(res[0].values()))}')
    return output_string(res[0] if res else {})


def prueba( node_count, edge_count, edges):
    print("node_count", node_count)
    print("edge_count", edge_count)
    print("edges", edges)
    grafo = dict_adya(node_count, edges)
    sol = { k:0 for k,v in grafo.items()}
    print(sol)
    print('Es sol', es_sol(node_count, edges, sol))

def trivial_coloring(node_count, edge_count, edges):
    """ every node has its own color """
    colores = range(0, node_count)

    # Convertimos la solución en el formato esperado
    output_data = str(node_count) + '\n'
    output_data += ' '.join(map(str, colores))

    return output_data
    



## TODO: Modifica este diccionario
algorithms = {
    'trivial_coloring': trivial_coloring,
    'p': prueba,
    'csp': csp,
    'greedy': greedy
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
        algo_name = sys.argv[2].strip().split('_')
        if algo_name[0] == 'csp':
            algorithm = partial(csp, num_colors=int(algo_name[1]))
        else:
            algorithm = algorithms[sys.argv[2].strip()]

        print(f"Ejecutando el algoritmo {algorithm} en {file_location}")
        
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        #print(solve_it(input_data, algorithm))
        sol=solve_it(input_data, algorithm)
        print(sol)
        f = open("colores.txt", "a")
        f.write(f"{file_location} {sys.argv[2].strip()} {sol}\n")
        f.close()
    else:
        print("""Este script requiere dos argumentos: \n"""
              """El archivo con los datos del problema y el nombre del algoritmo que diseñaste.\n"""
              """i.e. python solver.py ./data/gc_4_1 trivial_coloring""")
