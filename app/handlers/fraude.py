from state import MessageState

# Encaminha a mensagem classificada como fraude para Central de Fraude
def handle_fraude(state: MessageState) -> MessageState:
    state["department"] = "Central de Fraude"
    print("Encaminhado para Central de Fraude")
    return state
