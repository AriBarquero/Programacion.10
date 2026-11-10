from collections import deque 

red = { 
    "Santiago": ["Mercedes Sur", "Barbacoas", "Candelarita"],
    "Mercedes Sur": ["Santiago", " San Rafael"],
    "San Rafael": ["Mercedes Sur", " Grifo Alto"], 
    "Grifo Alto": [ " Barbacoas", "San Rafael"],
    "Barbacoas": [ "Santiago","Grifo Alto"],
    "Candelarita": [ "Santiago"],
    "Desamparaditos": ["Chires"],
    "Chires": ["Desamparaditos"],
    "Zapatón": []
}

obras = {                                     
    "Estudio" : [ "Permisos", "Materiales" ], 
    "Permisos" : [ "Excavación"],             
    "Excavación" : [ "Alcantarillado"],   
    "Alcantarillado": ["Asfaltado"],
    "Asfaltado": ["Señalización"],
    "Señalización": []                                                                                        
}                                          

def normalizar(texto):
    return texto.strip().tittle()

def dfs_iterativo(grafo, inicio):
    if inicio not in grafo:
        return []
    
    visitados = []
    pila = [inicio]
    marcados = set()
    
    while pila:
        actual = pila.pop()
        if actual not in marcados:
            marcados.add(actual)
            visitados.append(actual)
            for vecino in reversed(grafo[actual]):
                if vecino not in marcados:
                    pila.append(vecino)
    return visitados


def ruta_mas_corta(grafo, inicio, destino):
    if inicio not in grafo or destino not in grafo:
        return None
    if inicio == destino:
        return None   
    
    cola = deque([inicio])
    padres = {inicio: None}
    
    while cola:
        actual = cola.popleft()
        if actual == destino:
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]
            return ruta[::-1]
        
        for vecino in grafo[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return None


def contar_componentes(grafo):
    visitados = set()
    componentes = {}
    num_componente = 0
    
    for comunidad in grafo: 
     if comunidad not in visitados:
        num_componente += 1
          pila = [comunidad]
          while pila:
              actual = pila.pop()
                if actual not in visitados:
                    visitados.add(actual)
                    componentes[actual] = num_componente
                 for vecino in reversed(grafo[actual]):
                        if vecino not in visitados:
                            pila.append(vecino)
    
    return num_componente, componentes


def tiene_ciclo(grafo):
    visitados = set()
    
    def dfs(nodo, padre):
        visitados.add(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                if dfs(vecino, nodo):
                    return True
            elif vecino != padre:
                return True 
        return False
    
    for nodo in grafo:
        if nodo not in visitados:
            if dfs(nodo, None):
                return True
    return False


def orden_topologico(grafo):
    grado = {nodo: 0 for nodo in grafo}
    for nodo in grafo:
        for vecino in grafo[nodo]:
            grado[vecino] += 1
    cola = deque([nodo for nodo in grafo if grado[nodo] == 0])
    orden = []
    
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for vecino in grafo[actual]:
            grado[vecino] -= 1
            if grado[vecino] == 0:
                cola.append(vecino)
    
    return orden


def mostrar_menu():
    print("\n=== RED VIAL DE PURISCAL ===")
    print("1. Ver la red de caminos")
    print("2. Agregar un camino")
    print("3. Comunidades alcanzables desde una comunidad")
    print("4. Ruta con menos tramos entre dos comunidades")
    print("5. Componentes conexas de la red")
    print("6. Detectar caminos circulares")
    print("7. Orden de ejecución de las obras")
    print("8. Agregar un prerrequisito entre obras")
    print("9. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()
        
        if opcion == "1":
            print("\nRed de caminos de Puriscal")
            total_grados = 0
            for comunidad, vecinos in red.items():
                grado = len(vecinos)
                total_grados += grado
                if grado == 0:
                    print(f"{comunidad} (grado 0): sin caminos")
                else:
                    print(f"{comunidad} (grado {grado}): {', '.join(vecinos)}")
            print(f"Total de caminos: {total_grados // 2}")
        
        elif opcion == "2":
            c1 = normalizar(input("Comunidad 1: "))
            c2 = normalizar(input("Comunidad 2: "))
            
            if c1 not in red or c2 not in red:
                print("Error: alguna comunidad no existe")
            elif c1 == c2:
                print("Error: ambas comunidades son la misma")
            elif c2 in red[c1]:
                print("Error: ya existe un camino entre esas comunidades.")
            else:
                red[c1].append(c2)
                red[c2].append(c1)
                print(f"Camino agregado entre {c1} y {c2}.")
        
        elif opcion == "3":
            inicio = normalizar(input("Comunidad de inicio: "))
            if inicio not in red:
                print("Error: la comunidad no existe.")
            else:
                visitados = dfs_iterativo(red, inicio)
                print(f"Comunidades alcanzables: {len(visitados)}")
                print(" -> ".join(visitados))
        
        elif opcion == "4":
            origen = normalizar(input("Comunidad origen: "))
            destino = normalizar(input("Comunidad destino: "))
            
            if origen not in red or destino not in red:
                print("Error: una o ambas comunidades no existen.")
            elif origen == destino:
                print("Error: el origen y el destino son la misma comunidad.")
            else:
                ruta = ruta_mas_corta(red, origen, destino)
                if ruta is None:
                    print("Las comunidades no están comunicadas.")
                else:
                    print(" -> ".join(ruta))
                    print(f"Cantidad de tramos: {len(ruta) - 1}")
        
        elif opcion == "5":
            cantidad, componentes = contar_componentes(red)

            grupos = {}
            for comunidad in red:
                num = componentes[comunidad]
                if num not in grupos:
                    grupos[num] = []
                grupos[num].append(comunidad)
            
            for num in sorted(grupos):
                print(f"Componente {num}: {', '.join(grupos[num])}")
            
            print(f"Total de componentes: {cantidad}")
            if cantidad == 1:
                print("Todas las comunidades están comunicadas entre sí.")
            else:
                print("No todas las comunidades están comunicadas entre sí.")
        
        elif opcion == "6":
            hay_ciclo = tiene_ciclo(red)
            cantidad, _ = contar_componentes(red)
            n = len(red)
            total_caminos = sum(len(v) for v in red.values()) // 2
            esperado = n - cantidad
            
            print(f"Método DFS: {'Sí hay ciclos' if hay_ciclo else 'No hay ciclos'}")
            print(f"Método conteo: caminos reales = {total_caminos}, esperados sin ciclos = {esperado}")
            if (hay_ciclo and total_caminos > esperado) or (not hay_ciclo and total_caminos == esperado):
                print("Los dos métodos coinciden.")
            else:
                print("Los dos métodos NO coinciden.")
        
        elif opcion == "7":
            orden = orden_topologico(obras)
            if len(orden) == len(obras):
                print(" -> ".join(orden))
            else:
                print("Existe un ciclo de prerrequisitos.")
                bloqueadas = [obra for obra in obras if obra not in orden]
                print("Obras bloqueadas:", ", ".join(bloqueadas))
        
        elif opcion == "8":
            previa = normalizar(input("Obra previa (la que debe terminar primero): "))
            dependiente = normalizar(input("Obra que depende de ella: "))
            
            if previa not in obras or dependiente not in obras:
                print("Error: una o ambas obras no existen.")
            elif previa == dependiente:
                print("Error: una obra no puede depender de sí misma.")
            elif dependiente in obras[previa]:
                print("Error: esa dependencia ya existe.")
            else:
                obras[previa].append(dependiente)
                print(f"Prerrequisito agregado: {previa} -> {dependiente}")
        
        elif opcion == "9":
            print("¡Hasta luego! Programa terminado.")
            break
        
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()