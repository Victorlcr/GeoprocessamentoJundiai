from fastapi import APIRouter, HTTPException
from ..services.geocoding import geocode_address
from ..services.espacial import calculate_green_area

router = APIRouter()

@router.post("/analise")
async def analyze_area(address: str):
    try:
        # Etapa 1: Geocodificação
        coordinates = geocode_address(address)
        
        # Etapa 2: Cálculo da área verde
        result = calculate_green_area(coordinates)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))