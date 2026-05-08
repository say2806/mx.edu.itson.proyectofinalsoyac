import random
import os

def generar_aleatorios():
    # Lista de posibles nombres
    apps = ["Chrome", "Spotify", "VSCode", "Discord", "Zoom", "Excel", "Steam", 
            "Kernel", "Word", "Photoshop", "Terminal", "Edge"]
    
    # Decidimos cuántos procesos queremos (mínimo 5, máximo el total de la lista)
    cantidad = random.randint(5, 8)
    
    # CLAVE: random.sample elige N elementos SIN REPETIR de la lista
    seleccionados = random.sample(apps, cantidad)
    
    with open("procesos.txt", "w") as f:
        for nombre in seleccionados:
            tiempo = random.randint(3, 12)
            f.write(f"{nombre},{tiempo}\n")

def leer_archivo():
    lista_datos = []
    if os.path.exists("procesos.txt"):
        with open("procesos.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    lista_datos.append((partes[0], int(partes[1])))
    return lista_datos