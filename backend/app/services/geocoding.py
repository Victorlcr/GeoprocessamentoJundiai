from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_address(address: str) -> tuple[float, float]:
    geolocator = Nominatim(user_agent="jundiai-green-areas")
    try:
        location = geolocator.geocode(f"{address}, Jundiaí, Brasil")
        if location:
            return (location.longitude, location.latitude)  # Retorna (x, y) para GeoPandas
        else:
            raise ValueError("Endereço não encontrado")
    except GeocoderTimedOut:
        raise Exception("Timeout na geocodificação")