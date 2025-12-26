import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
from groq import Groq
import tempfile

# Configuração da Página
st.set_page_config(page_title="LinguaFlow AI", page_icon="🌊", layout="wide")
st.title("🌊 LinguaFlow - Your AI English Partner")

# 1. Carrega variáveis de ambiente
load_dotenv()

# Garante que a chave da API esteja disponível nas variáveis de ambiente (para Streamlit Cloud)
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if not os.getenv("GROQ_API_KEY"):
    st.error("Erro: GROQ_API_KEY não encontrada. Verifique o arquivo .env ou os Secrets do Streamlit.")
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
        model_name="llama-3.1-8b-instant"
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
try:
    audio = mic_recorder(
        start_prompt="🎤 Speak Now",
        stop_prompt="⏹ Stop",
        key='recorder'
    )
except Exception as e:
    st.error("⚠️ Erro ao inicializar o microfone. Verifique as permissões do navegador.")
    audio = None

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

# Barra lateral com ferramentas de estudo
with st.sidebar:
    st.header("Study Tools")
    if st.button("📅 Generate Weekly Plan"):
        processar_resposta("Based on our conversation so far, please create a personalized weekly study plan for me. Identify my weak points and interests from our chat, and suggest specific activities for each day of the week (Monday to Sunday) to improve my English. For each day, recommend a specific YouTube video topic or search query.")
        st.rerun()

    if st.button("📺 Recommend YouTube Videos"):
        processar_resposta("Based on our recent topics and my mistakes, please recommend 3 specific YouTube videos or channels that would help me improve. For each recommendation, explain why it's useful for me.")
        st.rerun()

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
                # Cria o arquivo temporário e fecha imediatamente para evitar conflito no Windows
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp_filename = tmp.name
                
                tts.save(tmp_filename)
                with open(tmp_filename, "rb") as f:
                    audio_bytes = f.read()
                
                st.audio(audio_bytes, format="audio/mp3")
                os.remove(tmp_filename)
            except Exception as e:
                st.error(f"Erro no áudio: {e}")

if user_input := st.chat_input("Type your message here..."):
    processar_resposta(user_input)
    st.rerun()