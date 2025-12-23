import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
from groq import Groq
import tempfile

# Configuração da Página
st.set_page_config(page_title="English Tutor AI", page_icon="🇬🇧", layout="wide")
st.title("🇬🇧 English Conversation Partner")

# 1. Carrega variáveis de ambiente
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error("Erro: GROQ_API_KEY não encontrada no arquivo .env")
    st.stop()

# 2. Inicializa o estado da sessão (Histórico e Modelo)
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("system", "You are a friendly English tutor. Your goal is to help the user practice English conversation. "
                   "Speak only in English. If the user makes a grammatical error, gently correct them inside your response, "
                   "but keep the conversation flowing naturally.")
    ]

if "chat" not in st.session_state:
    st.session_state.chat = ChatGroq(
        temperature=0.6,
        model_name="llama3-8b-8192"
    )

# Função para processar a resposta da IA e gerar áudio
def processar_resposta(user_text):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append(("human", user_text))
    
    # Gera resposta da IA
    resposta = st.session_state.chat.invoke(st.session_state.messages)
    st.session_state.messages.append(("ai", resposta.content))
    
    return resposta.content

# 4. Área de Entrada de Voz (Movido para o topo da página principal)
st.write("### Voice Input")
# Componente de gravação compatível com navegadores web
audio = mic_recorder(
    start_prompt="🎤 Speak Now",
    stop_prompt="⏹ Stop",
    key='recorder'
)

if audio:
    with st.spinner("Transcribing..."):
        try:
            # Salva o áudio (bytes) em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio['bytes'])
                tmp_filename = tmp.name
            
            # Transcreve usando Groq
            client = Groq()
            with open(tmp_filename, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(tmp_filename, file.read()),
                    model="whisper-large-v3",
                    language="en"
                )
            os.remove(tmp_filename)
            
            if transcription.text:
                processar_resposta(transcription.text)
                st.rerun()
                
        except Exception as e:
            st.error(f"Error processing audio: {e}")

# 3. Exibe o histórico de chat
for role, content in st.session_state.messages:
    if role == "system":
        continue
    with st.chat_message(role):
        st.write(content)
        # Se for a última mensagem e for da IA, gera o áudio (opcional: apenas para a última)
        if role == "ai" and content == st.session_state.messages[-1][1]:
            try:
                tts = gTTS(text=content, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    with open(tmp.name, "rb") as f:
                        audio_bytes = f.read()
                os.remove(tmp.name)
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error(f"Erro no áudio: {e}")

if user_input := st.chat_input("Type your message here..."):
    processar_resposta(user_input)
    st.rerun()