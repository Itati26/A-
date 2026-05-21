from arbol import Nodo

# Precios por empresa y tipo de rueda (tabla correcta)
precios = {
    'Empresa1': {'T': 20, 'H': 30, 'V': 20, 'W': 40},
    'Empresa2': {'T': 50, 'H': 50, 'V': 40, 'W': 50},
    'Empresa3': {'T': 60, 'H': 55, 'V': 50, 'W': 60},
    'Empresa4': {'T': 100,'H': 80, 'V': 60, 'W': 70},
}

EMPRESAS = ['Empresa1', 'Empresa2', 'Empresa3', 'Empresa4']
TIPOS    = ['T', 'H', 'V', 'W']


def heuristica(estado):
    empresas_usadas = {e for e, _ in estado}
    tipos_cubiertos = {t for _, t in estado}
    pendientes  = [t for t in TIPOS if t not in tipos_cubiertos]
    disponibles = [e for e in EMPRESAS if e not in empresas_usadas]

    h = 0
    libres = list(disponibles)
    for tipo in pendientes:
        if not libres:
            break
        empresa_min = min(libres, key=lambda e: precios[e][tipo])
        h += precios[empresa_min][tipo]
        libres.remove(empresa_min)
    return h


def buscar_solucion_A(estado_inicial):
    solucionado     = False
    nodos_visitados = []
    nodos_frontera  = []

    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodos_frontera.sort(
            key=lambda x: x.get_costo() + heuristica(x.get_datos())
        )

        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        estado = nodo.get_datos()

        if len(estado) == len(TIPOS):
            solucionado = True
            return nodo

        empresas_usadas = {e for e, _ in estado}
        tipos_cubiertos = {t for _, t in estado}
        pendientes  = [t for t in TIPOS if t not in tipos_cubiertos]
        disponibles = [e for e in EMPRESAS if e not in empresas_usadas]

        siguiente_tipo = pendientes[0]
        lista_hijos = []

        for empresa in disponibles:
            nuevo_estado = estado + ((empresa, siguiente_tipo),)
            hijo = Nodo(nuevo_estado)
            hijo.set_padre(nodo)
            costo_paso = precios[empresa][siguiente_tipo]
            hijo.set_costo(nodo.get_costo() + costo_paso)
            lista_hijos.append(hijo)

            if not hijo.en_lista(nodos_visitados):
                if hijo.en_lista(nodos_frontera):
                    for n in nodos_frontera:
                        if n.igual(hijo) and n.get_costo() > hijo.get_costo():
                            nodos_frontera.remove(n)
                            nodos_frontera.append(hijo)
                else:
                    nodos_frontera.append(hijo)

        nodo.set_hijos(lista_hijos)

    return None


if __name__ == "__main__":
    estado_inicial = ()

    nodo_solucion = buscar_solucion_A(estado_inicial)

    if nodo_solucion is not None:
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()

        print("\nAsignacion optima encontrada:")
        asignacion = nodo_solucion.get_datos()
        for empresa, tipo in sorted(asignacion, key=lambda x: x[1]):
            print(f"  {empresa} -> Tipo {tipo}: ${precios[empresa][tipo]}")

        print(f"\nCosto total: ${nodo_solucion.get_costo()}")
    else:
        print("No se encontro solucion")
