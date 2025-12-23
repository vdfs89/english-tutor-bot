import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Carrega as variáveis do arquivo .env (GROQ_API_KEY)
load_dotenv()

# 2. Inicializa o modelo ChatGroq
# O parâmetro 'model' define qual LLM usar (ex: llama3-8b-8192 ou llama3-70b-8192)
chat = ChatGroq(
    temperature=0,
    model="llama3-8b-8192"
)

# 3. Cria um template de prompt para estruturar a conversa
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente conciso e prestativo."),
    ("human", "{pergunta}")
])

# 4. Cria a cadeia (chain) conectando o prompt ao modelo
chain = prompt | chat

# 5. Executa a cadeia
resposta = chain.invoke({"pergunta": "Quais são as vantagens de usar Groq com LangChain?"})

print(resposta.content)
