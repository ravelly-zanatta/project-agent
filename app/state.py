from typing import TypedDict, Optional

# Configuração da estrutura de estado da mensagem
class MessageState(TypedDict):
    text: str
    classification: Optional[str]
    department: Optional[str]
