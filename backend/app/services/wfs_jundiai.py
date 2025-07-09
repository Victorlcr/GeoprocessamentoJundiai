# backend/app/services/wfs_jundiai.py
import os
import geopandas as gpd
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Definição dos grupos de camadas
GRUPOS_CAMADAS = {
    "areas_verdes": [
        "GeoJundiai:LC_417-2004_SistProtSerradoJapi",
        "GeoJundiai:L_8683-2016_m03_rem-veg-nat",
        "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Cerrado",
        "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Mata_Atlantica",
        "GeoJundiai:L_8683-2016_m13_parques-municipais",
    ]
}

CAMINHO_CACHE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))


def carregar_camadas(grupo: str, combinar: bool = True):
    """
    Carrega camadas de um grupo específico do WFS
    
    Args:
        grupo: Nome do grupo de camadas
        combinar: Se True, combina todas as camadas em um único GeoDataFrame
    
    Returns:
        GeoDataFrame combinado ou dicionário de GeoDataFrames por camada
    """
    if grupo not in GRUPOS_CAMADAS:
        raise ValueError(f"Grupo '{grupo}' não existe. Grupos válidos: {list(GRUPOS_CAMADAS.keys())}")
    
    camadas = GRUPOS_CAMADAS[grupo]
    
    if combinar:
        gdf_combinado = gpd.GeoDataFrame()
    else:
        resultado = {}
    
    for camada in camadas:
        try:
            filename = camada.replace(":", "__") + ".geojson"
            response = os.path.join(CAMINHO_CACHE, filename)
            gdf = gpd.read_file(response)
            
            # Garantir CRS consistente
            if gdf.crs is None:
                gdf.crs = "EPSG:31983"

            if not gdf.empty:
                # 1. Corrigir geometrias inválidas
                gdf['geometry'] = gdf.geometry.buffer(0)
                
                # 2. Filtrar apenas geometrias válidas
                gdf = gdf[gdf.geometry.is_valid]
                
                # 3. Remover geometrias vazias
                gdf = gdf[~gdf.geometry.is_empty]
            
            if combinar:
                if gdf_combinado.empty:
                    gdf_combinado = gdf
                else:
                    gdf_combinado = gpd.pd.concat([gdf_combinado, gdf], ignore_index=True)
            else:
                resultado[camada] = gdf
                
        except Exception as e:
            logger.error(f"Erro ao carregar camada {camada}: {str(e)}")
            continue
    
    if combinar:
        # Dissolver geometrias para evitar sobreposições
        try:
            if not gdf_combinado.empty:
                gdf_combinado = gdf_combinado.dissolve()
        except Exception as e:
            logger.warning(f"Não foi possível dissolver geometrias: {str(e)}")
        return gdf_combinado
    
    return resultado

def carregar_areas_verdes():
    """Função específica para carregar camadas de áreas verdes (combinadas)"""
    return carregar_camadas("areas_verdes").to_crs("EPSG:31983")