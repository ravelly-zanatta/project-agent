from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.models.schemas import ClassificationResult
from app.state import MessageState

# Criar o parser estruturado
parser = PydanticOutputParser(pydantic_object=ClassificationResult)

# Definir o prompt de classificação
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Você é um classificador de mensagens de clientes recebidas via WhatsApp.

        Classifique a mensagem abaixo em APENAS UMA das categorias:
        - Fraude
        - Assédio
        - Reclamação
        - Outro

        Responda somente com o nome da categoria."""
    ),
    # Mensagem do usuário (humano)
    # {message} -> conteúdo da mensagem do cliente
    # {format_instructions} -> instruções automáticas do parser Pydantic
    ("human", "{message}\n\n{format_instructions}")
])

# Inicializa a LMM Groq
llm = ChatGroq(model="openai/gpt-oss-20b", 
              temperature=0.0
              )

# Pipeline: Prompt -> LLM -> Parser estruturado
chain = prompt | llm | parser

# Função do nó de classificação
def classify_message(state: MessageState) -> MessageState:
    result = chain.invoke({
        "message": state["message"],
        "format_instructions": parser.get_format_instructions()
    })

    state["classification"] = result.category
    return state
