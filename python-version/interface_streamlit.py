import io
import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
from groq import Groq
from gtts import gTTS
from langchain_groq import ChatGroq
from streamlit_mic_recorder import mic_recorder

# Configuração da Página
st.set_page_config(page_title="LinguaFlow AI", page_icon="🌊", layout="wide")
st.title("🌊 LinguaFlow - Your AI English Partner")

# 1. Carrega variáveis de ambiente
load_dotenv()

# Garante que a chave da API esteja disponível nas variáveis de ambiente (para Streamlit Cloud)
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not os.getenv("GROQ_API_KEY"):
    st.error(
        "Erro: GROQ_API_KEY não encontrada. Verifique o arquivo .env ou os Secrets do Streamlit."
    )
    st.stop()

# Barra lateral com configurações (Definida antes para usar as variáveis na inicialização)
with st.sidebar:
    st.header("Settings")
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=1,
    )
    roleplay_mode = st.selectbox(
        "Roleplay Persona",
        [
            "Default (Tutor)",
            "Waiter (Restaurant)",
            "Job Interviewer",
            "Travel Agent",
            "Doctor",
            "Shop Assistant",
            "Immigration Officer",
            "Hotel Receptionist",
            "Taxi Driver",
            "Tech Support",
        ],
        index=0,
    )
    start_roleplay = st.button("▶ Start Roleplay")
    enable_audio = st.toggle("🔊 Enable Audio Response", value=False)
    st.divider()

# 2. Inicializa o estado da sessão (Histórico e Modelo)
difficulty_prompts = {
    "Beginner": "Use simple vocabulary, short sentences, and be very encouraging.",
    "Intermediate": "Use standard vocabulary and grammar. Introduce some common idioms.",
    "Advanced": "Use sophisticated vocabulary, complex grammar, and idioms. Speak like a native speaker.",
}

roleplay_prompts = {
    "Default (Tutor)": "You are a friendly English tutor. Your goal is to help the user practice English conversation.",
    "Waiter (Restaurant)": "You are a waiter at a restaurant. The user is a customer. "
    "Take their order, make recommendations, and simulate a dining experience.",
    "Job Interviewer": "You are a hiring manager conducting a job interview. "
    "Ask standard interview questions and evaluate the user's responses professionally.",
    "Travel Agent": "You are a travel agent. Help the user plan a trip, discussing destinations, flights, and accommodation.",
    "Doctor": "You are a doctor. The user is a patient describing symptoms. Ask diagnostic questions and give medical advice.",
    "Shop Assistant": "You are a sales assistant in a store. "
    "Help the user find products, discuss prices, and handle the purchase.",
    "Immigration Officer": "You are an immigration officer at border control. "
    "Ask the user about their trip purpose, duration, and accommodation in a formal tone.",
    "Hotel Receptionist": "You are a hotel receptionist. "
    "Check the user in, discuss room preferences, and explain hotel amenities.",
    "Taxi Driver": "You are a chatty taxi driver. "
    "Make small talk about the city, weather, or traffic while driving the user to their destination.",
    "Tech Support": "You are a tech support agent. "
    "Help the user troubleshoot a technical problem with their computer or internet.",
}

system_prompt = (
    f"{roleplay_prompts[roleplay_mode]} "
    "Speak only in English. If the user makes a grammatical error, gently correct them inside your response "
    "using **bold text** for the corrected part, but keep the conversation flowing naturally. "
    "At the end of your response, provide a separate list explaining the reason for any grammatical errors found. "
    f"Current level: {difficulty}. {difficulty_prompts[difficulty]}"
)

if "messages" not in st.session_state:
    st.session_state.messages = [("system", system_prompt)]
else:
    # Atualiza o prompt do sistema se o nível de dificuldade mudar
    st.session_state.messages[0] = ("system", system_prompt)

if "chat" not in st.session_state:
    st.session_state.chat = ChatGroq(temperature=0.6, model="llama-3.1-8b-instant")

if "display_offset" not in st.session_state:
    st.session_state.display_offset = 0

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = b""


# Função para processar a resposta da IA e gerar áudio
def processar_resposta(user_text):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append(("human", user_text))

    # Gera resposta da IA
    resposta = st.session_state.chat.invoke(st.session_state.messages)
    st.session_state.messages.append(("ai", resposta.content))

    return resposta.content


if start_roleplay:
    processar_resposta(
        "Please start the roleplay now. Introduce yourself in character based on your persona and ask me a question to begin the interaction."
    )
    st.rerun()

# 4. Área de Entrada de Voz (Movido para o topo da página principal)
st.write("### Voice Input")
# Componente de gravação compatível com navegadores web
try:
    audio = mic_recorder(start_prompt="🎤 Speak Now", stop_prompt="⏹ Stop", key="recorder")
except Exception:
    st.error("⚠️ Erro ao inicializar o microfone. Verifique as permissões do navegador.")
    audio = None

if audio:
    # Evita processar o mesmo áudio múltiplas vezes (loop de rerun)
    if audio["bytes"] != st.session_state.last_audio_bytes:
        st.session_state.last_audio_bytes = audio["bytes"]

        with st.spinner("Transcribing..."):
            try:
                # Transcreve usando Groq
                client = Groq()

                # Otimização: Usar BytesIO e modelo Distil (mais rápido)
                audio_file = io.BytesIO(audio["bytes"])
                audio_file.name = "audio.wav"

                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3-turbo",  # Modelo rápido (substituto do distil)
                    language="en",
                )

                if transcription.text:
                    processar_resposta(transcription.text)
                    st.rerun()

            except Exception as e:
                st.error(f"Error processing audio: {e}")

# Barra lateral com ferramentas de estudo
with st.sidebar:
    st.header("Study Tools")
    if st.button("📅 Generate Weekly Plan"):
        processar_resposta(
            "Based on our conversation so far, please create a personalized weekly study plan for me. "
            "Identify my weak points and interests from our chat, and suggest specific activities for each day of the week "
            "(Monday to Sunday) to improve my English. For each day, recommend a specific YouTube video topic or search query."
        )
        st.rerun()

    if st.button("💡 Suggest Topics"):
        processar_resposta(
            f"I am currently at a {difficulty} level. Please suggest 3 interesting conversation topics suitable for my level "
            "that we could discuss right now. For each topic, provide a sample opening question to get us started."
        )
        st.rerun()

    if st.button("🇧🇷 Translate Last Response"):
        processar_resposta("Please translate your very last response into Portuguese.")
        st.rerun()

    if st.button("📺 Recommend YouTube Videos"):
        processar_resposta(
            "Based on our recent topics and my mistakes, please recommend 3 specific YouTube videos or channels "
            "that would help me improve. For each recommendation, explain why it's useful for me."
        )
        st.rerun()

    if st.button("🧹 Clear Visual History"):
        st.session_state.display_offset = len(st.session_state.messages)
        st.rerun()

    st.divider()

    st.header("📊 Your Statistics")
    user_messages = [content for role, content in st.session_state.messages if role == "human"]
    if user_messages:
        total_messages = len(user_messages)
        all_words = " ".join(user_messages).lower().split()
        total_words = len(all_words)
        unique_words = len(set(all_words))

        st.metric("Messages Sent", total_messages)
        st.metric("Total Words", total_words)
        st.metric("Unique Vocabulary", unique_words)
    else:
        st.info("Start chatting to see stats!")

    st.divider()

    # Exportar para PDF
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for role, content in st.session_state.messages:
            if role == "system":
                continue

            # Tratamento básico para caracteres não-Latin-1 (FPDF padrão requer fontes externas para UTF-8 completo)
            safe_content = content.encode("latin-1", "replace").decode("latin-1")
            role_name = "You" if role == "human" else "AI Tutor"

            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, f"{role_name}:", ln=True)

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, safe_content)
            pdf.ln(5)

        val = pdf.output(dest="S")
        return val.encode("latin-1") if isinstance(val, str) else bytes(val)

    if len(st.session_state.messages) > 1:
        pdf_bytes = create_pdf()
        st.download_button(
            label="📄 Export Chat to PDF",
            data=pdf_bytes,
            file_name="lingua_flow_history.pdf",
            mime="application/pdf",
        )

# 3. Exibe o histórico de chat
for i, (role, content) in enumerate(st.session_state.messages):
    if i < st.session_state.get("display_offset", 0):
        continue
    if role == "system":
        continue
    with st.chat_message(role):
        st.write(content)
        # Gera áudio se habilitado e for a última mensagem da IA
        if enable_audio and role == "ai" and content == st.session_state.messages[-1][1]:
            try:
                tts = gTTS(text=content, lang="en")
                # Cria o arquivo temporário e fecha imediatamente para evitar conflito no Windows
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp_filename = tmp.name

                tts.save(tmp_filename)
                with open(tmp_filename, "rb") as f:
                    audio_bytes = f.read()

                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                os.remove(tmp_filename)
            except Exception as e:
                st.error(f"Erro no áudio: {e}")

if user_input := st.chat_input("Type your message here..."):
    with st.spinner("Thinking..."):
        processar_resposta(user_input)
    st.rerun()
