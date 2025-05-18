import geopandas as gpd

# Leer el GeoJSON
def MultiDigs():
    files = [
        "SREETS_NAV_4815075",
        "SREETS_NAV_4815078",
        "SREETS_NAV_4815079",
        "SREETS_NAV_4815081",
        "SREETS_NAV_4815083",

        "SREETS_NAV_4815084",
        "SREETS_NAV_4815085",
        "SREETS_NAV_4815086",
        "SREETS_NAV_4815087",
        "SREETS_NAV_4815090",

        "SREETS_NAV_4815091",
        "SREETS_NAV_4815096",
        "SREETS_NAV_4815097",
        "SREETS_NAV_4815098",
        "SREETS_NAV_4815099",
        
        "SREETS_NAV_4815425",
        "SREETS_NAV_4815428",
        "SREETS_NAV_4815429",
        "SREETS_NAV_4815440",
        "SREETS_NAV_4815441"
    ]

    return files

def Save_Files(files):
    # Extraer todos las calles con multidigit
    for file in files:
        gdf = gpd.read_file(f"./datasets/STREETS_NAV/{file}.geojson")
        multiDigs = gdf[gdf["MULTIDIGIT"] == "Y"]
        multiDigs.to_file(f"./datasets/multiDigs/multiDigs_{file}.geojson", driver="GeoJSON")

files = MultiDigs()

Save_Files(files)
