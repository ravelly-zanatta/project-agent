from app.state import MessageState

# Encaminha a mensagem classificada como assédio para Ombudsman
def handle_assedio(state: MessageState) -> MessageState:
    state["department"] = "Ombudsman"
    print("Encaminhado para Ombudsman")
    return state
