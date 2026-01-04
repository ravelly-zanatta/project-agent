from app.state import MessageState
from logs.logger import get_logger, log_event

# Logger específico do Ombudsman
logger = get_logger(
    name="Ombudsman",
    log_file="logs/assedio.log"
)

# Encaminha a mensagem classificada como assédio para Ombudsman
def handle_assedio(state: MessageState) -> MessageState:
    state["department"] = "Ombudsman"

    # Log estruturado
    log_event(
        logger,
        {
            "event": "message_routed",
            "department": "Ombudsman",
            "classification": "assédio",
            "input_message": state["message"],
        }
    )

    print("Encaminhado para Ombudsman")
    return state

