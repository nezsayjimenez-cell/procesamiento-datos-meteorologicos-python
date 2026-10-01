import os
import re 
import urllib.request
import urllib.error  # <- Importación necesaria para atrapar el error 404
import pandas as pd
from datetime import datetime

# =====================================================================
# CONFIGURACIÓN GENERAL DEL PERIODO DE ESTUDIO
# =====================================================================
CARPETA_SALIDA = "/home/abisai/Tesis_datos/estaciones/CDMX/diarios/estaciones_descargadas"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# URL Base del SMN (Cambiamos el final para que sea dinámico)
URL_BASE = "https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/df/dia{}.txt"

# Variable para limpiar numéricamente
variables_clima = ['Precipitacion', 'Evaporacion', 'Tmax', 'Tmin']
# ----- Variable para almacenar los datos resumidos de todas las estaciones -----
datos_resumen_global = []

# =====================================================================
# BUCLE PRINCIPAL DE DESCARGA (Estaciones de la 1 a la 100 o 400)
# =====================================================================
print("Iniciando descarga y procesamiento de estaciones...\n")

for i in range(1, 100):
    # Convertimos el número i a un texto de 5 dígitos (Ej: 1 -> '00001', 15 -> '00015')
    numero_estacion = i + 9000
    id_estacion = str(numero_estacion).zfill(5) 
    url_estacion = URL_BASE.format(id_estacion)
    
    lat_estacion = None
    lon_estacion = None
    alt_estacion = None
    lineas_a_saltar = 0
    palabra_clave = "(mm)"
    
    try:
        # Intentamos abrir la URL para verificar si existe
        with urllib.request.urlopen(url_estacion) as respuesta_web:
            # Intentamos obtener los datos del servidor de CONAGUA
            lineas = [linea.decode('utf-8', errors='ignore') for linea in respuesta_web.readlines()]
            
            # 1. Buscamos los metadatos en las primeras 25 líneas
            for linea in lineas[:25]:
                if "Latitud" in linea or "LATITUD" in linea:
                    numeros = re.findall(r'[-+]?\d*\.\d+|\d+', linea)
                    if numeros: lat_estacion = float(numeros[0])
                elif "Longitud" in linea or "LONGITUD" in linea:
                    numeros = re.findall(r'[-+]?\d*\.\d+|\d+', linea)
                    if numeros: lon_estacion = float(numeros[0])
                elif "Altitud" in linea or "ALTITUD" in linea or "Elevacion" in linea:
                    numeros = re.findall(r'[-+]?\d*\.\d+|\d+', linea)
                    if numeros: alt_estacion = float(numeros[0])
            
            # 2. Buscamos en qué número de línea está la palabra clave "(mm)"
            for idx, linea in enumerate(lineas):
                if palabra_clave in linea:
                    lineas_a_saltar = idx
                    break

            print(f" Descargando Estación Clave: {id_estacion}...")
    
            # -----------------------------------------------------------------
            # LECTURA DEL ARCHIVO TXT
            # -----------------------------------------------------------------
            mis_columnas = ['Fecha', 'Precipitacion', 'Evaporacion', 'Tmax', 'Tmin']            

            df_temp = pd.read_csv(
                url_estacion, 
                skiprows=lineas_a_saltar + 1,  # Sumamos 1 para saltarnos los guiones debajo de (mm)
                names=mis_columnas, 
                sep=r'\s+', 
                engine='python'
            )

            # --- 4. CONVERSIÓN DE FECHAS ---
            df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format='mixed', errors='coerce')
            df_temp = df_temp.dropna(subset=['Fecha'])
            df_temp = df_temp[(df_temp['Fecha'].dt.month != 2) | (df_temp['Fecha'].dt.day != 29)]
            df_temp.set_index('Fecha', inplace=True)
            
            # --- 5. INYECCIÓN DE METADATOS ---
            df_temp['Estacion'] = id_estacion
            df_temp['Latitud'] = lat_estacion
            df_temp['Longitud'] = lon_estacion
            df_temp['Altitud'] = alt_estacion 

            # ---------------------------------------------------------------------
            # FORZAR LIMPIEZA NUMÉRICA CON -999.99 (Cambio a negativo para que tu evaluación funcione)
            # ---------------------------------------------------------------------
            for var in variables_clima:
                if var in df_temp.columns:
                    df_temp[var] = pd.to_numeric(df_temp[var], errors='coerce')
                    df_temp[var] = df_temp[var].fillna(-999.99)

            # =====================================================================
            # 3.3 EVALUACIÓN DE VIABILIDAD POR VARIABLE (0 = Inútil, 1 = Útil)
            # =====================================================================
            meses_utiles_por_var = {
                'Precipitacion': 0,
                'Evaporacion': 0,
                'Tmax': 0,
                'Tmin': 0
            }
            
            total_meses_evaluados = 0

            # Agrupamos los datos mes por mes utilizando el índice de fechas
            for mes, df_mes in df_temp.groupby(df_temp.index.to_period('M')):
                total_meses_evaluados += 1
                
                # Evaluamos cada variable de forma independiente en este mes
                for var in variables_clima:
                    if var in df_mes.columns:
                        # Contamos cuántos días de este mes tienen el error -999.99 en esta variable
                        dias_con_error = (df_mes[var] == -999.99).sum()
                        
                        # CONDICIÓN: Si tiene 25 o menos días con error, el mes es ÚTIL para esta variable
                        if dias_con_error <= 25:
                            meses_utiles_por_var[var] += 1
            
            # =====================================================================
            # REGISTRO EN EL RESUMEN GLOBAL
            # =====================================================================
            datos_resumen_global.append({
                "Estacion": id_estacion,
                "Latitud": lat_estacion,
                "Longitud": lon_estacion,
                "Altitud": alt_estacion,
                "Total_Meses_Periodo": total_meses_evaluados,
                "Meses_Utiles_Precipitacion": meses_utiles_por_var['Precipitacion'],
                "Meses_Utiles_Evaporacion": meses_utiles_por_var['Evaporacion'],
                "Meses_Utiles_Tmax": meses_utiles_por_var['Tmax'],
                "Meses_Utiles_Tmin": meses_utiles_por_var['Tmin']
            })

            # --- 6. GUARDAR EL ARCHIVO INDIVIDUAL .CSV ---
            df_final_guardar = df_temp.reset_index().rename(columns={'index': 'Fecha'})
            ruta_csv = os.path.join(CARPETA_SALIDA, f"estacion_{id_estacion}.csv")
            df_final_guardar.to_csv(ruta_csv, index=False)
            print(f"   💾 Guardado con éxito en: {ruta_csv}\n")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"⚠️ Estación Clave {id_estacion} no existe en el servidor. Saltando...")
        else:
            print(f"❌ Error HTTP {e.code} en estación {id_estacion}")
        continue
    except Exception as e:
        print(f"❌ Error procesando la estación {id_estacion}: {e}")
        continue

# =====================================================================
# EXPORTACIÓN DEL INFORME RESUMEN GLOBAL (Fuera de todos los bucles)
# =====================================================================
print("\nGenerando archivo de resumen global de viabilidad...")
if datos_resumen_global:
    df_resumen_final = pd.DataFrame(datos_resumen_global)
    ruta_resumen_csv = os.path.join(CARPETA_SALIDA, "resumen_viabilidad_por_variable.csv")
    df_resumen_final.to_csv(ruta_resumen_csv, index=False)
    print(f"➔ ¡Resumen guardado exitosamente en: {ruta_resumen_csv}!")
else:
    print("⚠️ No se colectaron datos para el resumen global.")

print("\n¡Todo el proceso de descarga, limpieza y diagnóstico ha finalizado con éxito!")
