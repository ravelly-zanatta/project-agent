from state import MessageState
from logs.logger import get_logger, log_event

# Logger específico do Central de Fraude
logger = get_logger(
    name="Central de Fraude",
    log_file="logs/fraude.log"
)

# Encaminha a mensagem classificada como fraude para Central de Fraude
def handle_fraude(state: MessageState) -> MessageState:
    state["department"] = "Central de Fraude"

    # Log estruturado
    log_event(
        logger,
        {
            "event": "message_routed",
            "department": "Central de Fraude",
            "classification": "fraude",
            "input_message": state["message"],
        }
    )

    print("Encaminhado para Central de Fraude")
    return state
