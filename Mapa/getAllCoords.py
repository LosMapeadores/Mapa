import geopandas as gpd
import os
import pandas as pd

def get_files():
    """Lista de códigos de archivos"""
    return [
        "4815075","4815078","4815079","4815081","4815083",
        "4815084","4815085","4815086","4815087","4815090",
        "4815091","4815096","4815097","4815098","4815099",
        "4815425","4815428","4815429","4815440","4815441"
    ]

def extract_all_coordinates():
    # Configuración de directorios
    base_dir = "./datasets"
    streets_dir = os.path.join(base_dir, "STREETS_NAV")  # Cambiado a directorio de calles
    output_dir = os.path.join(base_dir, "all_coords")    # Nuevo directorio para salida
    
    # Asegurar que existe el directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista para almacenar todos los datos
    all_data = []
    
    for file_code in get_files():
        street_file = f"SREETS_NAV_{file_code}.geojson"  # Cambiado a archivos de calles
        input_path = os.path.join(streets_dir, street_file)
        
        # Verificar si el archivo existe
        if not os.path.exists(input_path):
            print(f"Archivo no encontrado: {street_file}")
            continue
        
        try:
            # Leer el archivo GeoJSON
            gdf = gpd.read_file(input_path)
            
            # Extraer coordenadas de cada feature (todas las calles)
            for _, row in gdf.iterrows():
                geom = row.geometry
                
                # Manejar diferentes tipos de geometría
                if geom.geom_type == 'LineString':
                    coords = list(geom.coords)
                elif geom.geom_type == 'MultiLineString':
                    coords = [point for line in geom.geoms for point in line.coords]
                else:
                    continue
                
                # Agregar datos a la lista (con todos los metadatos disponibles)
                for lon, lat in coords:
                    all_data.append({
                        'file_code': file_code,
                        'link_id': row['link_id'],
                        'longitud': lon,
                        'latitud': lat,
                        'urban': row.get('URBAN', 'N/A'),
                        'func_class': row.get('FUNC_CLASS', 'N/A'),
                        'paved': row.get('PAVED', 'N/A'),
                        'direction': row.get('DIR_TRAVEL', 'N/A')
                        # Añade más propiedades si las necesitas
                    })
            
            print(f"Procesado: {street_file}")
            
        except Exception as e:
            print(f"Error procesando {street_file}: {str(e)}")
            continue
    
    # Crear DataFrame con todos los datos
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Guardar archivo consolidado
        consolidated_path = os.path.join(output_dir, "ALL_STREETS_COORDS.csv")
        df.to_csv(consolidated_path, index=False, encoding='utf-8')
        print(f"\nArchivo consolidado creado: {consolidated_path}")
        
        # Opcional: Guardar archivos individuales por código
        for file_code, group in df.groupby('file_code'):
            individual_path = os.path.join(output_dir, f"STREETS_COORDS_{file_code}.csv")
            group.to_csv(individual_path, index=False, encoding='utf-8')
        
        print(f"Se crearon {len(df['file_code'].unique())} archivos individuales")
    else:
        print("No se encontraron datos para procesar")

if __name__ == "__main__":
    print("Iniciando extracción de todas las coordenadas...")
    extract_all_coordinates()
    print("Proceso completado")