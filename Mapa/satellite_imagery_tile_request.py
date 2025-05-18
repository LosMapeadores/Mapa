import pandas as pd
import requests
import math
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración global (ajusta según necesidades)
TILE_SIZE = 512
TILE_FORMAT = 'png'
OUTPUT_DIR = "./map_tiles"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tus funciones existentes (sin modificaciones)
def lat_lon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    n = 2.0 ** zoom
    x = int((lon_rad - (-math.pi)) / (2 * math.pi) * n)
    y = int((1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2 * n)
    return (x, y)

def download_tile(lat, lon, zoom, api_key):
    """Versión mejorada de get_satellite_tile para integración con CSV"""
    try:
        x, y = lat_lon_to_tile(lat, lon, zoom)
        url = f'https://maps.hereapi.com/v3/base/mc/{zoom}/{x}/{y}/{TILE_FORMAT}?style=satellite.day&size={TILE_SIZE}&apiKey={api_key}'
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = os.path.join(OUTPUT_DIR, f"tile_{zoom}_{x}_{y}.{TILE_FORMAT}")
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        print(f"Error HTTP {response.status_code} para ({lat}, {lon})")
        return False
    except Exception as e:
        print(f"Error procesando ({lat}, {lon}): {str(e)}")
        return False

def process_all_bugs(csv_path, api_key, zoom=16, max_workers=8):
    """Procesa todo el CSV de bugs de manera eficiente"""
    # Leer CSV manteniendo todos los datos
    df = pd.read_csv(csv_path)
    
    # Obtener coordenadas únicas para optimizar descargas
    unique_coords = df[['latitud', 'longitud']].drop_duplicates()
    total = len(unique_coords)
    print(f"🔍 Procesando {total} ubicaciones únicas de {len(df)} bugs reportados")
    
    # Descargar tiles en paralelo
    success = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_tile, row['latitud'], row['longitud'], zoom, api_key): idx
            for idx, row in unique_coords.iterrows()
        }
        
        for i, future in enumerate(as_completed(futures), 1):
            if future.result():
                success += 1
            if i % 10 == 0 or i == total:
                print(f"Progreso: {i}/{total} | Exitosa: {success}")
    
    # Generar reporte final
    print(f"\n✅ Resultado: {success}/{total} tiles descargados")
    print(f"📁 Tiles guardados en: {os.path.abspath(OUTPUT_DIR)}")
    
    # Opcional: Generar archivo con metadatos completos
    generate_metadata_file(df, zoom)

def generate_metadata_file(df, zoom):
    """Crea un CSV con metadatos geográficos extendidos"""
    metadata = []
    for _, row in df.iterrows():
        x, y = lat_lon_to_tile(row['latitud'], row['longitud'], zoom)
        metadata.append({
            'file_code': row['file_code'],
            'link_id': row['link_id'],
            'longitud': row['longitud'],
            'latitud': row['latitud'],
            'urban': row['urban'],
            'func_class': row['func_class'],
            'multidigit': row['multidigit'],
            'tile_x': x,
            'tile_y': y,
            'tile_zoom': zoom
        })
    
    metadata_path = os.path.join(OUTPUT_DIR, "bugs_metadata.csv")
    pd.DataFrame(metadata).to_csv(metadata_path, index=False)
    print(f"📄 Metadatos guardados en: {metadata_path}")

# Ejecución principal
if __name__ == "__main__":
    # Configuración
    CSV_PATH = "./datasets/bug_coords/ALL_BUGS_COORDS.csv"
    API_KEY = open("./APIkey.txt").read().strip()
    
    # Procesar todo
    process_all_bugs(CSV_PATH, API_KEY, zoom=16)