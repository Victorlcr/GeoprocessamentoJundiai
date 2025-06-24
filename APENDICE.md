# Apêndice de termos  

- EPSG:4326 - Conjunto de dados WGS 84 para coordenadas 2D (latitude, longitude) com precisão de 2 metros, usado pelo Sistema de Posicionamento Global, entre outros.

- ESPG:31983 - Padrão utilizado na América Latina, com unidade de medida em metro.

---

- Polygon: Área simples e contínua.

- MultiPolygon: Agrupamento de várias áreas, tratadas como uma única feição (feature).

---

### WFS (Web Feature Service)
- Fornece dados vetoriais, ou seja, feições em formato como Point, LineString, Polygon, atributos tabulares, etc.
- Ideal para análises espaciais, manipulação, filtros e cálculos, como identificar áreas verdes e urbanas.

### WMS (Web Map Service)
- Fornece apenas imagens de mapas renderizadas, tipo um print do mapa.
- Útil para visualização, mas não serve para análises ou cálculos de geometrias.

### WMTS (Web Map Tile Service)
- Similar ao WMS, mas envia o mapa em pedaços ("tiles"), ótimo para visualização rápida em grandes áreas.
- Só visual, sem acesso direto a dados vetoriais.

### WCS (Web Coverage Service)
- Fornece dados matriciais (raster), como imagens de satélite, modelos de elevação, etc.
- Pode ser usado para análises de cobertura do solo se você souber interpretar ou classificar os pixels.

### Designação das "Zonas Especiais"

- [Plano Diretor de Jundiaí](https://planodiretor.jundiai.sp.gov.br/wp-content/uploads/2018/07/PD_Reuni%C3%A3o-2018-7-18.pptx.pdf)