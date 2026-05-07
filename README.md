# 🗺️ Smart POI Fixer

A set of tools to identify, extract, and visualize bugs in street networks from geospatial GeoJSON data. The project cross-references street navigation data with Points of Interest (POIs) to detect problematic road segments, generates network maps, and downloads satellite imagery of affected areas.

---

## 📁 Project Structure

```
.
├── datasets/
│   ├── STREETS_NAV/          # Street GeoJSON files per tile code
│   ├── POIs/                 # POI CSV files per tile code
│   ├── bugs/                 # Generated GeoJSON files with buggy streets
│   ├── all_coords/           # CSVs with coordinates of all streets
│   └── bug_coords/           # CSVs with coordinates of buggy streets
├── map_tiles/
│   └── bugs_metadata.csv     # Metadata of downloaded satellite tiles
├── Mapa/
│   ├── getCoordBugs.py       # Extracts coordinates from buggy streets
│   ├── nodeMapping.py        # Generates a visual map of the street network
│   └── satellite_imagery_tile_request.py  # Downloads satellite tiles via HERE Maps API
├── Identify_case_1_bugs/
│   └── index.html            # Interactive bug visualization using Leaflet
├── getAllCoords.py            # Extracts coordinates from all streets
├── APIkey.txt                # HERE Maps API key (do not commit)
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

- Python 3.8+
- A valid [HERE Maps API](https://developer.here.com/) key

### Install dependencies

```bash
pip install geopandas pandas shapely matplotlib requests
```

---

## 🚀 Usage

### 1. Extract coordinates from all streets

```bash
python getAllCoords.py
```

Reads `SREETS_NAV_<code>.geojson` files from `datasets/STREETS_NAV/` and produces:
- `datasets/all_coords/ALL_STREETS_COORDS.csv` — consolidated file
- `datasets/all_coords/STREETS_COORDS_<code>.csv` — one file per tile

**Output columns:** `file_code`, `link_id`, `longitud`, `latitud`, `urban`, `func_class`, `paved`, `direction`

---

### 2. Detect and extract buggy streets

```bash
python Mapa/getCoordBugs.py
```

Cross-references street GeoJSONs with POI CSVs to flag segments where:
- `MULTIDIGIT == "Y"` (multidigitized street)
- The `link_id` appears in POIs with `POI_ST_SD == "N"`

Results are saved as GeoJSON files in `datasets/bugs/BUGS_STREET_<code>.geojson`.

---

### 3. Generate the street network map

```bash
python Mapa/nodeMapping.py
```

Loads `datasets/all_coords/ALL_STREETS_COORDS.csv` and renders a full network map with nodes, saved as `datasets/street_network_map.png`.

---

### 4. Download satellite imagery for bugs

Requires a HERE Maps API key stored in `APIkey.txt`.

```bash
python Mapa/satellite_imagery_tile_request.py
```

Downloads satellite tiles (zoom 16, 512px) for each unique coordinate in `datasets/bug_coords/ALL_BUGS_COORDS.csv` using parallel downloads via `ThreadPoolExecutor`. Tiles are saved to `map_tiles/` along with a `bugs_metadata.csv` file.

---

### 5. Interactive browser visualization

Open `Identify_case_1_bugs/index.html` via a local server to explore bugs over a Leaflet map with OpenStreetMap tiles.

```bash
# Example with Python
cd Identify_case_1_bugs
python -m http.server 8080
# Then open http://localhost:8080
```

> Make sure to place the relevant `SREETS_NAV_<code>.geojson` file in the same folder as `index.html`.

---

## 📊 Expected Input Files

| File | Location | Description |
|---|---|---|
| `SREETS_NAV_<code>.geojson` | `datasets/STREETS_NAV/` | Street network per tile |
| `POI_<code>.csv` | `datasets/POIs/` | POIs with `POI_ST_SD` and `LINK_ID` columns |
| `APIkey.txt` | project root | HERE Maps API key (do not commit) |

### Available tile codes

```
4815075, 4815078, 4815079, 4815081, 4815083,
4815084, 4815085, 4815086, 4815087, 4815090,
4815091, 4815096, 4815097, 4815098, 4815099,
4815425, 4815428, 4815429, 4815440, 4815441
```

---

## 🔒 Security

`APIkey.txt` is listed in `.gitignore` and **must never be committed to the repository**. Never hardcode your API key in source files.

---

## 👥 Authors

Developed collaboratively as part of a geospatial data quality analysis project for road networks.
