from shapely.geometry import Point
from .wfs_jundiai import carregar_areas_verdes
from pyproj import Transformer
import json
import logging

def calcular_area_verde(coordenadas: tuple[float, float]):
    """Calcula área verde em torno de coordenadas (lon, lat) em WGS84"""
    logger = logging.getLogger(__name__)
    try:
        # 1. Converter coordenadas para SIRGAS 2000
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)
        x, y = transformer.transform(coordenadas[0], coordenadas[1])
        ponto = Point(x, y)
        
        # 2. Criar buffer de 1 km
        buffer = ponto.buffer(1000)  # 1000 metros
        
        # 3. Carregar áreas verdes
        areas_verdes = carregar_areas_verdes()
        
        # 4. Filtrar geometrias válidas
        areas_verdes = areas_verdes[areas_verdes.geometry.is_valid & 
                                   ~areas_verdes.geometry.is_empty]
        
        # 5. Interseção espacial
        areas_verdes_buffer = areas_verdes[areas_verdes.intersects(buffer)]
        geojson_verde = json.loads(areas_verdes_buffer.to_json()) if not areas_verdes_buffer.empty else {"type": "FeatureCollection", "features": []}
        
        # 6. Cálculo da área verde total
        area_verde = areas_verdes_buffer.geometry.area.sum()
        area_total = buffer.area
        
        return {
            "area_total": round(area_total / 1_000_000, 2),  # em km²
            "area_verde": round(area_verde / 1_000_000, 2),
            "porcentagem": round((area_verde / area_total) * 100, 2),
            "coordenadas": {
                "lat": coordenadas[1],
                "lon": coordenadas[0]
            },
            "geometrias_verdes": geojson_verde
            }
        
    except Exception as e:
        logger.error(f"Erro no cálculo de área verde: {str(e)}")
        raise