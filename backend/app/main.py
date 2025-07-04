from fastapi import FastAPI
from .routers import analise, grupos, wfs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(analise.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API de Análise de Áreas Verdes"}

app.include_router(grupos.router, prefix="/api")
app.include_router(wfs.router, prefix="/api")
app.include_router(analise.router, prefix="/api")