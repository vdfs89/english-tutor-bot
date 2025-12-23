import os
from dotenv import load_dotenv
from groq import Groq

# 1. Carrega as variáveis de ambiente
load_dotenv()

# 2. Inicializa o cliente Groq (busca automaticamente GROQ_API_KEY)
client = Groq()

# Defina o nome do seu arquivo de áudio aqui (mp3, mp4, mpeg, mpga, m4a, wav, ou webm)
arquivo_audio = "audio_teste.mp3"

if not os.path.exists(arquivo_audio):
    print(f"Erro: O arquivo '{arquivo_audio}' não foi encontrado na pasta.")
    print("Por favor, coloque um arquivo de áudio na pasta e ajuste a variável 'arquivo_audio' neste script.")
else:
    print("Iniciando transcrição...")
    with open(arquivo_audio, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(arquivo_audio, file.read()),
            model="whisper-large-v3",
            language="pt"  # Opcional: força o idioma para português
        )
        print("\nTexto Transcrito:")
        print(transcription.text)