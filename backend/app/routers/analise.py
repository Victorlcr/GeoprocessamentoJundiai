from fastapi import APIRouter, HTTPException
from ..models.esquema import RequisicaoAnalise 
from ..services.geocodificacao import geocodificar_endereco
from ..services.espacial import calcular_area_verde

router = APIRouter()

@router.post("/analise")
async def analisar_area(requisicao: RequisicaoAnalise):
    try:
        coordenadas = geocodificar_endereco(requisicao.endereco)
        resultado = calcular_area_verde(coordenadas)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))