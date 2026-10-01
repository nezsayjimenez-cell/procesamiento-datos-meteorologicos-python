# =====================================================
# IMPORTACIÓN DE LIBRERÍAS
# =====================================================

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg

import numpy as np
import xarray as xr
import geopandas as gpd

from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from pathlib import Path



# =====================================================
# RUTAS
# =====================================================

archivo_nc = "/home/abisai/Tesis_datos/datos_crudos/MMOX_land_enero.nc"

carpeta_salida = Path("/home/abisai/Tesis_datos/figuras/Pruebas")
carpeta_salida.mkdir(parents=True, exist_ok=True)

ruta_curvas = "/home/abisai/Tesis_datos/estaciones/curvas1000.gpkg"
ruta_virtual = "/home/abisai/Tesis_datos/estaciones/virtual100015.gpkg"
ruta_aeropuerto = "/home/abisai/Tesis_datos/estaciones/Aeropuerto.gpkg"
landVStemp = mpimg.imread("/home/abisai/Tesis_datos/figuras/series_temporales/temperatura_enero_2025.png")
landVSwin = mpimg.imread("/home/abisai/Tesis_datos/figuras/series_temporales/viento_enero_2025.png")
landVSPt = mpimg.imread("/home/abisai/Tesis_datos/figuras/series_temporales/precipitacion_enero_2025.png")
leyenda = mpimg.imread("/home/abisai/Tesis_datos/estaciones/Leyendas.jpg")
rosa = mpimg.imread("/home/abisai/Tesis_datos/estaciones/Rosa.png")

# =====================================================
# LECTURA DEL NETCDF
# =====================================================

datos = xr.open_dataset(archivo_nc)
datos = datos.sortby("latitude")

print(datos)

lat = datos["latitude"].values
lon = datos["longitude"].values
time = datos["valid_time"]
# =====================================================
# LECTURA DE VARIABLES
# =====================================================
u = datos["u10"]
v = datos["v10"]
rapidez = np.sqrt(u**2 + v**2)
# =====================================================
t2m = datos['t2m'][:]-273.15
# ===================================================
#Si tp YA está en mm acumulados:
# Si tp estuviera en metros, usar:
tp = datos["tp"].diff("valid_time") * 1000
tp = tp.where(tp >= 0, 0)
# ====================================================
t= datos["ssrd"].diff("valid_time") / 3600
t = t.where(t >= 0, 0)
#======================================================
lons, lats = np.meshgrid(lon, lat)
 

# =====================================================
# LECTURA DE CAPAS VECTORIALES
# =====================================================

curvas = gpd.read_file(ruta_curvas)
virtual = gpd.read_file(ruta_virtual)
aeropuerto = gpd.read_file(ruta_aeropuerto)


# =====================================================
# PALETA DE COLORES
# =====================================================

mis_colores = LinearSegmentedColormap.from_list(
    "mi_paleta_vientos",
    [
    '#13441e',
    '#007a66',
    '#00ffff',
    '#5eff8b',
    '#b6ff33',
    '#ffff00',
    '#ffb700',   
    '#ff5500',
    '#ff0000',
    '#d60050',     
    '#8b008b',
    ]
)

mis_colores1 = LinearSegmentedColormap.from_list(
    "mi_paleta_temperatura",
    [
    '#FF00FF',
    '#7F00FF',
    '#0000FF',
    '#00FFFF',
    '#00A040',
    '#00FF00',
    '#CCFF00',
    '#FFFF00',
    '#FF9900',
    '#FF3300',
    '#CC0000',
    '#660000'
    ]
)
mis_colores2 = LinearSegmentedColormap.from_list(
    "mi_paleta_lluvia",
    [
        "#E0E0E0", 
        "#00E0FF", 
        "#0000FF", 
        "#008A00",
        "#00FF00", 
        "#7CFF00", 
        "#FFFF00",
        "#FF8A00",
        "#FF0000",
        "#6A0096",
        "#FF00FF"
    ]
)

mis_colores3 = LinearSegmentedColormap.from_list(
    "mi_paleta_SSRD",
    [
        '#000000', 
        '#004040', 
        '#2F4F4F', 
        '#008000', 
        '#00FF00', 
        '#AFFF00', 
        '#FFFF00', 
        '#FF7F00', 
        '#FF0000', 
        '#4A0000', 
        '#6A0096', 
        '#FF00FF'
    ]
)



# =====================================================
# CONFIGURACIÓN DE ESCALAS
# =====================================================

niveles_relleno = np.arange(0, 60, 1)
niveles_contorno = np.arange(0, 60, 1)
niveles_etiqueta = np.arange(0, 60, 25)
ticks_colorbar = np.arange(0, 60, 5)

niveles_relleno1 = np.arange(-5, 40.5, .5)
niveles_contorno1 = np.arange(-5, 40.5, .5)
niveles_etiqueta1 = np.arange(-5, 41, 5)
ticks_colorbar1 = np.arange(-5, 41, 5)

niveles_relleno2 = np.arange(0, 31, 0.5)
niveles_contorno2 = np.arange(0, 31, 0.5)
niveles_etiqueta2 = np.arange(0, 31, 5)
ticks_colorbar2 = np.arange(0, 31, 5)

niveles_relleno3 = np.arange(0, 1200 ,10)
niveles_contorno3 = np.arange(0, 1200 ,10)
niveles_etiqueta3 = np.arange(0, 1200 ,120)
ticks_colorbar3 = np.arange(0, 1200 ,120)



# =====================================================
# CONFIGURACIÓN TEMPORAL
# =====================================================

anio = 2025
mes = 1    #recuerda cambiar el mes 
horas = range(23)

# =====================================================
# Función para complementos / accessories
# =====================================================

def graficar_complementos(mapa,ax,curvas,virtual,aeropuerto,es_mapa_sol=False): #empty = vacio 

        if es_mapa_sol:
            color_leyenda = "darkgray"
        else:
            color_leyenda = "black"

        curvas.plot(
            ax=ax,
            color=color_leyenda,
            linewidth=0.4,
            alpha=0.5,
            zorder=4
        )

        virtual.plot(
            ax=ax,
            color=color_leyenda,
            linewidth=0.4,
            alpha=0.5,
            zorder=5
        )

        aeropuerto.plot(
            ax=ax,
            color=color_leyenda,
            linewidth=0.8,
            alpha=1,
            zorder=6
        )

        lat_escala = 16.08
        lon_inicio = -97.80
        lon_fin = -97.32   # aprox. 50 km cerca de 16-17°N

        ax.plot(
            [lon_inicio, lon_fin],
            [lat_escala, lat_escala],
            color=color_leyenda,
            linewidth=4,
            zorder=20
        )

        ax.plot(
            [lon_inicio, lon_inicio],
            [lat_escala - 0.02, lat_escala + 0.02],
            color=color_leyenda,
            linewidth=2,
            zorder=20
        )

        ax.plot(
            [lon_fin, lon_fin],
            [lat_escala - 0.02, lat_escala + 0.02],
            color=color_leyenda,
            linewidth=2,
            zorder=20
        )

        ax.text(
            (lon_inicio + lon_fin) / 2,
            lat_escala + 0.04,
            "50 km",
            ha="center",
            fontsize=10,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
            zorder=21
        )


        return mapa
# =====================================================
# Función para crear el mapa
# =====================================================
def crear_mapa(ax):

            mapa = Basemap(
                projection="cyl",
                resolution="l",
                llcrnrlat=16,
                urcrnrlat=18,
                llcrnrlon=-98,
                urcrnrlon=-95,
                ax=ax,
                fix_aspect=False
            )

            paralelos = np.arange(16, 18.5, 0.5)
            meridianos = np.arange(-98, -95, 0.5)

            mapa.drawparallels(
                paralelos,
                labels=[False, True, False, False],
                size=10,
                linewidth=0.2
            )
            
           
            mapa.drawmeridians(
                meridianos,
                labels=[False, False, False, True],
                size=10,
                linewidth=0.2
            )
            return mapa
# =====================================================
# CICLO DE GENERACIÓN DE FIGURAS
# =====================================================       
for dia in range(1, 2):

    for hora in horas:

        fecha = f"{anio}-{mes:02d}-{dia:02d}T{hora:02d}:00:00"

        try:
            u_campo = u.sel(valid_time=fecha, method="nearest")
            v_campo = v.sel(valid_time=fecha, method="nearest")
            rapidez_campo = rapidez.sel(valid_time=fecha,method="nearest")
            temperatura_campo = t2m.sel(valid_time=fecha, method="nearest")
            precipitacion_campo = tp.sel(valid_time=fecha, method="nearest")
            radiacion_campo = t2m.sel(valid_time=fecha, method="nearest")



        except Exception:
            print(f"Saltando fecha no encontrada: {fecha}")
            continue

        fig = plt.figure(figsize=(32, 16))

        gs = gridspec.GridSpec(
        nrows=4,
        ncols=3,
        figure=fig,
        height_ratios=[1, 1, 1, 1],  #[1, 1, 1, 0.45]
        width_ratios=[0.75, 1, 1],  #[1,1,4.5,0.8 ]
        hspace=0.35, 
        wspace=0.30
        )

        ax_temp = fig.add_subplot(gs[0, 0:1])      # Temperatura y rocío
        ax_prec = fig.add_subplot(gs[1, 0:1])      # Precipitación
        ax_viento = fig.add_subplot(gs[2, 0:1])     # Viento
        ax_temp.axis("off")
        ax_prec.axis("off")
        ax_viento.axis("off")
        ax_mapa_tem = fig.add_subplot(gs[0:2, 1])      # Mapa principal
        ax_mapa_pre = fig.add_subplot(gs[0:2, 2])      # Mapa principal
        ax_mapa_win = fig.add_subplot(gs[2:4, 1])      # Mapa principal
        ax_mapa_sol = fig.add_subplot(gs[2:4, 2])      # Mapa principal
        #ax_leyenda = fig.add_subplot(gs[0:2, 3])     # Simbología
        #ax_leyenda = fig.add_subplot(gs[1:3, 3])
        #ax_rosa = fig.add_subplot(gs[2:3, 3])      # Rosa de viento
        #ax_rosa = fig.add_subplot(gs[0:1, 3]) 

        ax_texto = fig.add_subplot(gs[3,0:1])       # METAR + interpretación


        #ax_leyenda = fig.add_subplot(gs[0:2, 3])     # Simbología(original)
        #ax_leyenda = fig.add_subplot(gs[1:3, 3])
        #ax_rosa = fig.add_subplot(gs[2:3, 3])      # Rosa de viento(original)
        #ax_rosa = fig.add_subplot(gs[0:1, 3]) 

        #ax_texto = fig.add_subplot(gs[3, :])       # METAR + interpretación

        # Apagar ejes que serán solo texto/leyenda
        #ax_leyenda.axis("off")
        ax_texto.axis("off")
        #ax_rosa.axis("off")
        # =====================================================
        # MAPS
        # =====================================================  
        mapa_prec = crear_mapa(ax_mapa_pre)
        mapa_win = crear_mapa(ax_mapa_win)
        mapa_tem = crear_mapa(ax_mapa_tem)
        mapa_sol = crear_mapa(ax_mapa_sol)
    
        # =====================================================
        # RELLENO
        # =====================================================
        cf = mapa_win.contourf(
            lons,
            lats,
            rapidez_campo.values,
            levels=niveles_relleno,
            cmap=mis_colores,
            extend="both"
        )
        
        
        cf1 = mapa_tem.contourf(
            lons,
            lats,
            temperatura_campo.values,
            levels=niveles_relleno1,
            cmap=mis_colores1,
            extend="both"
        )
        
        cf2 = mapa_prec.contourf(
            lons,
            lats,
            precipitacion_campo.values,
            levels=niveles_relleno2,
            cmap=mis_colores2,
            extend="both"
        )

        cf3 = mapa_sol.contourf(
            lons,
            lats,
            radiacion_campo.values,
            levels=niveles_relleno3,
            cmap=mis_colores3,
            extend="both"
        )

        # =====================================================
        # CONTORNOS 
        # =====================================================

        contornos = mapa_win.contour(
            lons,
            lats,
            rapidez_campo.values,
            levels=niveles_contorno,
            colors="black",
            linewidths=0.10,
            alpha=0.30
        )

        plt.clabel(
            contornos,
            levels=niveles_etiqueta,
            fontsize=6,
            inline=True,
            fmt="%d"
        )

        contornos = mapa_tem.contour(
            lons,
            lats,
            temperatura_campo.values,
            levels=niveles_contorno1,
            colors="black",
            linewidths=0.10,
            alpha=0.30
        )

        plt.clabel(
            contornos,
            levels=niveles_etiqueta1,
            fontsize=6,
            inline=True,
            fmt="%d"
        )
        
        contornos = mapa_tem.contour(
            lons,
            lats,
            precipitacion_campo.values,
            levels=niveles_contorno2,
            colors="black",
            linewidths=0.10,
            alpha=0.30
        )

        plt.clabel(
            contornos,
            levels=niveles_etiqueta2,
            fontsize=6,
            inline=True,
            fmt="%d"
        )

        contornos = mapa_tem.contour(
            lons,
            lats,
            radiacion_campo.values,
            levels=niveles_contorno3,
            colors="darkgray",
            linewidths=0.10,
            alpha=0.30
        )

        plt.clabel(
            contornos,
            levels=niveles_etiqueta3,
            fontsize=6,
            inline=True,
            fmt="%d"
        )

        # =====================================================
        # BARBAS DE VIENTO / STREAMLINES
        # =====================================================
        mapa_win.streamplot(
          lons,
          lats,
          u_campo.values,
          v_campo.values,
          color="black",
          density=2,
          linewidth=0.8,
          arrowsize=0.8
        )
        




        r = 2

        mapa_tem.barbs(
            lons[::r, ::r],
            lats[::r, ::r],
            u_campo.values[::r, ::r],
            v_campo.values[::r, ::r],
            length=5,
            linewidth=0.4,
            color="black",
            zorder=3
        )

        mapa_prec.barbs(
            lons[::r, ::r],
            lats[::r, ::r],
            u_campo.values[::r, ::r],
            v_campo.values[::r, ::r],
            length=5,
            linewidth=0.4,
            color="black",
            zorder=3
        )

        mapa_sol.barbs(
            lons[::r, ::r],
            lats[::r, ::r],
            u_campo.values[::r, ::r],
            v_campo.values[::r, ::r],
            length=5,
            linewidth=0.4,
            color="darkgray",
            zorder=3
        )


        # =====================================================
        # Complementos / accessories
        # =====================================================
        graficar_complementos(mapa_win, ax_mapa_win, curvas, virtual, aeropuerto,es_mapa_sol=False)
        graficar_complementos(mapa_tem, ax_mapa_tem, curvas, virtual, aeropuerto, es_mapa_sol=False)
        graficar_complementos(mapa_prec, ax_mapa_pre, curvas, virtual, aeropuerto, es_mapa_sol=False)
        graficar_complementos(mapa_sol, ax_mapa_sol, curvas, virtual, aeropuerto, es_mapa_sol=True)
        # =====================================================
        # COLORBAR
        # =====================================================
     #########################################
     #          win a 2m
     #########################################
        cbar = fig.colorbar(
            cf,
            ax=ax_mapa_win,
            orientation="vertical",
            pad=0.08,
            shrink=0.75,
            ticks=ticks_colorbar
        )

        cbar.ax.set_title(
            "Velocidad \nde viento\n2 m (m/s)",
            fontsize=14,
            fontweight="bold",
            pad=10
        )

        cbar.ax.tick_params(labelsize=14)
     #########################################
     #         Temperatura 2 m  
     #########################################
        cbar = fig.colorbar(
            cf1,
            ax=ax_mapa_tem,
            orientation="vertical",
            pad=0.08,
            shrink=0.75,
            ticks=ticks_colorbar1
        )

        cbar.ax.set_title(
            "Temperatura\n2 m (°C)",
            fontsize=14,
            fontweight="bold",
            pad=10
        )

        cbar.ax.tick_params(labelsize=14)
     #########################################
     #         precipitación 2 m  
     #########################################
        cbar = fig.colorbar(
            cf2,
            ax=ax_mapa_pre,
            orientation="vertical",
            pad=0.08,
            shrink=0.75,
            ticks=ticks_colorbar2
        )

        cbar.ax.set_title(
            "Precipitación\n2 m (mm)",
            fontsize=14,
            fontweight="bold",
            pad=10
        )

        cbar.ax.tick_params(labelsize=14)
     #########################################
     #         SSRD / radiación incidente  
     #########################################
        cbar = fig.colorbar(
            cf3,
            ax=ax_mapa_sol,
            orientation="vertical",
            pad=0.08,
            shrink=0.75,
            ticks=ticks_colorbar3
        )

        cbar.ax.set_title(
            "Radiación\n2 m (W/m²)",
            fontsize=14,
            fontweight="bold",
            pad=10
        )

        cbar.ax.tick_params(labelsize=14)
        # =====================================================
        # TÍTULO
        # =====================================================

        fecha_graf = np.datetime_as_string(
            rapidez_campo.valid_time.values,
            unit="h"
        )
        

        # =====================================================
        # EJEMPLO DE CONTENIDO
        # =====================================================
        ax_temp.imshow(

            landVStemp,
            #extent=[0.00,1,0,1],#0,4,0,8
            aspect="auto",
            #zorder=1
        )

        ax_viento.imshow(

            landVSwin,
            #extent=[0.00,1,0,1],#0,4,0,8
            aspect="auto",
            #zorder=1
        )

        ax_prec.imshow(

            landVSPt,
            #extent=[0.00,1,0,1],#0,4,0,8
            aspect="auto",
            #zorder=1
        )
        
        ax_mapa_win.set_title(
            f"ERA5-Land Dirección del viento a\n 10 m horaria\n{fecha_graf} UTC, de (2000-2026) " ,
            fontsize=18,
            fontweight="bold"
        )

        ax_mapa_sol.set_title(
            f"ERA5-Land Radiación incidente horaria\n{fecha_graf} UTC, de (2000-2026) " ,
            fontsize=18,
            fontweight="bold"
        )

        ax_mapa_pre.set_title(
            f"ERA5-Land Precipitación horaria\n{fecha_graf} UTC, de (2000-2026) " ,
            fontsize=18,
            fontweight="bold"
        )

        ax_mapa_tem.set_title(
            f"ERA5-Land Temperatura horaria\n{fecha_graf} UTC, de (2000-2026) " ,
            fontsize=18,
            fontweight="bold"
        )



        ####################################################
        #--------------Leyenda----------------
        ####################################################
        
        #ax_leyenda.imshow(

            #leyenda,
            #extent=[0.00,1,0,1],#0,4,0,8
            #aspect="auto",
            #zorder=1
        #)
        #ax_leyenda.set_xlim(0, 1)
        #ax_leyenda.set_ylim(0, 1)
        ###################################################
        #-------------Rosa de viento----------------
        ###################################################
        #ax_rosa.imshow(

        #    rosa,
        #    extent=[0.00,0.8,0,1.2],#0,4,0,8
        #    aspect="auto",
        #    zorder=1
        #)
        #ax_rosa.set_xlim(0, 1)
        #ax_rosa.set_ylim(0, 1)



        ax_texto.text(
            0.01, 0.5,
            "METAR MMOX: aquí va el METAR original + interpretación operacional.",
            va="center",
            fontsize=11,
            bbox=dict(facecolor="white", edgecolor="black", alpha=0.9)
        )
        # =====================================================
        # GUARDADO
        # =====================================================

        nombre = carpeta_salida / f"TODO_{anio}_{mes:02d}_{dia:02d}_{hora:02d}UTC_pruebas01.png"

        fig.savefig(
            nombre,
            dpi=180,
            facecolor="white"
        )

        
        plt.close(fig)

        print(f"Guardado: {nombre.name}")