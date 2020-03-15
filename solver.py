#!/usr/bin/python
# -*- coding: utf-8 -*-

def trivial_coloring(node_count, edge_count, edges):
    """ every node has its own color """
    colores = range(0, node_count)

    # Convertimos la solución en el formato esperado
    output_data = str(node_count) + '\n'
    output_data += ' '.join(map(str, colores))

    return output_data
    

## TODO: Modifica este diccionario
algorithms = {'trivial_coloring': trivial_coloring}

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
