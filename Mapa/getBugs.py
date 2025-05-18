import geopandas as gpd
import pandas as pd

dir = "./Mapa/datasets"

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
    # Extraer todos las calles con multidigit
    for file in files:
        gdf = gpd.read_file(f"{dir}/multiDigs/multiDigs_SREETS_NAV_{file}.geojson")
        df = pd.read_csv(f'{dir}/nonCardPOIs/nonCardPOI_POI_{file}.csv')
        sts_with_N = df["LINK_ID"]
        bugs_list = []
        for i in sts_with_N:
            bugs_list.append(gdf[gdf["link_id"] == i])
        bugs = pd.concat(bugs_list)
        bugs.to_file(f"{dir}/bugs/bugs_streets_{file}.geojson", driver="GeoJSON")




files = Files()

Save_Files(files)
