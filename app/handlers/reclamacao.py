from state import MessageState

# Encaminha a mensagem classificada como reclamação para Atendimento ao Cliente
def handle_reclamacao(state: MessageState) -> MessageState:
    state["department"] = "Atendimento ao Cliente"
    print("Encaminhado para Atendimento ao Cliente")
    return state
