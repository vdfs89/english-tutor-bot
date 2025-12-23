import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS
import pygame

# 1. Carrega variáveis de ambiente
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("Erro: GROQ_API_KEY não encontrada no arquivo .env")
    exit()

# Inicializa o mixer do pygame para tocar áudio
pygame.mixer.init()

def falar_texto(texto):
    try:
        tts = gTTS(text=texto, lang='en')
        arquivo_temp = "temp_audio.mp3"
        tts.save(arquivo_temp)
        pygame.mixer.music.load(arquivo_temp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(arquivo_temp)
    except Exception as e:
        print(f"(Erro ao reproduzir áudio: {e})")

# 2. Configura o modelo
# Usamos temperature=0.6 para ele ser um pouco mais natural/criativo na conversa
chat = ChatGroq(
    temperature=0.6,
    model_name="llama3-8b-8192"
)

# 3. Define o histórico inicial com a "persona"
# Instrução: Ser um tutor amigável, conversar em inglês e corrigir erros sutilmente.
mensagens = [
    ("system", "You are a friendly English tutor. Your goal is to help the user practice English conversation. "
               "Speak only in English. If the user makes a grammatical error, gently correct them inside your response, "
               "but keep the conversation flowing naturally.")
]

print("--- English Conversation Partner (Type 'sair' to exit) ---")
print("AI: Hello! I'm ready to help you practice your English. What would you like to talk about today?")

# 4. Loop de conversação
while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["quit", "exit", "sair"]:
        print("AI: Goodbye! Keep practicing!")
        break
        
    mensagens.append(("human", user_input))
    
    resposta = chat.invoke(mensagens)
    print(f"AI: {resposta.content}")
    
    mensagens.append(("ai", resposta.content))
    falar_texto(resposta.content)