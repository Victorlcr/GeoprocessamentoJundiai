import os
from fastapi import APIRouter, HTTPException
import geopandas as gpd
import os
import json
from ..services import estilos
from fastapi import APIRouter, HTTPException
import geopandas as gpd


router = APIRouter()
CAMINHO_CACHE = "backend/app/static"

@router.get("/wfs/{layer_name}")
async def get_wfs_layer(layer_name: str):
    """Obtém dados de uma camada WFS específica"""
    try:
        filename = layer_name.replace(":", "__") + ".geojson"
        filepath = os.path.join(CAMINHO_CACHE, filename)
        
        gdf = gpd.read_file(filepath)
        geojson = json.loads(gdf.to_json())
        return {
            "layer": layer_name,
            "color": estilos.obter_cor_por_camada(layer_name),
            "data": geojson
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao acessar camada WFS: {str(e)}"
        )