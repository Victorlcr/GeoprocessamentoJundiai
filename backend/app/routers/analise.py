from fastapi import APIRouter, HTTPException
from ..models.esquema import AnaliseResult
from ..models.esquema import RequisicaoAnalise
from ..services.geocodificacao import geocodificar_endereco
from ..services.espacial import calcular_area_verde
import geopandas as gpd
from shapely.geometry import Point

router = APIRouter()

@router.post("/analise", response_model=AnaliseResult)
async def analisar_area(requisicao: RequisicaoAnalise):
    try:
        coordenadas = geocodificar_endereco(requisicao.endereco)
        # Converter para GeoDataFrame temporário para validação
        gdf_temp = gpd.GeoDataFrame(
            geometry=[Point(coordenadas)],
            crs="EPSG:4326"
        )
        
        # Verificar se é um ponto válido
        if gdf_temp.geometry.is_empty.any():
            raise ValueError("Coordenadas inválidas")
        resultado = calcular_area_verde(coordenadas)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))