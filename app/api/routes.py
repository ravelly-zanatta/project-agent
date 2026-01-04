from fastapi import APIRouter
from app.graph import build_graph
from app.api.schemas import MessageRequest, MessageResponse

# Cria o roteador de endpoints da API
router = APIRouter()
# Inicializa o grafo de agentes (LangGraph)
graph = build_graph()

@router.post("/classify", response_model=MessageResponse)
def classify_message(request: MessageRequest):
    initial_state = {
        "message": request.message,
        "classification": None,
        "department": None
    }

    # Execução do grafo de agentes
    result = graph.invoke(initial_state)

    # Retorna a resposta estruturada para o cliente da API
    return MessageResponse(
        message=result["message"],
        classification=result["classification"],
        department=result["department"],
        event=f"Você está sendo encaminhado para {result['department']}"
    )
