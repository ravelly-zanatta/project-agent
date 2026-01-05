# Sistema Multiagente de Classificação e Encaminhamento de Mensagens
## Visão Geral
Este projeto implementa um sistema multiagente que classifica automaticamente as mensagens recebidas e as encaminha aos respectivos setores, utilizando **LangChain** e **LangGraph**.
As mensagens podem ser classificadas em **assédio**, **fraude**, **reclamação** e **outros**.

Relação entre as classificações e setores:
  - Assédio     ---> Ombudsman
  - Fraude      ---> Central de Fraude
  - Reclamação  ---> Atendimento ao Cliente
  - Outro       ---> Central de Atendimento Geral

Nesse projeto, o **Langchain** foi utilizado como camada responsável pela integração com as LLMs e pela definição de ferramentas e prompts que orientam o processamento das mensagens.

O **LangGraph** foi utilizado para a orquestração do fluxo multiagente, organizando o processamento das mensagens em um grafo de estados definido. Cada nó do grafo representa uma etapa específica, como classificação, roteamento e encaminhamento, enquanto as transições controlam a sequência lógica e as decisões do sistema.

O diagrama abaixo mostra, resumidamente, o fluxo do processo de classificação das mensagens e de encaminhamento aos setores.
```
                     +--------------------+
                     | Entrada dos dados  |
                     | (CSV ou API REST)  |
                     +---------+----------+
                               |
                               v
                     +--------------------+
                     | Leitura / Parsing  |
                     | das mensagens      |
                     +---------+----------+
                               |
                               v
          +-------------------------------------------+
          |               LangGraph                   |
          |-------------------------------------------|
          |  +-------------------+                    |
          |  | Classificação     |  (LangChain e LLM) |
          |  +-------------------+                    |
          |            |                              |
          |            v                              |
          |  +-------------------+                    |
          |  | Roteamento        |  (condicional)     |
          |  +-------------------+                    |
          |            |                              |
          |            v                              |
          |  +-------------------+                    |
          |  | Encaminhamento    |  (handlers)        |
          |  | simulado (logs)   |                    |
          |  +-------------------+                    |
          +-------------------+-----------------------+
                              |
                              v
                +----------------------------+
                | Observabilidade            |
                | - Logs estruturados (JSON) |
                | - Dashboard Streamlit      |
                +----------------------------+

```
#### Escolha do Modelo de Linguagem (LLM)

O modelo `openai/gpt-oss-20b` foi escolhido para esse projeto devido à sua alta precisão e à capacidade de inferência semântica e de compreensão contextual, especialmente em contextos sensíveis (fraude e assédio) que podem conter mensagens ambíguas, sensíveis, emocionais ou até mesmo mal escritas. Nesses casos, um falso negativo pode resultar em impactos críticos.

Embora modelos menores ofereçam menor latência, o `GPT-OSS-20B` apresenta um bom equilíbrio entre desempenho e custo, com throughput elevado (~1000 tokens/s), amplo contexto e maior robustez na tomada de decisão. Essa característica é fundamental para reduzir erros de classificação em cenários críticos.

### Tecnologias Complementares:
- **Groq:** Por meio da integração com a **API Groq** via **LangChain**, o sistema consegue acessar modelos otimizados para desempenho, garantindo respostas rápidas mesmo em cenários de alto volume de mensagens.
- **FastAPI:** É responsável por expor uma **API REST** para integração com sistemas externos. Ele permite receber mensagens via HTTP, validá-las automaticamente, encaminhá-las ao fluxo de processamento e retornar respostas estruturadas de forma eficiente. (Esse projeto também tem a opção de ler uma lista de mensagens em um arquivo `.csv` para testar o modelo)
- **Streamlit:** O Streamlit permite criar um **dashboard** interativo para acompanhar o comportamento do sistema. Por meio dele, é possível visualizar métricas como volume de mensagens, classificações, encaminhamentos por setor, distribuição temporal e alertas operacionais, a partir dos logs de saída do sistema.

## Como executar o projeto
### Instalar dependências
**Passo 1:** Cria ambiente virtual (opcional)
```
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

**Passo 2:** Instalar dependências
```
pip install -r requirements.txt
```

### Executar Projeto (Com lista de mensagens via arquivo `.csv`)

**Passo 1:** Configuração do Groq.
  - [Acessar o site da Groq](https://groq.com/)
  - Start Building -> Create Account -> API Keys -> Create API Key
  - Copiar a API Key e colar no arquivo `.env`.
  - **OBS:** Você pode visualizar os modelos disponíveis para teste pelo Groq em _Docs -> Models_

**Passo 2:** Executar testes de classificação.

Na pasta raiz do projeto executar o comando:
```
python -m app.graph
```

### Execução do Dashboard (Streamlit)
**Passo 1:** Na pasta raiz do projeto executar o comando:
```
streamlit run .\dashboard\dashboard.py
```
Após a execução, caso não abra automaticamente, o Streamlit irá disponibilizar um endereço local, como: `Local URL: http://localhost:8501`

### Execução da API REST (FastAPI)
**Passo 1:** Na pasta raiz do projeto, iniciar a API executando o comando:
```
uvicorn app.api.main:app --reload
```
A API ficará disponível em: `http://127.0.0.1:8000`

#### Documentação automática (Swagger)
O FastAPI gera automaticamente a documentação interativa em: `http://127.0.0.1:8000/docs`

### Exemplo de Uso da API
**Endpoint de classificação:** POST `/classify`

#### Enviar uma mensagem: 
**Passo 1:** Clicar em **`Try it out`**

**Passo 2:** Escrever a mensagem

Corpo da requisição (JSON):
```
{
  "message": "O produto não correspondeu as minhas expectativas."
}
```

**Passo 3:** Clicar em **`Execute`**

Resposta esperada:
```
{
  "message": "O produto não correspondeu as minhas expectativas.",
  "classification": "Reclamação",
  "department": "Atendimento ao Cliente",
  "event": "Você está sendo encaminhado para Atendimento ao Cliente"
}
```

## Tecnologias Utilizadas (Resumo)

 - Python
 - FastAPI
 - LangChain
 - LangGraph
 - Streamlit
 - Pydantic
