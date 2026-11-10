nombres = {
    "E": "Entrada",
    "C": "Exposición de ciencias",
    "J": "Zona de juegos",
    "R": "Robótica",
    "T": "Talleres",
    "S": "Salida"
}

mapa = {
    "E": ["C", "J"],
    "C": ["E", "R", "T"],
    "J": ["E", "S"],
    "R": ["C", "S"],
    "T": ["C", "S"],
    "S": ["J", "R", "T"]
}

nodos = ["E", "C", "J", "R", "T", "S"]

def construir_matriz(mapa, nodos):
    n = len(nodos)
    matriz = [[0] * n for _ in range(n)]
    indice = {nodo: i for i, nodo in enumerate(nodos)}

    for origen in mapa:
        for destino in mapa[origen]:
            i = indice[origen]
            j = indice[destino]
            matriz[i][j] = 1
    return matriz


def dfs_recursivo(mapa, inicio):
    visitados = set()
    recorrido = []

    def dfs(nodo):
        visitados.add(nodo)
        recorrido.append(nodo)
        for vecino in mapa[nodo]:
            if vecino not in visitados:
                dfs(vecino)

    dfs(inicio)
    return recorrido


def dfs_iterativo(mapa, inicio):
    visitados = set()
    recorrido = []
    pila = [inicio]

    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        recorrido.append(nodo)
        for vecino in reversed(mapa[nodo]):
            if vecino not in visitados:
                pila.append(vecino)

    return recorrido


def mostrar_menu():
    print("=== MAPA DE LA FERIA CIENTÍFICA ===")
    print("1. Ver conexiones de un espacio")
    print("2. Ver matriz de adyacencia")
    print("3. Recorrer con DFS recursivo")
    print("4. Recorrer con DFS iterativo")
    print("5. Consultar si hay un pasillo directo")
    print("6. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nodo = input("Espacio: ").strip().upper()
            if nodo not in mapa:
                print("Ese espacio no existe en el mapa.")
            else:
                vecinos = ", ".join(mapa[nodo])
                print(f"{nodo} · {nombres[nodo]} se conecta con: {vecinos}")

        elif opcion == "2":
            matriz = construir_matriz(mapa, nodos)
            print(" " + " ".join(nodos))
            for i, fila in enumerate(matriz):
                print(nodos[i] + " " + " ".join(str(x) for x in fila))

        elif opcion == "3":
            nodo = input("Nodo inicial: ").strip().upper()
            if nodo not in mapa:
                print("Ese espacio no existe en el mapa.")
            else:
                recorrido = dfs_recursivo(mapa, nodo)
                print(" -> ".join(recorrido))

        elif opcion == "4":
            nodo = input("Nodo inicial: ").strip().upper()
            if nodo not in mapa:
                print("Ese espacio no existe en el mapa.")
            else:
                recorrido = dfs_iterativo(mapa, nodo)
                print(" -> ".join(recorrido))

        elif opcion == "5":
            origen = input("Nodo de origen: ").strip().upper()
            destino = input("Nodo de destino: ").strip().upper()

            if origen not in mapa or destino not in mapa:
                print("Uno o ambos espacios no existen en el mapa.")
            else:
                matriz = construir_matriz(mapa, nodos)
                i = nodos.index(origen)
                j = nodos.index(destino)
                if matriz[i][j] == 1:
                    print(f"Sí existe un pasillo directo entre {origen} y {destino}.")
                else:
                    print(f"No existe un pasillo directo entre {origen} y {destino}.")

        elif opcion == "6":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()