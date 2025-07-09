from pydantic import BaseModel
from typing import Dict, Any

class RequisicaoAnalise(BaseModel):
    endereco: str

    # Adicione um exemplo para o Swagger
    class Config:
        json_schema_extra = {
            "example": {
                "endereco": "Av. 9 de Julho 1000, Jundiaí"
            }
        }

class AnaliseResult(BaseModel):
    area_total: float
    area_verde: float
    porcentagem: float
    coordenadas: Dict[str, float]
    geometrias_verdes: Dict[str, Any] 