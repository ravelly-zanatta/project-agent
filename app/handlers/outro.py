from app.state import MessageState

# Encaminha a mensagem classificada como outro para Central de Atendimento Geral
def handle_outro(state: MessageState) -> MessageState:
    state["department"] = "Central de Atendimento Geral"
    print("Encaminhado para Central de Atendimento Geral")
    return state
