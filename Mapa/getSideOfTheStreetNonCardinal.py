import pandas as pd

dir = "./Mapa/datasets"

def NonCard():
    files = [
        "POI_4815075",
        "POI_4815078",
        "POI_4815079",
        "POI_4815081",
        "POI_4815083",

        "POI_4815084",
        "POI_4815085",
        "POI_4815086",
        "POI_4815087",
        "POI_4815090",

        "POI_4815091",
        "POI_4815096",
        "POI_4815097",
        "POI_4815098",
        "POI_4815099",
        
        "POI_4815425",
        "POI_4815428",
        "POI_4815429",
        "POI_4815440",
        "POI_4815441"
    ]

    return files

def Save_Files(files):
    # Extraer todos las calles con multidigit
    for file in files:
        df = pd.read_csv(f'{dir}/POIs/{file}.csv')
        NonCardinalSide = df[df['POI_ST_SD'] == "N"]
        NonCardinalSide.to_csv(f'{dir}/nonCardPOIs/nonCardPOI_{file}.csv', index=False)

files = NonCard()

Save_Files(files)
