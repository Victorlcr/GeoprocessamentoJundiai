from shapely.geometry import Point
import geopandas as gpd
from .wfs_jundiai import carregar_areas_verdes

def calcular_area_verde(coordenadas: tuple[float, float]):
    # Carregar todas as camadas verdes
    areas_verdes = carregar_camadas_verdes()
    
    # Criar buffer
    ponto = Point(coordenadas)
    buffer = ponto.buffer(1000)  # 1000 metros
    
    # Interseção com todas as áreas verdes
    areas_verdes_buffer = gpd.overlay(areas_verdes, gpd.GeoDataFrame(geometry=[buffer], crs=areas_verdes.crs), how='intersection')
    
    # Cálculo da área verde total
    area_verde = areas_verdes_buffer.geometry.area.sum()
    
    return {
        "area_total": buffer.area,
        "area_verde": area_verde,
        "porcentagem": (area_verde / buffer.area) * 100
    }