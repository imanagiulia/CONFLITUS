from fastapi import FastAPI
from app.controllers import simulacao
from app.controllers import rotas
from app.controllers import fontes

app = FastAPI(
    title="CONFLITUS - Simulador Educativo",
    description="Mapeamento de cenários de conflito e análise de rotas."
)

# Conecta os controllers ao aplicativo principal
app.include_router(simulacao.router, tags=["Simulação de Impacto"])
app.include_router(rotas.router, tags=["Análise de Rotas"])
app.include_router(fontes.router, tags=["Transparência e Fontes"])

@app.get("/")
def home():
    """Endpoint de boas-vindas para checar se a API está no ar."""
    return {"mensagem": "Bem-vindo à API do projeto CONFLITUS!"}