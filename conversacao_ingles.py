import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS  # type: ignore
import pygame  # type: ignore
import speech_recognition as sr  # type: ignore
from groq import Groq

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

def ouvir_microfone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n(Listening... Speak now)")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
            
    temp_wav = "temp_mic.wav"
    with open(temp_wav, "wb") as f:
        f.write(audio.get_wav_data())
        
    client = Groq()
    with open(temp_wav, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(temp_wav, file.read()),
            model="whisper-large-v3",
            language="en"
        )
    os.remove(temp_wav)
    return transcription.text

# 2. Configura o modelo
# Usamos temperature=0.6 para ele ser um pouco mais natural/criativo na conversa
chat = ChatGroq(
    temperature=0.6,
    model="llama-3.3-70b-versatile"
)

# 3. Define o histórico inicial com a "persona"
# Instrução: Ser um tutor amigável, conversar em inglês e corrigir erros sutilmente.
mensagens = [
    ("system", "You are a friendly English tutor. Your goal is to help the user practice English conversation. "
               "Speak only in English. If the user makes a grammatical error, gently correct them inside your response, "
               "but keep the conversation flowing naturally.")
]

print("--- English Conversation Partner (Type 'sair' to exit) ---")
print("🌐 Web Version: https://linguaflow.streamlit.app/")
print("AI: Hello! I'm ready to help you practice your English. Speak to me!")

# 4. Loop de conversação
while True:
    try:
        user_input = ouvir_microfone()
        
        if not user_input:
            continue
            
        print(f"You: {user_input}")
        
        if user_input.lower() in ["quit", "exit", "sair"]:
            print("AI: Goodbye! Keep practicing!")
            break
            
        mensagens.append(("human", user_input))
        
        resposta = chat.invoke(mensagens)
        print(f"AI: {resposta.content}")
        
        mensagens.append(("ai", str(resposta.content)))
        falar_texto(str(resposta.content))

    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro (possivelmente na API): {e}")
        print("Reiniciando o ciclo de escuta...\n")