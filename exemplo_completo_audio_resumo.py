import os
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GROQ_API_KEY não foi encontrada.")

# 2. Configuração do arquivo de áudio
arquivo_audio = "audio_teste.mp3"

if not os.path.exists(arquivo_audio):
    print(f"Erro: O arquivo '{arquivo_audio}' não foi encontrado.")
    print("Por favor, adicione um arquivo 'audio_teste.mp3' na pasta para testar.")
    exit()

print("--- Passo 1: Transcrevendo Áudio com Whisper (Groq) ---")

# 3. Transcrição usando cliente nativo Groq
client = Groq(api_key=api_key)

with open(arquivo_audio, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=(arquivo_audio, file.read()),
        model="whisper-large-v3",
        language="pt"
    )

texto_transcrito = transcription.text
print(f"Texto original detectado ({len(texto_transcrito)} caracteres).")

print("\n--- Passo 2: Gerando Resumo com Llama 3 (LangChain) ---")

# 4. Configuração do LangChain com Llama 3
chat = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente especialista em resumir textos. Crie um resumo conciso em tópicos (bullet points) do texto fornecido pelo usuário."),
    ("human", "Texto para resumir:\n\n{texto}")
])

chain = prompt | chat

# 5. Execução da chain passando o texto transcrito
resposta = chain.invoke({"texto": texto_transcrito})

print("\nResumo Gerado:")
print(resposta.content)