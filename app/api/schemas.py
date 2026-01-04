from pydantic import BaseModel

# Schema de entrada da API
class MessageRequest(BaseModel):
    message: str

# Schema de saída da API
class MessageResponse(BaseModel):
    message: str
    classification: str
    department: str
    event: str
