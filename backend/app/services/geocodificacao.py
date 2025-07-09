from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocodificar_endereco(endereco: str) -> tuple[float, float]:
    geolocalizador = Nominatim(user_agent="jundiai-geoprocessamento", timeout=25)
    try:
        localizacao = geolocalizador.geocode(f"{endereco}, Jundiaí, Brasil")
        if localizacao:
            return (localizacao.longitude, localizacao.latitude)
        else:
            raise ValueError("Endereço não encontrado")
    except GeocoderTimedOut:
        raise Exception("Timeout na geocodificação")