import geopandas as gpd
from shapely.geometry import Point
from .wfs_jundiai import carregar_areas_verdes
import logging

logger = logging.getLogger(__name__)

def calcular_area_verde(coordenadas: tuple[float, float], raio_metros: float = 500) -> dict:
    """
    Calcula a porcentagem de área verde em um buffer ao redor das coordenadas fornecidas.

    Args:
        coordenadas: Tupla (longitude, latitude)
        raio_metros: Raio do buffer em metros (default: 500m)

    Returns:
        Um dicionário com área total, área verde e percentual de área verde
    """
    longitude, latitude = coordenadas

    # Cria ponto com as coordenadas (WGS84)
    ponto = gpd.GeoSeries([Point(longitude, latitude)], crs="EPSG:4326")

    # Reprojeta para um CRS métrico adequado (SIRGAS 2000 / UTM zone 23S)
    ponto = ponto.to_crs("EPSG:31983")

    # Cria buffer (raio em metros)
    buffer = ponto.buffer(raio_metros)

    # Transforma em GeoDataFrame
    buffer_gdf = gpd.GeoDataFrame(geometry=buffer, crs="EPSG:31983")
    buffer_area = buffer_gdf.geometry.area.values[0]  # em m²

    # Carrega áreas verdes (também em EPSG:31983)
    logger.info("Carregando camadas de áreas verdes...")
    areas_verdes_gdf = carregar_areas_verdes()

    if areas_verdes_gdf.empty:
        raise ValueError("Nenhuma área verde carregada.")

    # Interseção: áreas verdes dentro do buffer
    interseccao = gpd.overlay(areas_verdes_gdf, buffer_gdf, how="intersection")
    area_verde_m2 = interseccao.geometry.area.sum()

    # Calcula percentual
    percentual = (area_verde_m2 / buffer_area) * 100 if buffer_area > 0 else 0

    return {
        "area_total_m2": round(buffer_area, 2),
        "area_verde_m2": round(area_verde_m2, 2),
        "percentual_area_verde": round(percentual, 2)
    }
