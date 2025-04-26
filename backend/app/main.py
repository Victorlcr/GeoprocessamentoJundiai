from fastapi import FastAPI
from .routers import analises
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(analises.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "API de Análise de Áreas Verdes"}