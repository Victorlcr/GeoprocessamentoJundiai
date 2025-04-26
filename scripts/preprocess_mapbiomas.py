import geopandas as gpd
import rasterio
from rasterio.mask import mask

def clip_mapbiomas_to_jundiai():
    # Carregar limites de Jundiaí (ex: Shapefile da prefeitura)
    jundiai = gpd.read_file("data/raw/jundiai_boundary.shp")
    
    # Carregar raster do MapBiomas
    with rasterio.open("data/raw/mapbiomas_2022.tif") as src:
        # Recortar para a área de Jundiaí
        out_image, out_transform = mask(src, jundiai.geometry, crop=True)
        
        # Salvar recorte
        profile = src.profile
        profile.update(height=out_image.shape[1], width=out_image.shape[2], transform=out_transform)
        
        with rasterio.open("data/processed/mapbiomas_jundiai.tif", "w", **profile) as dest:
            dest.write(out_image)