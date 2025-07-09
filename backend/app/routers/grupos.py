from fastapi import APIRouter
from ..services.wfs_jundiai import GRUPOS_CAMADAS

router = APIRouter()

@router.get("/grupos")
def listar_grupos():
    """Retorna a estrutura de grupos com metadados básicos"""
    return {
        "grupos": [
            {
                "nome": grupo,
                "camadas": camadas,
                "quantidade": len(camadas)
            }
            for grupo, camadas in GRUPOS_CAMADAS.items()
        ]
    }

@router.get("/grupos/{grupo}")
def obter_grupo(grupo: str):
    """Retorna metadados detalhados de um grupo específico"""
    if grupo not in GRUPOS_CAMADAS:
        return {"error": "Grupo não encontrado"}
    
    return {
        "nome": grupo,
        "camadas": GRUPOS_CAMADAS[grupo],
        #"descricao": DESCRICOES_GRUPOS.get(grupo, "Sem descrição disponível")
    }

# Descrições dos grupos (pode ser movido para um banco de dados posteriormente)
# DESCRICOES_GRUPOS = {
#     "areas_verdes": "Áreas verdes, parques e unidades de conservação",
#     "hidrografia": "Rios, represas, bacias hidrográficas e recursos hídricos",
#     "zoneamento": "Zoneamento urbano e uso do solo",
#     # Adicione descrições para outros grupos...
# }