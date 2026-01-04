from app.state import MessageState
from logs.logger import get_logger, log_event

# Logger específico do Atendimento ao Cliente
logger = get_logger(
    name="Atendimento ao Cliente",
    log_file="logs/reclamacao.log"
)

# Encaminha a mensagem classificada como reclamação para Atendimento ao Cliente
def handle_reclamacao(state: MessageState) -> MessageState:
    state["department"] = "Atendimento ao Cliente"

    # Log estruturado
    log_event(
        logger,
        {
            "event": "message_routed",
            "department": "Atendimento ao Cliente",
            "classification": "reclamação",
            "input_message": state["message"],
        }
    )

    print("Encaminhado para Atendimento ao Cliente")
    return state
