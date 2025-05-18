import pandas as pd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import os

def plot_network_map():
    """
    Versión mejorada que busca el archivo automáticamente
    """
    # Configuración de directorios
    base_dir = "./datasets"
    
    # Posibles ubicaciones del archivo (ajusta según tu estructura real)
    possible_paths = [
        os.path.join(base_dir, "all_coords", "ALL_STREETS_COORDS.csv"),
    ]
    
    # Buscar el archivo existente
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print("Error: No se encontró el archivo CSV. Busqué en:")
        for path in possible_paths:
            print(f"- {path}")
        return
    
    print(f"Leyendo archivo: {csv_path}")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(csv_path)
        
        # Verificar columnas necesarias
        required_cols = ['file_code', 'link_id', 'longitud', 'latitud']
        if not all(col in df.columns for col in required_cols):
            print("Error: El CSV no tiene las columnas requeridas")
            print(f"Columnas encontradas: {list(df.columns)}")
            print(f"Columnas requeridas: {required_cols}")
            return
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(15, 12))
        
        # Procesar cada grupo de calles
        for (file_code, link_id), group in df.groupby(['file_code', 'link_id']):
            if len(group) < 2:
                continue  # Necesitamos al menos 2 puntos para una línea
            
            # Crear y dibujar LineString
            line = LineString(group[['longitud', 'latitud']].values)
            x, y = line.xy
            ax.plot(x, y, 'b-', linewidth=0.5, alpha=0.7)
            
            # Dibujar nodos
            for _, row in group.iterrows():
                ax.plot(row['longitud'], row['latitud'], 'ro', markersize=3, alpha=0.7)
        
        # Configuración del mapa
        ax.set_title('Mapa de Red de Calles con Nodos', fontsize=16)
        ax.set_xlabel('Longitud', fontsize=12)
        ax.set_ylabel('Latitud', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal', adjustable='datalim')
        
        # Guardar y mostrar
        output_image = os.path.join(base_dir, "network_map.png")
        plt.savefig(output_image, dpi=300, bbox_inches='tight')
        print(f"Mapa guardado como: {output_image}")
        plt.show()
        
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")

if __name__ == "__main__":
    print("Iniciando generación de mapa...")
    plot_network_map()
    print("Proceso completado")