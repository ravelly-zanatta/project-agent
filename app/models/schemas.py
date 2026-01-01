from pydantic import BaseModel
from typing import Literal

# Restringe os resultados do agente de classificação em conjuntos fixos 
class ClassificationResult(BaseModel):
    category: Literal["Fraude", "Assédio", "Reclamação", "Outro"]
