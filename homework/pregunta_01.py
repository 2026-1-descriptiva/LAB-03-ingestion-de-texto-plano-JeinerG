"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", "r") as archivo:
        lineas = archivo.readlines()

    # Omitimos las primeras 4 lineas (encabezados)
    datos = lineas[4:]
    
    clusters = []
    cluster_actual = None
    
    for linea in datos:
        # Buscamos lineas que inicien con numero de cluster
        coincidencia = re.match(r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s+%\s+(.*)", linea)
        
        if coincidencia:
            if cluster_actual:
                clusters.append(cluster_actual)
            
            id_cluster = int(coincidencia.group(1))
            numero_palabras = int(coincidencia.group(2))
            porcentaje_valor = float(coincidencia.group(3).replace(",", "."))
            palabras_clave = coincidencia.group(4).strip()
            
            cluster_actual = {
                "cluster": id_cluster,
                "cantidad_de_palabras_clave": numero_palabras,
                "porcentaje_de_palabras_clave": porcentaje_valor,
                "principales_palabras_clave": palabras_clave
            }
        elif not linea.strip():
            continue
        else:
            if cluster_actual:
                texto_adicional = linea.strip()
                cluster_actual["principales_palabras_clave"] += " " + texto_adicional

    if cluster_actual:
        clusters.append(cluster_actual)

    # Limpieza final de las palabras clave
    for registro in clusters:
        if registro["principales_palabras_clave"].endswith("."):
            registro["principales_palabras_clave"] = registro["principales_palabras_clave"][:-1]
        
        # Unificar espacios multiples
        registro["principales_palabras_clave"] = " ".join(registro["principales_palabras_clave"].split())

    # Crear el DataFrame
    df = pd.DataFrame(clusters)
    
    return df