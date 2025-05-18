import geopandas as gpd
import os
import pandas as pd

def get_bug_files():
    """Lista de códigos de archivos de bugs"""
    return [
        "4815081", "4815085", "4815087", "4815090","4815091", 
        "4815096", "4815097", "4815098", "4815099",
    ]

def extract_bug_coordinates():
    # Configuración de directorios
    base_dir = "./datasets"
    bugs_dir = os.path.join(base_dir, "bugs")
    output_dir = os.path.join(base_dir, "bug_coords")
    
    # Asegurar que existe el directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista para almacenar todos los datos
    all_data = []
    
    for file_code in get_bug_files():
        bug_file = f"BUGS_STREET_{file_code}.geojson"
        input_path = os.path.join(bugs_dir, bug_file)
        
        # Verificar si el archivo existe
        if not os.path.exists(input_path):
            print(f"Archivo no encontrado: {bug_file}")
            continue
        
        try:
            # Leer el archivo GeoJSON
            gdf = gpd.read_file(input_path)
            
            # Extraer coordenadas de cada feature
            for _, row in gdf.iterrows():
                geom = row.geometry
                
                # Manejar diferentes tipos de geometría
                if geom.geom_type == 'LineString':
                    coords = list(geom.coords)
                elif geom.geom_type == 'MultiLineString':
                    coords = [point for line in geom.geoms for point in line.coords]
                else:
                    continue
                
                # Agregar datos a la lista
                for lon, lat in coords:
                    all_data.append({
                        'file_code': file_code,
                        'link_id': row['link_id'],
                        'longitud': lon,
                        'latitud': lat,
                        'urban': row.get('URBAN', 'N/A'),
                        'func_class': row.get('FUNC_CLASS', 'N/A'),
                        'multidigit': row.get('MULTIDIGIT', 'N/A')
                    })
            
            print(f"Procesado: {bug_file}")
            
        except Exception as e:
            print(f"Error procesando {bug_file}: {str(e)}")
            continue
    
    # Crear DataFrame con todos los datos
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Guardar archivo consolidado
        consolidated_path = os.path.join(output_dir, "ALL_BUGS_COORDS.csv")
        df.to_csv(consolidated_path, index=False, encoding='utf-8')
        print(f"\nArchivo consolidado creado: {consolidated_path}")
        
        # Guardar archivos individuales por código
        for file_code, group in df.groupby('file_code'):
            individual_path = os.path.join(output_dir, f"BUGS_COORDS_{file_code}.csv")
            group.to_csv(individual_path, index=False, encoding='utf-8')
        
        print(f"Se crearon {len(df['file_code'].unique())} archivos individuales")
    else:
        print("No se encontraron datos para procesar")

if __name__ == "__main__":
    print("Iniciando extracción de coordenadas...")
    extract_bug_coordinates()
    print("Proceso completado")