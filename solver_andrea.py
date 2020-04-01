#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import deque
from CSP import Constraint, CSP

def parse_solution(colors, assignments):
    output_data = f'{len(colors)}\n'
    output_data += ' '.join(map(str, assignments.values()))

    return output_data

def make_graph(node_count, edges):
    graph = {}
    connections = {}
    restrictions = {}
    
    for n in range(node_count):
        graph[n] = set()
        connections[n] = 0
        restrictions[n] = set()

    for x,y in edges:
        graph[x].add(y)
        graph[y].add(x)

        connections[x] += 1
        connections[y] += 1
    
    return graph, connections, restrictions

def get_color(colors, restriction):
    available_colors = colors - restriction

    if len(available_colors) == 0:
        return max(colors) + 1
    else:
        return min(available_colors)
#-------------------------------------------------------------------------------
#
#                           SEARCH METHODS
#
#-------------------------------------------------------------------------------
def dfs_with_prunning(goal, gen_neighbors, number_colors, bound=float('inf')):
    best_path = None
    best_cost = bound
    
    frontera = deque()  

    frontera.appendleft(({}, [{}])) # nodo y path
    
    while frontera:
        nodes, path = frontera.popleft() # Extraigo por la izquierda
        #print(f'Nodo a explorar: {nodes}')
        if number_colors(nodes) < best_cost:
            if goal(nodes):
                best_solution = nodes
                best_cost = number_colors(nodes)
                #print(f"Mejor solución encontrada: {best_solution} con valor {best_cost}")
            else:            
                neighbors = reversed(gen_neighbors(nodes))
                for neighbor in neighbors:
                    frontera.appendleft((neighbor, path + [neighbor]))
        #else:
            #print(f'{nodes} ha sido podado')
        
        #print('----'*30)
        #print()
    return best_solution, best_cost

def bfs_search(goal, gen_neighbors):
    border = deque()

    border.append(({}, [{}]))

    while border:
        nodes, path = border.popleft()
        #print('NODES: ',nodes)
        #print('PATH: ', path)
        if goal(nodes):
            best_path = path
            best_sol = nodes
            return best_sol, best_path
        else:
            neighbors = gen_neighbors(nodes)
            #print(neighbors)
            neighbors = reversed(neighbors)
            
            for neighbor in neighbors:
                border.appendleft((neighbor, path + [neighbor]))

        #print()
        #print("====="*30)
        #print()

#-------------------------------------------------------------------------------
#
#                           PROBLEM SOLVERS
#
#-------------------------------------------------------------------------------
def csp_solver(node_count, edge_count, edges):
    def get_degree(edges, node_count):
        degree = {n:0 for n in range(node_count)}
        for x,y in edges:
            degree[x] += 1
            degree[y] += 1
        return degree

    def goal(nodes):
        return len(nodes) == node_count

    def gen_neighbors(nodes):
        node = list(csp.variables)[len(nodes)]
        #print('NEW NODE: ', node)
        neighbors = []
        colors = (csp.domain).copy()

        for color in colors:
            assignment = nodes.copy()
            assignment.update({node:color})

            if csp.consistent_var(assignment, node):
                neighbors.append(assignment)


        if len(neighbors) == 0:
            new_color = max(colors) + 1
            assignment = nodes.copy()
            assignment.update({node:new_color})

            if csp.consistent_var(assignment, node):
                neighbors.append(assignment)
                colors.add(new_color)
                csp.update_domain(colors)

        return neighbors

    constraints = [Constraint(scope = edge, predicate = lambda x,y: x != y) for edge in edges]

    domain = {1}
    degree  = get_degree(edges, node_count)
    sorted_variables = sorted(degree, key = lambda n: degree[n], reverse = True)

    #print(constraints)
    csp = CSP(domain, constraints, variables=sorted_variables)

    assignments, path = bfs_search(goal, gen_neighbors)
    colors = set(assignments.values())

    return colors, assignments

def csp_optimum(node_count, edge_count, edges):
    def get_degree(edges, node_count):
        degree = {n:0 for n in range(node_count)}
        for x,y in edges:
            degree[x] += 1
            degree[y] += 1
        return degree

    def goal(nodes):
        return len(nodes) == node_count

    def gen_neighbors(nodes):
        node = list(csp.variables)[len(nodes)]
        neighbors = []
        #colors = (csp.domain).copy()
        colors = set(nodes.values()) if len(nodes) > 0 else {1}
        for color in colors:
            assignment = nodes.copy()
            assignment.update({node:color})

            if csp.consistent_var(assignment, node):
                neighbors.append(assignment)


        if len(neighbors) == 0:
            new_color = max(colors) + 1
            assignment = nodes.copy()
            assignment.update({node:new_color})
            
            if csp.consistent_var(assignment, node):
                neighbors.append(assignment)
                #colors.add(new_color)
                #csp.update_domain(colors)

        #print('Colors: ', colors)

        return neighbors

    def number_colors(nodes):
        return len(set(nodes.values()))

    constraints = [Constraint(scope = edge, predicate = lambda x,y: x != y) for edge in edges]

    #colors = set(range(1, node_count+1))
    #domains = {n: colors for n in range(node_count)}

    domain = {1}
    degree  = get_degree(edges, node_count)
    sorted_variables = sorted(degree, key = lambda n: degree[n], reverse = True)
    #print('VARIABLES: ', sorted_variables)
    csp = CSP(domain, constraints, variables=sorted_variables)

    assignments, path = dfs_with_prunning(goal, gen_neighbors, number_colors, bound = node_count)
    colors = set(assignments.values())

    return colors, assignments

def trivial_greedy(node_count, edge_count, edges):
    graph, connections, restrictions = make_graph(node_count, edges)

    colors = {1}
    assignments = {}

    sorted_nodes = sorted(connections, key = lambda x: connections[x], reverse = True)

    for node in sorted_nodes:
        color = get_color(colors, restrictions[node])
        
        colors.add(color)
        assignments[node] = color

        for neighbor in graph[node]:
            restrictions[neighbor].add(color)

    return colors, assignments

def complex_greedy(node_count, edge_count, edges):
    def make_assignment(color, selected_node, graph, restrictions, connections):
        for node in graph[selected_node]:
            restrictions[node].add(color)
            connections[node] -= 1
            graph[node].remove(selected_node)

        connections.pop(selected_node)

    graph, connections, restrictions = make_graph(node_count, edges)


    colors = {1}
    assignments = {}

    while len(connections) > 0:
        node = max(connections, key = lambda x: connections[x])

        color = get_color(colors, restrictions[node])
        assignments[node] = color
        colors.add(color)

        make_assignment(color, node, graph, restrictions, connections)

    return colors, assignments

#-------------------------------------------------------------------------------
#
#                           MAIN FUNCTIONS
#
#-------------------------------------------------------------------------------
algorithms = {'complex_greedy': complex_greedy,
              'trivial_greedy': trivial_greedy,
              'csp': csp_solver,
              'csp_prunning': csp_optimum         
}

def solve_it(input_data, algorithm=trivial_greedy):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    node_count = int(firstLine[0])
    edge_count = int(firstLine[1])

    edges = []

    for i in range(1, edge_count+1):
        line = lines[i]
        parts = line.split()

        x = int(parts[0])
        y = int(parts[1])

        edges.append((int(parts[0]), int(parts[1])))

    colors, assignments = algorithm(node_count, edge_count, edges)

    #print('COLORS: ', colors)

    output_data = parse_solution(colors, assignments)

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        file_location = sys.argv[1].strip()
        algorithm = algorithms[sys.argv[2].strip()]

        print(f"Ejecutando el algoritmo {algorithm} en {file_location}")
        
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        #solve_it(input_data, algorithm)

        print(solve_it(input_data, algorithm))
    else:
        print("""Este script requiere dos argumentos: \n"""
              """El archivo con los datos del problema y el nombre del algoritmo que diseñaste.\n"""
              """i.e. python solver.py ./data/gc_4_1 trivial_coloring""")
