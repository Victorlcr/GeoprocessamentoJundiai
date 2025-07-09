from fastapi import APIRouter, HTTPException
from owslib.wfs import WebFeatureService
import geopandas as gpd
import json
from ..services import estilos

router = APIRouter()

@router.get("/wfs/{layer_name}")
async def get_wfs_layer(layer_name: str):
    """Obtém dados de uma camada WFS específica"""
    try:
        url_wfs = "https://geo.jundiai.sp.gov.br/geoserver/ows?service=WFS&acceptversions=2.0.0&request=GetCapabilities"
        wfs = WebFeatureService(url=url_wfs, version='2.0.0')
        
        response = wfs.getfeature(
            typename=layer_name,
            outputFormat='application/json',
            srsname='EPSG:31983'
        )
        
        # Converter para GeoJSON
        gdf = gpd.read_file(response)
        gdf = gdf.to_crs("EPSG:4326")
        gdf.geometry = gdf.geometry.simplify(0.0001)
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