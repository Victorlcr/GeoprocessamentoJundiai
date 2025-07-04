from .wfs_jundiai import GRUPOS_CAMADAS

GRUPOS_CORES = {
    "areas_verdes": "#4CAF50",
    "hidrografia": "#2196F3",
    "zoneamento": "#FF9800",
    "infraestrutura_urbana": "#9C27B0",
    "patrimonio_cultural": "#795548",
    "areas_especiais": "#F44336",
    "cadastro_fundiario": "#607D8B",
    "enderecamento": "#00BCD4",
    "limites_territoriais": "#000000"
}

def obter_cor_por_grupo(grupo: str):
    return GRUPOS_CORES.get(grupo, "#777777")

def obter_cor_por_camada(camada: str):
    for grupo, camadas in GRUPOS_CAMADAS.items():
        if camada in camadas:
            return obter_cor_por_grupo(grupo)
    return "#777777"