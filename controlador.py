from tkinter import filedialog, messagebox
import tkinter as tk
import minizinc
import os
import glob

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
    return resultado
  except Exception as e:
    print(f"Error ejecutando el modelo con Gurobi: {e}")
    return None
  
  
 