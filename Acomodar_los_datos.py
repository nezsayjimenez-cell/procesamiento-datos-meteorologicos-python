import pandas as pd
from datetime import datetime
import os

# =====================================================================
# 1. CONFIGURACIÓN DE RUTAS DE TRABAJO y RUTAS (Modificable)
# =====================================================================
# Define aquí el periodo exacto que deseas recortar y armar para tu tesis
ANIO_INICIO = 1970
ANIO_FIN    = 2010

# Fabricamos el Calendario Maestro diario (desde el 1 de enero hasta el 31 de diciembre)
fecha_desde = f"{ANIO_INICIO}-01-01"
fecha_hasta = f"{ANIO_FIN}-12-31"
calendario_maestro = pd.date_range(start=fecha_desde, end=fecha_hasta, freq='D')

CARPETA_ORIGEN = "/home/abisai/Tesis_datos/estaciones/CDMX/diarios/estaciones_descargadas"
CARPETA_REPORTES = "/home/abisai/Tesis_datos/estaciones/CDMX/diarios/reportes_anuales"

os.makedirs(CARPETA_REPORTES, exist_ok=True)

# =====================================================================
# 2. DECLARACIÓN DE LOS CONTENEDORES GLOBALES
# =====================================================================
embudo_precipitacion = []
embudo_evaporacion   = []
embudo_tmax          = []
embudo_tmin          = []

# =====================================================================
# 3. LECTURA Y PROCESAMIENTO ARCHIVO POR ARCHIVO (Del 1 al 400)
# =====================================================================
for i in range(1, 401):
    numero_estacion = i + 9000
    id_estacion = str(numero_estacion).zfill(5)
    nombre_archivo = f"estacion_{id_estacion}.csv"
    ruta_completa = os.path.join(CARPETA_ORIGEN, nombre_archivo)
    
    if os.path.exists(ruta_completa):
        print(f"Leyendo datos locales de la estación: {id_estacion}")
        df = pd.read_csv(ruta_completa)
        
        # =====================================================================
        # 4. EXTRACCIÓN PREVÍA DE METADATOS FIJOS
        # =====================================================================
        # Guardamos los metadatos reales del primer renglón antes de alterar la tabla
        lat_estacion = df['Latitud'].iloc[0]
        lon_estacion = df['Longitud'].iloc[0]
        alt_estacion = df['Altitud'].iloc[0]
        
        # =====================================================================
        # 5. SINCRONIZACIÓN CON EL CALENDARIO MAESTRO (Corte e inyección de 999.99)
        # =====================================================================
        # A) Pasamos la Fecha a formato de tiempo y la ponemos como Índice (molde)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df.set_index('Fecha', inplace=True)
        
        # B) LA MAGIA DEL REINDEX: Aplica el corte temporal exacto (ANIO_INICIO a ANIO_FIN)
        # y si faltan días o años completos, inventa la fila y le mete 999.99 a las variables.
        df_sincronizado = df.reindex(calendario_maestro, fill_value=999.99)
        
        # C) Regresamos la Fecha a columna y reconstruimos las casillas de Año y Día
        df_sincronizado.index.name = 'Fecha'
        df_sincronizado = df_sincronizado.reset_index()
        
        df_sincronizado['Anio'] = df_sincronizado['Fecha'].dt.year
        df_sincronizado['Dia_Del_Anio'] = df_sincronizado['Fecha'].dt.dayofyear
        
        # D) Rellenamos los metadatos fijos en las filas nuevas que el programa acaba de inventar
        df_sincronizado['Estacion'] = id_estacion
        df_sincronizado['Latitud']  = lat_estacion
        df_sincronizado['Longitud'] = lon_estacion
        df_sincronizado['Altitud']  = alt_estacion

        # =====================================================================
        # 6. SEPARACIÓN Y AGRUPACIÓN POR AÑO
        # =====================================================================
        for anio_actual, df_anio in df_sincronizado.groupby("Anio"):
            renglon_base = {
                "Anio": anio_actual,
                "Estacion": id_estacion,
                "Latitud": lat_estacion,
                "Longitud": lon_estacion,
                "Altitud": alt_estacion
            }
            
            fila_precipitacion = renglon_base.copy()
            fila_evaporacion   = renglon_base.copy()
            fila_tmax          = renglon_base.copy()
            fila_tmin          = renglon_base.copy()
        
            # =====================================================================
            # 7. LLENADO HORIZONTAL DÍA POR DÍA
            # =====================================================================
            for idx_fila, fila_dia in df_anio.iterrows():
                num_dia = int(fila_dia['Dia_Del_Anio'])
                nombre_columna = f"Dia_{num_dia}"
                
                fila_precipitacion[nombre_columna] = fila_dia['Precipitacion']
                fila_evaporacion[nombre_columna]   = fila_dia['Evaporacion']
                fila_tmax[nombre_columna]          = fila_dia['Tmax']
                fila_tmin[nombre_columna]          = fila_dia['Tmin']

            # ⬅️ CORREGIDO: Estos append van AL LADO del bucle for de los días, no adentro.
            # Se ejecutan una sola vez cuando el año terminó de llenarse.
            embudo_precipitacion.append(fila_precipitacion)
            embudo_evaporacion.append(fila_evaporacion)
            embudo_tmax.append(fila_tmax)
            embudo_tmin.append(fila_tmin)

# =====================================================================
# 9. EXPORTACIÓN DE MATRICES FINALES HORIZONTALES (Fuera de los bucles)
# =====================================================================
print("\nGenerando matrices consolidadas horizontales finales...")

# 1. Definimos a la fuerza el orden exacto de las columnas que queremos en el CSV
columnas_metadatos = ["Anio", "Estacion", "Latitud", "Longitud", "Altitud"]
columnas_dias = [f"Dia_{d}" for d in range(1, 366)]  # Genera del Dia_1 al Dia_366 en orden secuencial
orden_columnas_perfecto = columnas_metadatos + columnas_dias

embudos_finales = {
    "embudo_precipitacion": (embudo_precipitacion, "matriz_precipitacion_horizontal.csv"),
    "embudo_evaporacion":   (embudo_evaporacion,   "matriz_evaporacion_horizontal.csv"),
    "embudo_tmax":          (embudo_tmax,          "matriz_tmax_horizontal.csv"),
    "embudo_tmin":          (embudo_tmin,          "matriz_tmin_horizontal.csv")
}

for nombre_embudo, (lista_datos, nombre_csv) in embudos_finales.items():
    if lista_datos:
        # Convertimos la lista de filas en una tabla estructurada
        df_matriz = pd.DataFrame(lista_datos)
        
        # 2. Reindexamos las columnas para forzar el orden secuencial estricto (1 al 366)
        # Si un año común no tiene Dia_366, Pandas creará la columna y la llenará con NaN de forma limpia.
        df_matriz = df_matriz.reindex(columns=orden_columnas_perfecto)
        
        # 3. ORDENAMIENTO JERÁRQUICO: Primero por Año, luego por Estación
        df_matriz.sort_values(by=["Anio", "Estacion"], inplace=True)
        
        # 4. Guardamos la matriz horizontal en un archivo .csv limpio
        ruta_salida_csv = os.path.join(CARPETA_REPORTES, nombre_csv)
        df_matriz.to_csv(ruta_salida_csv, index=False)
        print(f"➔ ¡{nombre_embudo.upper()} exportado con éxito en: {ruta_salida_csv}!")
    else:
        print(f"⚠️ El {nombre_embudo} está vacío. No se generó el archivo.")

print("\n¡Todo el proceso de reestructuración y transposición ha finalizado con éxito!")




