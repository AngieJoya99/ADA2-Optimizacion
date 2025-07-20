from tkinter import filedialog, messagebox
import tkinter as tk
import minizinc
import os

def cargar_archivo(archivo_seleccionado, ventana_entrada):
  global datos
  archivo = filedialog.askopenfilename(
    title="Seleccionar archivo",
    filetypes=[("Archivos de texto", "*.txt")]
  )
  if archivo:
    archivo_seleccionado.set(archivo)  
    try:
      datos = leer_archivo(archivo_seleccionado.get(), ventana_entrada)
      correrModelo(datos)
    except Exception as e:
      print(f"Error al leer el archivo: {e}")  
      raise 
    return archivo  
      
  return None

def leer_archivo(ruta_archivo,ventana_entrada):
  try:
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
      lineas = [linea.strip() for linea in archivo.readlines()]

    if len(lineas) < 8:
      print("El archivo no tiene suficientes líneas.")
      return None

    n = int(lineas[0])
    m = int(lineas[1])
    p = [int(x) for x in lineas[2].split(",")]
    ext = [float(x) for x in lineas[3].split(",")]
    ce = [float(x) for x in lineas[4].split(",")]    
    ct = float(lineas[-2])
    maxM = int(lineas[-1])

    c = []
    for linea in lineas[5:-2]:
      numeros = linea.split(',')
      fila = [float(n) for n in numeros]
      c.append(fila)

    print(ventana_entrada)
    ventana_entrada.configure(state="normal")
    ventana_entrada.delete('1.0', tk.END)
    grupos = '\n'.join(str(sublista) for sublista in c)
    # ventana_entrada.insert(tk.INSERT,"DATOS DE ENTRADA\n\nCantidad de grupos: " +str(primera_linea)+"\n\nEsfuerzo máximo: "+str(ultima_linea)+"\n\nGrupos de agentes:\n"+grupos)
    ventana_entrada.insert(tk.INSERT,f"DATOS DE ENTRADA\n\nn = {n}\nm = {m}\np = {p}\next = {ext}\nce = {ce}\nc = {c}\nct = {ct}\nmaxM = {maxM}\n")
    ventana_entrada.configure(state="disabled")
    
    return [n, m, p, ext, ce,  c, ct, maxM]

  except Exception as e:
    print(f"Ocurrió un error: {e}")
    return None
  
def correrModelo(datos):
  modelo = model = minizinc.Model()
  modelo.add_file("Modelo.mzn")
  
  solver = minizinc.Solver.lookup("gecode")
  instancia = minizinc.Instance(solver, modelo)
  instancia["n"] = datos[0]
  instancia["m"] = datos[1]
  instancia["p"] = datos[2]
  instancia["ext"] = datos[3]
  instancia["ce"] = datos[4]
  instancia["c"] = datos[5]
  instancia["ct"] = datos[6]
  instancia["maxM"] = datos[7]
  
  resultado = instancia.solve()
  print(resultado)
  
  
 