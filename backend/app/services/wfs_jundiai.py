# backend/app/services/wfs_jundiai.py
from owslib.wfs import WebFeatureService
import geopandas as gpd
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Definição dos grupos de camadas
GRUPOS_CAMADAS = {
    "limites_territoriais": [
        "GeoJundiai:1979_IGC_limite_municipio",
        "GeoJundiai:L_8683-2016_m04_perimetro-urbano-rural",
        "GeoJundiai:L_9321-2019_m02-Limite_corredor_desenv_regional",
        "GeoJundiai:LC_461-2008_regioes",
        "GeoJundiai:LC_461-2008_bairros",
        "GeoJundiai:bairros_em_1968"
    ],
    "areas_verdes": [
        "GeoJundiai:LC_417-2004_SistProtSerradoJapi",
        "GeoJundiai:L_8683-2016_m03_rem-veg-nat",
        "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Cerrado",
        "GeoJundiai:L_9321-2019_m04-Remanescente_Vegetacao-Mata_Atlantica",
        "GeoJundiai:L_8683-2016_m13_parques-municipais",
    ],
    "hidrografia": [
        "GeoJundiai:L_2405-1980_Manancial",
        "GeoJundiai:L_8683-2016_hidrografia-principal",
        "GeoJundiai:L_8683-2016_m01_bacias-hidrograficas",
        "GeoJundiai:L_8683-2016_m01_recarga-hidrica",
        "GeoJundiai:L_8683-2016_m01_represas",
        "GeoJundiai:L_8683-2016_m02_nascentes",
        "GeoJundiai:L_9321-2019_m01-Bacias_Hidrograficas",
        "GeoJundiai:hidrografia_aero_1993"
    ],
    "zoneamento": [
        "GeoJundiai:L_10177-2024_m01_Macrozoneamento",
        "GeoJundiai:L_10177-2024_m02_Zoneamento",
        "GeoJundiai:L_7857-2012_perimetro-urbano",
        "GeoJundiai:L_7858-2012-zoneamento",
        "GeoJundiai:L_8683-2016_m05_macrozoneamento",
        "GeoJundiai:L_8683-2016_m06_zoneamento",
        "GeoJundiai:L_9321-2019_m01-Macrozoneamento",
        "GeoJundiai:L_9321-2019_m02-Zoneamento",
        "GeoJundiai:L_9806-2022_m02_zoneamento",
        "GeoJundiai:v_macrozoneamento",
        "GeoJundiai:v_usodosolo"
    ],
    "infraestrutura_urbana": [
        "GeoJundiai:L_8683-2016_m12_vias_func_urbanistica",
        "GeoJundiai:L_8683-2016_m13_redecicloviaria",
        "GeoJundiai:L_9321-2019_m08-Rede_Cicloviaria",
        "GeoJundiai:L_8683-2016_m13_terminais-situ",
        "GeoJundiai:onibus_terminais",
        "GeoJundiai:v_classdiretrizviar",
        "GeoJundiai:v_classviaria_atual",
        "GeoJundiai:v_diretrizes_viarias"
    ],
    "patrimonio_cultural": [
        "GeoJundiai:L_8683-2016_m09_ZEIHC-bens-tombados",
        "GeoJundiai:L_9321-2019_m03-Bens_Tombados",
        "GeoJundiai:m03_bens_tombados_cica",
        "GeoJundiai:L_8683-2016_m09_zeihc",
        "GeoJundiai:L_9321-2019_m03-ZEIHC"
    ],
    "areas_especiais": [
        "GeoJundiai:L_8683-2016_m07_zeis",
        "GeoJundiai:L_8683-2016_m08_zerfie",
        "GeoJundiai:L_10177-2024_m06_ZEIS",
        "GeoJundiai:L_8683-2016_m10_zepam",
        "GeoJundiai:v_zeis",
        "GeoJundiai:v_zerf"
    ],
    "cadastro_fundiario": [
        "GeoJundiai:L_10177-2024_m05_Cadastro_Fundiário",
        "GeoJundiai:L_9321-2019_m05-Cadastro_Fundiario",
        "GeoJundiai:edificacoes",
        "GeoJundiai:v_loteamentos"
    ],
    "enderecamento": [
        "GeoJundiai:enderecamento_cep",
        "GeoJundiai:L_9321-2019_m02-Logradouros",
        "GeoJundiai:v_denominacoes",
        "GeoJundiai:v_logr_nome",
        "GeoJundiai:denominacoes"
    ]
}

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
    
    url_wfs = "https://geo.jundiai.sp.gov.br/geoserver/ows?service=WFS&acceptversions=2.0.0&request=GetCapabilities"
    camadas = GRUPOS_CAMADAS[grupo]
    
    if combinar:
        gdf_combinado = gpd.GeoDataFrame()
    else:
        resultado = {}
    
    for camada in camadas:
        try:
            logger.info(f"Carregando camada: {camada}")
            wfs = WebFeatureService(url=url_wfs, version='2.0.0', timeout=60)
            response = wfs.getfeature(
                typename=camada,
                outputFormat='application/json',
                srsname='EPSG:31983'
            )
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
    return carregar_camadas("areas_verdes")