import pandas as pd
from shapely.geometry import Point, LineString, MultiLineString
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.collections import LineCollection

def plot_network_map():
    """
    Versión optimizada para manejar grandes conjuntos de datos de calles
    """
    # Configuración de directorios
    base_dir = "./datasets"
    csv_path = os.path.join(base_dir, "all_coords", "ALL_STREETS_COORDS.csv")
    output_image = os.path.join(base_dir, "street_network_map.png")
    
    # Verificar existencia del archivo
    if not os.path.exists(csv_path):
        print(f"Error: No se encontró el archivo CSV en {csv_path}")
        print("Por favor verifica la ruta y la existencia del archivo")
        return
    
    try:
        # Leer el archivo CSV con chunks si es muy grande
        df = pd.read_csv(csv_path)
        
        # Verificar columnas necesarias
        required_cols = {'file_code', 'link_id', 'longitud', 'latitud'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            print(f"Error: Faltan columnas requeridas: {missing}")
            print(f"Columnas disponibles: {list(df.columns)}")
            return
        
        print(f"Procesando {len(df)} puntos de coordenadas...")
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(20, 16))
        
        # Optimización: Usar LineCollection para mejor rendimiento
        lines = []
        coords = []
        
        # Procesar cada segmento de calle
        for (file_code, link_id), group in df.groupby(['file_code', 'link_id']):
            if len(group) >= 2:  # Necesitamos al menos 2 puntos para una línea
                segment = group[['longitud', 'latitud']].values
                lines.append(segment)
                coords.extend(segment)
        
        # Dibujar todas las líneas a la vez (más eficiente)
        lc = LineCollection(lines, colors='blue', linewidths=0.6, alpha=0.7)
        ax.add_collection(lc)
        
        # Dibujar nodos (optimizado para muchos puntos)
        if coords:
            coords_array = np.array(coords)
            ax.scatter(
                coords_array[:, 0], coords_array[:, 1],
                color='red', s=3, alpha=0.5, marker='o'
            )
        
        # Configuración del mapa
        ax.set_title('Mapa Completo de Red de Calles con Nodos', fontsize=18)
        ax.set_xlabel('Longitud', fontsize=14)
        ax.set_ylabel('Latitud', fontsize=14)
        ax.grid(True, alpha=0.2)
        
        # Ajustar los límites del mapa automáticamente
        ax.autoscale()
        ax.set_aspect('equal', adjustable='datalim')
        
        # Guardar y mostrar
        plt.savefig(output_image, dpi=300, bbox_inches='tight')
        print(f"\n✅ Mapa guardado exitosamente en: {output_image}")
        plt.show()
        
    except Exception as e:
        print(f"\n❌ Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    print("Iniciando generación de mapa de red de calles...")
    plot_network_map()
    print("Proceso completado")