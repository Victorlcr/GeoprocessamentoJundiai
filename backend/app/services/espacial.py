from shapely.geometry import Point
import geopandas as gpd

def calcular_area_verde(coordinates: tuple[float, float]):
    # Converter coordenadas para SIRGAS 2000 (EPSG:31983)
    point = gpd.GeoSeries([Point(coordinates)], crs="EPSG:4326").to_crs("EPSG:31983")[0]
    
    # Criar buffer de 1 km² (1000 metros)
    buffer = point.buffer(1000)
    
    # Simular dados de áreas verdes (substitua com dados reais do MapBiomas)
    green_areas = {
        "total_area": 1000000,  # 1 km² em m²
        "area_verde": 250000,    # Exemplo: 25% de área verde
        "porcentagem": 25.0
    }
    return green_areas