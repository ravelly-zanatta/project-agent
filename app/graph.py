from langgraph.graph import StateGraph, END
from state import MessageState
from agents.classifier import classify_message
from agents.router import route_message
from handlers.fraude import handle_fraude
from handlers.assedio import handle_assedio
from handlers.reclamacao import handle_reclamacao
from handlers.outro import handle_outro
import csv

# Constrói e compila o grafo de execução do LangGraph
def build_graph():
    # Inicializa o grafo com o tipo de estado definido em app.state.MessageState
    graph = StateGraph(MessageState)

    # Nó responsável por classificar a mensagem
    graph.add_node("classify", classify_message)
    graph.add_node("fraude", handle_fraude)
    graph.add_node("assedio", handle_assedio)
    graph.add_node("reclamacao", handle_reclamacao)
    graph.add_node("outro", handle_outro)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_message,
        {
            "fraude": "fraude",
            "assedio": "assedio",
            "reclamacao": "reclamacao",
            "outro": "outro",
        }
    )

    graph.add_edge("fraude", END)
    graph.add_edge("assedio", END)
    graph.add_edge("reclamacao", END)
    graph.add_edge("outro", END)

    return graph.compile()

if __name__ == "__main__":
    app = build_graph()

    input_state = {
        #"text": "Fui ofendido pelo atendente",
        "text": "Estão usando meu CPF para abrir contas falsas",
        "classification": None,
        "department": None
    }

    result = app.invoke(input_state)
    print(result)
