import tkinter as tk
from tkinter import messagebox
import threading
import time
import archivos_de_procesos as ap 

class Proceso:
    def __init__(self, pid, nombre, tiempo):
        self.pid = pid
        self.nombre = nombre
        self.tiempo_restante = tiempo
        self.estado = "LISTO"
    def __str__(self):
        return f"PID: {self.pid:02} | {self.nombre:12} | {self.tiempo_restante:02}s | {self.estado}"

class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador SO - ITSON")
        self.root.geometry("650x600")
        self.procesos = []

        # --- DICCIONARIO DE TEMAS ---
        self.temas = {
            "Negro": {"bg": "#1e1e1e", "fg": "#00ff00", "list_bg": "#121212", "btn": "#333333", "text": "white"},
            "Blanco": {"bg": "#f0f0f0", "fg": "#000000", "list_bg": "#928b8b", "btn": "#c6b9b9", "text": "black"},
            "Caqui": {"bg": "#8B7D67", "fg": "#030302", "list_bg": "#E6D5AC", "btn": "#C0B2A0", "text": "#3e352f"}
        }

        # --- BARRA SUPERIOR PARA EL MENÚ DE TEMAS ---
        self.frame_superior = tk.Frame(root)
        # Cambia px=20 por padx=20
        self.frame_superior.pack(pady=10, fill="x", padx=20)
        
        tk.Label(self.frame_superior, text="Temas disponibles:", font=("Arial", 9)).pack(side="left", padx=5)
        
        self.var_tema = tk.StringVar(value="Negro")
        # El OptionMenu crea la "barra" que se despliega al tocarla
        self.menu_temas = tk.OptionMenu(self.frame_superior, self.var_tema, *self.temas.keys(), command=self.cambiar_tema)
        self.menu_temas.config(width=10)
        self.menu_temas.pack(side="left")

        # --- COMPONENTES VISUALES ---
        self.lbl_titulo = tk.Label(root, text="SIMULADOR DE PROCESOS", font=("Courier New", 16, "bold"))
        self.lbl_titulo.pack(pady=10)
        
        self.frame_archivo = tk.Frame(root)
        self.frame_archivo.pack(pady=5)
        self.btn_gen = tk.Button(self.frame_archivo, text="GENERAR LISTA DE PROCESOS", command=self.boton_generar_click)
        self.btn_gen.pack(side="left", padx=5)
        self.btn_car = tk.Button(self.frame_archivo, text="CARGAR", command=self.boton_cargar_click)
        self.btn_car.pack(side="left", padx=5)

        self.lista_visual = tk.Listbox(root, font=("Courier New", 11), width=65, height=12, borderwidth=0, highlightthickness=1)
        self.lista_visual.pack(pady=15, padx=20)

        self.frame_control = tk.Frame(root)
        self.frame_control.pack(pady=10)
        self.btn_fcfs = tk.Button(self.frame_control, text="CORRER FCFS", command=lambda: self.iniciar_hilo("FCFS"), bg="#2ecc71", font=("Arial", 9, "bold"), width=12)
        self.btn_fcfs.pack(side="left", padx=10)
        self.btn_rr = tk.Button(self.frame_control, text="CORRER RR", command=lambda: self.iniciar_hilo("RR"), bg="#e67e22", font=("Arial", 9, "bold"), width=12)
        self.btn_rr.pack(side="left", padx=10)
        
        self.lbl_q = tk.Label(self.frame_control, text="Quantum:")
        self.lbl_q.pack(side="left", padx=5)
        self.entry_quantum = tk.Entry(self.frame_control, width=5)
        self.entry_quantum.insert(0, "3")
        self.entry_quantum.pack(side="left", padx=5)

        # Aplicar tema inicial
        self.cambiar_tema()

    def cambiar_tema(self, *args):
        # Seleccionamos el tema del diccionario
        t = self.temas[self.var_tema.get()]
        
        # Colores de fondo de contenedores
        self.root.configure(bg=t["bg"])
        self.frame_superior.configure(bg=t["bg"])
        self.frame_archivo.configure(bg=t["bg"])
        self.frame_control.configure(bg=t["bg"])
        
        # Colores de textos y etiquetas
        self.lbl_titulo.configure(bg=t["bg"], fg=t["fg"])
        self.lbl_q.configure(bg=t["bg"], fg=t["text"])
        
        # Estilo de botones
        self.btn_gen.configure(bg=t["btn"], fg=t["text"])
        self.btn_car.configure(bg=t["btn"], fg=t["text"])
        self.menu_temas.configure(bg=t["btn"], fg=t["text"])
        
        # Estilo de la lista de procesos
        self.lista_visual.configure(bg=t["list_bg"], fg=t["fg"], highlightcolor=t["fg"])
        self.entry_quantum.configure(bg=t["btn"], fg=t["text"], insertbackground=t["text"])

    def boton_generar_click(self):
        ap.generar_aleatorios()
        self.boton_cargar_click()

    def boton_cargar_click(self):
        datos = ap.leer_archivo()
        if datos:
            self.procesos = [Proceso(i+1, n, t) for i, (n, t) in enumerate(datos)]
            self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_visual.delete(0, tk.END)
        for p in self.procesos:
            self.lista_visual.insert(tk.END, str(p))

    def iniciar_hilo(self, algoritmo):
        if not self.procesos: return
        threading.Thread(target=lambda: self.ejecutar(algoritmo), daemon=True).start()

    def ejecutar(self, algoritmo):
        if algoritmo == "FCFS":
            for p in self.procesos:
                if p.estado == "TERMINADO": continue
                p.estado = "EJECUTANDO"
                while p.tiempo_restante > 0:
                    self.actualizar_lista(); time.sleep(1); p.tiempo_restante -= 1
                p.tiempo_restante = 0; p.estado = "TERMINADO"
                self.actualizar_lista()
        
        elif algoritmo == "RR":
            q = int(self.entry_quantum.get())
            while any(p.estado != "TERMINADO" for p in self.procesos):
                for p in self.procesos:
                    if p.estado == "TERMINADO": continue
                    p.estado = "EJECUTANDO"
                    t_correr = min(p.tiempo_restante, q)
                    for _ in range(t_correr):
                        if p.tiempo_restante > 0:
                            self.actualizar_lista(); time.sleep(1); p.tiempo_restante -= 1
                    p.estado = "TERMINADO" if p.tiempo_restante <= 0 else "LISTO"
                    if p.estado == "TERMINADO": p.tiempo_restante = 0
                    self.actualizar_lista()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()