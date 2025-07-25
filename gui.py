from tkinter import scrolledtext 
from tkinter.ttk import Combobox
import tkinter as tk
from controlador import *
import minizinc
import os
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Minimización del Extremismo")
ventana.geometry("650x625")
ventana.resizable(False, False)

# Encabezado
frame_encabezado = tk.Frame(ventana, pady=10)
frame_encabezado.pack()
texto_inicial = tk.Label(frame_encabezado, text="Minimización del Extremismo", font=("Arial", 16, "bold"))
texto_inicial.pack()
subtexto_inicial = tk.Label(frame_encabezado, text="Oprima el botón para cargar su población en formato .txt", font=("Arial", 10))
subtexto_inicial.pack()

# Entrada para cargar archivo
frame_archivo = tk.Frame(ventana, pady=10)
frame_archivo.pack(fill="x", padx=20)
texto_archivo = tk.Label(frame_archivo, text="Seleccione un archivo:", anchor="w")
archivo_seleccionado = tk.StringVar()
campo_archivo = tk.Entry(frame_archivo, textvariable=archivo_seleccionado, width=72, state="readonly")
campo_archivo.pack(side="left", pady=5, padx=5)
boton_cargar = tk.Button(frame_archivo, text="Cargar Archivo", command=lambda: cargar_archivo(archivo_seleccionado, valorN_var, valorM_var, valorP, valorExt, valorCe, valorCij, valorCt_var, valorMaxM_var),bg="#D1C4E9", fg="black")
boton_cargar.pack(side="left", pady=5, padx=5)

# Panel variables
canvasVariables = tk.Frame(ventana, pady=10)
canvasVariables.pack(side="top", pady=10, anchor="center")

label_font = ("Arial", 10, "bold")
input_font = ("Arial", 12)
label_width = 7
input_width = 22

# Fila 1
labelN = tk.Label(canvasVariables, text="n =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelN.grid(row=0, column=0, padx=(8,2), pady=5, sticky="e")
valorN_var = tk.StringVar()
valorN = tk.Entry(canvasVariables, textvariable=valorN_var, width=input_width, font=input_font, state="readonly", justify="left")
valorN.grid(row=0, column=1, padx=(2,8), pady=5, sticky="w")
labelM = tk.Label(canvasVariables, text="m =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelM.grid(row=0, column=2, padx=(8,2), pady=5, sticky="e")
valorM_var = tk.StringVar()
valorM = tk.Entry(canvasVariables, textvariable=valorM_var, width=input_width, font=input_font, state="readonly", justify="left")
valorM.grid(row=0, column=3, padx=(2,8), pady=5, sticky="w")

# Fila 2
labelP = tk.Label(canvasVariables, text="p =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelP.grid(row=1, column=0, padx=(8,2), pady=5, sticky="e")
valorP = scrolledtext.ScrolledText(canvasVariables, wrap=tk.WORD, width=input_width, height=3, font=input_font)
valorP.config(state=tk.DISABLED)
valorP.grid(row=1, column=1, padx=(2,8), pady=5, sticky="w")
labelExt = tk.Label(canvasVariables, text="ext", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelExt.grid(row=1, column=2, padx=(8,2), pady=5, sticky="e")
valorExt = scrolledtext.ScrolledText(canvasVariables, wrap=tk.WORD, width=input_width, height=3, font=input_font)
valorExt.config(state=tk.DISABLED)
valorExt.grid(row=1, column=3, padx=(2,8), pady=5, sticky="w")

# Fila 3
labelCe = tk.Label(canvasVariables, text="ce =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelCe.grid(row=2, column=0, padx=(8,2), pady=5, sticky="e")
valorCe = scrolledtext.ScrolledText(canvasVariables, wrap=tk.WORD, width=input_width, height=3, font=input_font)
valorCe.config(state=tk.DISABLED)
valorCe.grid(row=2, column=1, padx=(2,8), pady=5, sticky="w")


labelCij = tk.Label(canvasVariables, text="cij =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelCij.grid(row=2, column=2, padx=(8,2), pady=5, sticky="e")
# Text con scroll horizontal y vertical
valorCij = tk.Text(canvasVariables, wrap=tk.NONE, width=input_width, height=3, font=input_font, state="disabled")
valorCij.grid(row=2, column=3, padx=(2,0), pady=5, sticky="nsew")
scroll_y_cij = tk.Scrollbar(canvasVariables, orient=tk.VERTICAL, command=valorCij.yview)
scroll_y_cij.grid(row=2, column=4, sticky="ns", pady=5)

scroll_x_cij = tk.Scrollbar(canvasVariables, orient=tk.HORIZONTAL, command=valorCij.xview)
scroll_x_cij.grid(row=2, column=3, padx=(2,0), pady=(0,0), sticky="sew")
valorCij.configure(yscrollcommand=scroll_y_cij.set, xscrollcommand=scroll_x_cij.set)

# Fila 4
labelCt = tk.Label(canvasVariables, text="ct =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelCt.grid(row=3, column=0, padx=(8,2), pady=5, sticky="e")
valorCt_var = tk.StringVar()
valorCt = tk.Entry(canvasVariables, textvariable=valorCt_var, width=input_width, font=input_font, state="readonly", justify="left")
valorCt.grid(row=3, column=1, padx=(2,8), pady=5, sticky="w")
labelMax = tk.Label(canvasVariables, text="maxM =", borderwidth=1, width=label_width, height=2, font=label_font, anchor="e", justify="right")
labelMax.grid(row=3, column=2, padx=(8,2), pady=5, sticky="e")
valorMaxM_var = tk.StringVar()
valorMaxM = tk.Entry(canvasVariables, textvariable=valorMaxM_var, width=input_width, font=input_font, state="readonly", justify="left")
valorMaxM.grid(row=3, column=3, padx=(2,8), pady=5, sticky="w")


# Botón de procesar archivo
frame_boton = tk.Frame(ventana, pady=10)
frame_boton.pack()
boton = tk.Button(frame_boton, text="Obtener Resultados",  width=20, bg="#F8BBD0", fg="black")
boton_resultado = tk.Button(frame_boton, text="Obtener Resultado", command=lambda: resultado(ventana_resultado),width=20, bg="#F8BBD0", fg="black")
boton_resultado.pack()

#Ventana para mostrar resultados:

frame_resultado = tk.Frame(ventana)
frame_resultado.pack(fill="both", expand=True, padx=20, pady=10)
frame_resultado.grid_rowconfigure(0, weight=1)
frame_resultado.grid_columnconfigure(0, weight=1)

ventana_resultado = scrolledtext.ScrolledText(frame_resultado, wrap=tk.NONE, width=40, height=10, font=("Arial", 12))
ventana_resultado.grid(row=0, column=0, sticky="nsew")

scroll_x = tk.Scrollbar(frame_resultado, orient=tk.HORIZONTAL, command=ventana_resultado.xview)
scroll_x.grid(row=1, column=0, sticky="ew")
ventana_resultado.configure(xscrollcommand=scroll_x.set)

ventana.mainloop()