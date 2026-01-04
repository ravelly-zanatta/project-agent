from fastapi import FastAPI
from app.api.routes import router

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Classificação de Mensagens",
    description="API REST para classificação, roteamento e encaminhamento de mensagens usando Langchain e LangGraph",
    version="1.0.0"
)

# Registra os endpoints no roteador principal
app.include_router(router)
