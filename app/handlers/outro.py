from state import MessageState
from logs.logger import get_logger, log_event

# Logger específico do Central de Atendimento Geral
logger = get_logger(
    name="Central de Atendimento Geral",
    log_file="logs/outro.log"
)

# Encaminha a mensagem classificada como outro para Central de Atendimento Geral
def handle_outro(state: MessageState) -> MessageState:
    state["department"] = "Central de Atendimento Geral"

    # Log estruturado
    log_event(
        logger,
        {
            "event": "message_routed",
            "department": "Central de Atendimento Geral",
            "classification": "outro",
            "input_message": state["text"],
        }
    )

    print("Encaminhado para Central de Atendimento Geral")
    return state
