def dict_adya(node_count, edges):
    vecinos = { f'N{i}':[] for i in range(node_count)}
    for edge in edges:
        vecinos[f'N{edge[0]}'].append(f'N{edge[1]}')
        vecinos[f'N{edge[1]}'].append(f'N{edge[0]}')
    return vecinos

def dict_grado(node_count, edges):
    grado = { f'N{i}': 0 for i in range(node_count)}
    for edge in edges:
        grado[f'N{edge[0]}']+=1
        grado[f'N{edge[1]}']+=1
    return grado

def es_sol(node_count, edges, sol):
    vecinos = dict_adya(node_count, edges)
    res = True
    for n, v_n in vecinos.items():
        for v in v_n:
            res = res and sol[n] != sol[v]
    return res

def output_string(sol):
    num_colores = max(sol.values()) + 1
    nodos_en_orden = list(sol.items())
    nodos_en_orden.sort(key=lambda x : int(x[0][1:]))
    #print(nodos_en_orden)
    output_data = str(num_colores) + '\n'
    for nodo in nodos_en_orden:
        output_data += f'{nodo[1]} '
    return output_data
    
def dict_union(d1, d2):
    """ Simplifica la unión de dos diccionarios """
    d = dict(d1)
    d.update(d2)
    return d