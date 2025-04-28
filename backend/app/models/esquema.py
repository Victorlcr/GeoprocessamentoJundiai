from pydantic import BaseModel

class RequisicaoAnalise(BaseModel):
    endereco: str

    # Adicione um exemplo para o Swagger
    class Config:
        json_schema_extra = {
            "example": {
                "endereco": "Av. 9 de Julho 1000, Jundiaí"
            }
        }