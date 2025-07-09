import os
import geopandas as gpd
from owslib.wfs import WebFeatureService

# Pasta onde os arquivos serão salvos
PASTA_SAIDA = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

os.makedirs(PASTA_SAIDA, exist_ok=True)

# Camadas que serão baixadas
camadas = [
    "GeoJundiai:LC_417-2004_SistProtSerradoJapi",
    "GeoJundiai:L_8683-2016_m03_rem-veg-nat",
    "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Cerrado",
    "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Mata_Atlantica",
    "GeoJundiai:L_8683-2016_m13_parques-municipais"
]

# URL base do GeoServer
url_wfs = "https://geo.jundiai.sp.gov.br/geoserver/ows?service=WFS&acceptversions=2.0.0&request=GetCapabilities"
wfs = WebFeatureService(url=url_wfs, version="2.0.0")

# Função para salvar camada como GeoJSON
def salvar_camada(layer_name):
    print(f"Baixando camada: {layer_name}")
    response = wfs.getfeature(
        typename=layer_name,
        outputFormat="application/json",
        srsname="EPSG:31983"
    )
    gdf = gpd.read_file(response)
    gdf = gdf.to_crs("EPSG:4326")
    gdf.geometry = gdf.geometry.simplify(0.0001)
    
    caminho = os.path.join(PASTA_SAIDA, f"{layer_name.replace(':', '__')}.geojson")
    gdf.to_file(caminho, driver="GeoJSON")
    print(f"Salvo em: {caminho}\n")

# Baixa todas as camadas
for camada in camadas:
    try:
        salvar_camada(camada)
    except Exception as e:
        print(f"Erro ao baixar {camada}: {e}")
