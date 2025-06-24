from owslib.wfs import WebFeatureService
import geopandas as gpd
from shapely.geometry import Polygon
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

def obter_borda_municipio():
    """
    Obtém a geometria do contorno municipal de Jundiaí a partir da camada histórica
    
    Returns:
        shapely.geometry.Polygon: Geometria do município em EPSG:31983
    """
    url_wfs = "https://geo.jundiai.sp.gov.br/geoserver/ows"
    camada = "GeoJundiai:1979_IGC_limite_municipio"
    
    try:
        # Acessar o WFS
        wfs = WebFeatureService(url=url_wfs, version='2.0.0')
        response = wfs.getfeature(
            typename=camada,
            outputFormat='application/json',
            srsname='EPSG:31983'
        )
        
        # Carregar em GeoDataFrame
        gdf = gpd.read_file(response)
        
        # Verificar se obteve dados
        if gdf.empty:
            logger.error("Camada municipal retornou vazia")
            return None
            
        # Dissolver todas as geometrias em um único polígono
        municipio = gdf.dissolve().geometry.iloc[0]
        
        # Simplificar geometria se necessário (opcional)
        if municipio.geom_type == 'MultiPolygon':
            # Criar envelope convexo para simplificar
            municipio = municipio.convex_hull
            
        logger.info("Borda municipal obtida com sucesso")
        return municipio
        
    except Exception as e:
        logger.error(f"Erro ao obter borda municipal: {str(e)}")
        return None

def criar_buffer_seguro():
    """
    Cria um buffer de segurança ao redor do município para validar endereços próximos
    
    Returns:
        shapely.geometry.Polygon: Buffer de 5km ao redor do município
    """
    municipio = obter_borda_municipio()
    if municipio:
        return municipio.buffer(5000)  # 5km em metros
    return None

def esta_dentro_municipio(longitude: float, latitude: float):
    """
    Verifica se um ponto está dentro do território municipal
    
    Args:
        longitude: Coordenada X (SIRGAS 2000)
        latitude: Coordenada Y (SIRGAS 2000)
    
    Returns:
        bool: True se o ponto estiver dentro do município
    """
    from shapely.geometry import Point
    
    municipio = obter_borda_municipio()
    if not municipio:
        return False
        
    ponto = Point(longitude, latitude)
    return municipio.contains(ponto)