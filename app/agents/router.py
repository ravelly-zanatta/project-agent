from state import MessageState

# Função que define o fluxo do LangGraph com base na classificação da mensagem
def route_message(state: MessageState) -> str:
    match state["classification"]:
        case "Fraude":
            return "fraude"
        case "Assédio":
            return "assedio"
        case "Reclamação":
            return "reclamacao"
        case _:
            return "outro"
