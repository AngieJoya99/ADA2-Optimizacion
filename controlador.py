from tkinter import filedialog, font
import tkinter as tk
import minizinc
import os
import glob
import re
import ast

global n, m, p, ext, ce, c, ct, maxM

def encontrar_gurobi():
  """Encuentra automáticamente la instalación de Gurobi en el sistema"""
  # Rutas comunes donde se instala Gurobi
  rutas_comunes = [
    "/opt/gurobi*/linux64",
    "/usr/local/gurobi*/linux64", 
    "/home/*/gurobi*/linux64",
    "C:/gurobi*/win64",  # Windows
    "/Library/gurobi*/mac64"  # macOS
  ]
  
  for patron in rutas_comunes:
    rutas_encontradas = glob.glob(patron)
    for ruta in rutas_encontradas:
      if os.path.exists(os.path.join(ruta, "lib")):
        return ruta
  
  # Verificar variable de entorno GUROBI_HOME
  if 'GUROBI_HOME' in os.environ:
    return os.environ['GUROBI_HOME']
    
  return None

def configurar_gurobi():
  """Configura las variables de entorno para Gurobi"""
  gurobi_home = encontrar_gurobi()
  
  if gurobi_home is None:
    print("ERROR: No se encontró instalación de Gurobi")
    print("Por favor instale Gurobi o configure la variable GUROBI_HOME")
    return False
  
  # Configurar variables de entorno
  os.environ['GUROBI_HOME'] = gurobi_home
  lib_path = os.path.join(gurobi_home, 'lib')
  
  if 'LD_LIBRARY_PATH' in os.environ:
    os.environ['LD_LIBRARY_PATH'] = lib_path + ':' + os.environ['LD_LIBRARY_PATH']
  else:
    os.environ['LD_LIBRARY_PATH'] = lib_path
    
  print(f"Gurobi configurado en: {gurobi_home}")
  return True

def cargar_archivo(archivo_seleccionado, valorN_var, valorM_var, valorP, valorExt, valorCe, valorCij, valorCt_var, valorMaxM_var):
  archivo = filedialog.askopenfilename(
    title="Seleccionar archivo",
    filetypes=[("Archivos de texto", "*.txt")]
  )
  if archivo:
    archivo_seleccionado.set(archivo)  
    try:
      leer_archivo(archivo_seleccionado.get(), valorN_var, valorM_var, valorP, valorExt, valorCe, valorCij, valorCt_var, valorMaxM_var)
    except Exception as e:
      print(f"Error al leer el archivo: {e}")  
      raise 
    return archivo  
      
  return None

def leer_archivo(ruta_archivo, valorN_var, valorM_var, valorP, valorExt, valorCe, valorCij, valorCt_var, valorMaxM_var):
  global n, m, p, ext, ce, c, ct, maxM
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
    
    valorN_var.set(str(n))
    valorM_var.set(str(m))
    valorCt_var.set(str(ct))
    valorMaxM_var.set(str(maxM))
    
    valorP.config(state=tk.NORMAL)
    valorP.delete('1.0', tk.END)
    valorP.insert(tk.END, str(p)[1:-1])
    valorP.config(state=tk.DISABLED)

    valorExt.config(state=tk.NORMAL)
    valorExt.delete('1.0', tk.END)
    valorExt.insert(tk.END, str(ext)[1:-1])
    valorExt.config(state=tk.DISABLED)
    
    valorCe.config(state=tk.NORMAL)
    valorCe.delete('1.0', tk.END)
    valorCe.insert(tk.END, str(ce)[1:-1])
    valorCe.config(state=tk.DISABLED)

    valorCij.config(state=tk.NORMAL)
    valorCij.delete('1.0', tk.END)
    for fila in c:
        valorCij.insert(tk.END, str(fila)[1:-1] + '\n')
    valorCij.config(state=tk.DISABLED)
    
    n, m, p, ext, ce, c, ct, maxM

  except Exception as e:
    print(f"Ocurrió un error: {e}")
    return None
  
def correrModelo():
  global n, m, p, ext, ce, c, ct, maxM
  # Configurar Gurobi automáticamente
  if not configurar_gurobi():
    print("No se puede ejecutar sin Gurobi")
    return None
    
  modelo = model = minizinc.Model()
  modelo.add_file("Modelo.mzn")
  
  try:
    solver = minizinc.Solver.lookup("gurobi")
    print("Usando solver: Gurobi")
  except Exception as e:
    print(f"Error: No se puede usar Gurobi: {e}")
    print("Verifique que Gurobi esté correctamente instalado y licenciado")
    return None
  
  try:
    instancia = minizinc.Instance(solver, modelo)
    instancia["n"] = n
    instancia["m"] = m
    instancia["p"] = p
    instancia["ext"] = ext
    instancia["ce"] = ce
    instancia["c"] = c
    instancia["ct"] = ct
    instancia["maxM"] = maxM
    resultado = instancia.solve()
    return resultado
  except Exception as e:
    print(f"Error ejecutando el modelo con Gurobi: {e}")
    return None
  
def resultado(ventana_resultado):  
  try:
    generarDZN()
    solucion = correrModelo()
    procesarSalida(str(solucion), ventana_resultado)
  except Exception as e:
    print(f"No se pudo solucionar el problema")  
    raise 

def generarDZN():
  global n, m, p, ext, ce, c, ct, maxM
  
  try:
    ruta_archivo = filedialog.asksaveasfilename(
      defaultextension=".dzn",
      filetypes=[("MiniZinc data", "*.dzn")],
      title="Guardar archivo como"
    )
    
    if not ruta_archivo:
      print("Guardado cancelado por el usuario.")
      return None
    
    aplanarCij = [num for fila in c for num in fila]
    
    with open(ruta_archivo, 'w') as file:
      file.write(f"n = {n};\n")
      file.write(f"m = {m};\n")
      file.write(f"p = [{', '.join(map(str, p))}];\n")
      file.write(f"ext = [{', '.join(map(str, ext))}];\n")
      file.write(f"ce = [{', '.join(map(str, ce))}];\n")
      file.write(f"c = array2d(1..{m}, 1..{m}, [{', '.join(map(str, aplanarCij))}]);\n")
      file.write(f"ct = {ct};\n")
      file.write(f"maxM = {maxM};\n")
      
    print(f"Archivo generado en: {os.path.abspath(ruta_archivo)}")  
    return os.path.abspath(ruta_archivo)

  except Exception as e:
    print(f"Error al escribir archivo: {e}")  
    raise 

def procesarSalida(solucion, ventana_resultado):
  
  # Patrón para cada parte
  patron_x = r"x=(\[\[.*?\]\])"
  patron_extremismo = r"extremismo=([\d\.]+)"
  patron_sol = r"sol=(\[[^\]]+\])"
  patron_total_cost = r"total_cost=([\d\.]+)"
  
  # Buscar y procesar
  x_text = re.search(patron_x, solucion).group(1)
  extremismo_text = re.search(patron_extremismo, solucion).group(1)
  sol_text = re.search(patron_sol, solucion).group(1)
  total_cost_text = re.search(patron_total_cost, solucion).group(1)
  
  x = ast.literal_eval(x_text)
  extremismo = float(extremismo_text)
  sol = ast.literal_eval(sol_text)
  total_cost = float(total_cost_text)  
  
  # Crear tabla formateada con cabeceros
  def crear_tabla_opiniones(matriz):
    if not matriz:
      return "No hay datos disponibles"
    
    num_opiniones = len(matriz)
    
    # Crear cabeceros de columnas
    cabecero = "".ljust(5)  
    for i in range(num_opiniones):
      cabecero += f"Op {i+1}".ljust(6)
    
    tabla = cabecero + "\n"
    tabla += "-" * len(cabecero) + "\n"
    
    # Crear filas de datos
    for i, fila in enumerate(matriz):
      fila_texto = f"Op {i+1}".ljust(7)
      for valor in fila:
        fila_texto += str(valor).ljust(6)
      tabla += fila_texto + "\n"
    
    return tabla
  
  textoX = crear_tabla_opiniones(x)
  
  # resultado = f"Solución encontrada:\n\nValor de la Solución= {extremismo}\nSolución= {str(sol)[1:-1]}\nCosto total= {total_cost}\nCantidad de personas a cambiar de opinión=\n{textoX}\n" 
  
  # ventana_resultado.config(state=tk.NORMAL)
  # ventana_resultado.delete('1.0', tk.END)
  # ventana_resultado.insert(tk.END, resultado)
  # ventana_resultado.config(state=tk.DISABLED)
  
  bold_font = font.Font(ventana_resultado, ventana_resultado.cget("font"))
  bold_font.configure(weight="bold")
  
  # Crear fuente monoespaciada para la tabla
  mono_font = font.Font(ventana_resultado, family="Courier New", size=10)
  
  ventana_resultado.config(state=tk.NORMAL)
  ventana_resultado.delete('1.0', tk.END)
  ventana_resultado.tag_configure("negrita", font=bold_font)
  ventana_resultado.tag_configure("tabla", font=mono_font)
  
  ventana_resultado.insert(tk.END, "SOLUCIÓN ENCONTRADA\n\n", "negrita")
  ventana_resultado.insert(tk.END, f"Valor de la Solución = ", "negrita")
  ventana_resultado.insert(tk.END, f"{extremismo}\n")
  ventana_resultado.insert(tk.END, "Solución = ", "negrita")
  ventana_resultado.insert(tk.END, f"{str(sol)[1:-1]}\n")
  ventana_resultado.insert(tk.END, "Costo total = ", "negrita")
  ventana_resultado.insert(tk.END, f"{total_cost}\n")
  ventana_resultado.insert(tk.END, "Cantidad de personas a cambiar de opinión\n\n", "negrita")
  ventana_resultado.insert(tk.END, f"{textoX}\n", "tabla")
  ventana_resultado.config(state=tk.DISABLED)