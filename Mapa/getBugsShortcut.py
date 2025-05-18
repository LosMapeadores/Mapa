import geopandas as gpd
import pandas as pd
import os

dir = "./datasets"

# Leer el GeoJSON
def Files():
    files = [
        "4815075",
        "4815078",
        "4815079",
        "4815081",
        "4815083",

        "4815084",
        "4815085",
        "4815086",
        "4815087",
        "4815090",

        "4815091",
        "4815096",
        "4815097",
        "4815098",
        "4815099",
        
        "4815425",
        "4815428",
        "4815429",
        "4815440",
        "4815441"
    ]

    return files

def Save_Files(files):
    # Crea la carpeta si no existe
    folder_path = f"{dir}/bugs"
    os.makedirs(folder_path, exist_ok=True)

    # Extraer todos las calles con multidigit
    for file in files:
        gdf = gpd.read_file(f"{dir}/STREETS_NAV/SREETS_NAV_{file}.geojson")
        df = pd.read_csv(f'{dir}/POIs/POI_{file}.csv')
        sts_with_N = df[df['POI_ST_SD'] == "N"]["LINK_ID"]
        bugs = gdf[
            (gdf["MULTIDIGIT"] == "Y") &
            (gdf["link_id"].isin(sts_with_N))
            ]
        if bugs.empty:
            continue
        bugs.to_file(f"{dir}/bugs/BUGS_STREET_{file}.geojson", driver="GeoJSON")
        

files = Files()

Save_Files(files)
