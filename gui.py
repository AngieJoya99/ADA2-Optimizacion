from tkinter import scrolledtext 
from tkinter.ttk import Combobox
import tkinter as tk
from controlador import *
import minizinc
import os

ventana = tk.Tk()
ventana.title("Moderador del conflicto interno")
ventana.geometry("600x625")
ventana.resizable(False, False)

# Encabezado
frame_encabezado = tk.Frame(ventana, pady=10)
frame_encabezado.pack()
texto_inicial = tk.Label(frame_encabezado, text="MCI", font=("Arial", 16, "bold"))
texto_inicial.pack()
subtexto_inicial = tk.Label(frame_encabezado, text="Complete los campos para procesar su red social", font=("Arial", 10))
subtexto_inicial.pack()

# Entrada para cargar archivo
frame_archivo = tk.Frame(ventana, pady=10)
frame_archivo.pack(fill="x", padx=20)
texto_archivo = tk.Label(frame_archivo, text="Seleccione un archivo:", anchor="w")
archivo_seleccionado = tk.StringVar()
campo_archivo = tk.Entry(frame_archivo, textvariable=archivo_seleccionado, width=72, state="readonly")
campo_archivo.pack(side="left", pady=5, padx=5)
boton_cargar = tk.Button(frame_archivo, text="Cargar Archivo", command=lambda: cargar_archivo(archivo_seleccionado, ventana_entrada) ,bg="#D1C4E9", fg="black")
boton_cargar.pack(side="left", pady=5, padx=5)

#Ventana para mostrar entrada:
ventana_entrada = scrolledtext.ScrolledText(wrap = tk.WORD,  width = 40,  height = 10, font =("Arial", 12)) 
ventana_entrada.config(state=tk.DISABLED)
ventana_entrada.pack()

# Selección de algoritmo
frame_algoritmo = tk.Frame(ventana, pady=10)
frame_algoritmo.pack(fill="x", padx=20)
texto_algoritmo = tk.Label(frame_algoritmo, text="Seleccione un algoritmo:", anchor="w")
texto_algoritmo.pack(fill="x")
opcion_alg = tk.StringVar()
combobox_alg = Combobox(frame_algoritmo, textvariable=opcion_alg, state="readonly", values=["Fuerza Bruta", "Dinámica", "Voraz"])
combobox_alg.current(0)
combobox_alg.pack(pady=5)

# Botón de procesar archivo
frame_boton = tk.Frame(ventana, pady=10)
frame_boton.pack()
boton = tk.Button(frame_boton, text="Obtener Resultados",  width=20, bg="#F8BBD0", fg="black")
boton.pack()

#Ventana para mostrar resultados:
ventana_resultado = scrolledtext.ScrolledText(wrap = tk.WORD,  width = 40,  height = 10, font =("Arial", 12)) 
ventana_resultado.config(state=tk.DISABLED)
ventana_resultado.pack()

# Iniciar la interfaz
ventana.mainloop()