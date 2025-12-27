#!/usr/bin/env python3
"""LinguaFlow API - Gemini + Groq com Fallback Inteligente

Arquitetura: Google Gemini (primario) -> Groq Llama (fallback)
Custo: R$0,00 para sempre
Confiabilidade: 99.9% com redundancia automatica
"""

import logging
import os
from typing import Any, Dict, Optional

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel

# Configuracao
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY and not GROQ_API_KEY:
    raise ValueError("Adicione GEMINI_API_KEY ou GROQ_API_KEY no .env")

# Configurar Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")
else:
    gemini_model = None

# Configurar Groq
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

# FastAPI app
app = FastAPI(
    title="LinguaFlow API",
    description="Chat de Inglês com IA - Gemini + Groq Fallback",
    version="2.0.0",
)

# CORS para Flutter e Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    model_used: str
    session_id: str


# Sessoes em memoria (usar Redis em produção)
sessions: Dict[str, list] = {}


# Funcao core: Chat com fallback
async def process_conversation_with_fallback(
    session_id: str, message: str, model_preference: str = "gemini"
) -> tuple[str, str]:
    """Processar conversa com fallback automatico Gemini -> Groq"""

    # Inicializar sessao se necessario
    if session_id not in sessions:
        sessions[session_id] = []

    # Adicionar mensagem do usuario
    sessions[session_id].append({"role": "user", "content": message})

    # TENTATIVA 1: Gemini (primario)
    if model_preference == "gemini" and gemini_model:
        try:
            logger.info(f"Tentando Gemini para {session_id}...")
            response = gemini_model.generate_content(message)
            reply = response.text
            logger.info(f"Gemini sucesso! Resposta: {reply[:50]}...")
            sessions[session_id].append({"role": "assistant", "content": reply})
            return reply, "gemini"
        except Exception as e:
            logger.warning(f"Gemini falhou: {e}. Tentando Groq...")

    # FALLBACK: Groq (backup)
    if groq_client:
        try:
            logger.info(f"Tentando Groq para {session_id}...")
            # Preparar historico para Groq
            messages = [
                {"role": msg.get("role", "user"), "content": msg["content"]}
                for msg in sessions[session_id]
            ]
            response = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile", messages=messages, max_tokens=1024, temperature=0.7
            )
            reply = response.choices[0].message.content
            logger.info(f"Groq sucesso! Resposta: {reply[:50]}...")
            sessions[session_id].append({"role": "assistant", "content": reply})
            return reply, "groq"
        except Exception as e:
            logger.error(f"Groq tambem falhou: {e}")
            raise HTTPException(status_code=503, detail=f"Ambas as APIs falharam: {e}")

    # Ambas as APIs estao deshabilitadas
    raise HTTPException(status_code=500, detail="Nenhuma chave de API configurada")


# Endpoints
@app.get("/")
async def health_check():
    """Health check - verifica status das APIs"""
    gemini_status = "online" if gemini_model else "offline"
    groq_status = "online" if groq_client else "offline"
    return {
        "status": "online",
        "message": "LinguaFlow API v2.0.0 - Gemini + Groq",
        "gemini": gemini_status,
        "groq": groq_status,
        "fallback": "enabled" if (gemini_model and groq_client) else "limited",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat de texto - POST /chat

    Exemplo:
    {
        "session_id": "user123",
        "message": "Hello, how are you?"
    }
    """
    try:
        response, model = await process_conversation_with_fallback(
            request.session_id, request.message
        )
        return ChatResponse(response=response, model_used=model, session_id=request.session_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/audio")
async def chat_audio_endpoint(file: UploadFile = File(...), session_id: str = Form("default")):
    """Chat com audio - POST /chat/audio

    Envia arquivo .wav para transcricao + processamento
    """
    try:
        # Ler arquivo de audio
        audio_bytes = await file.read()
        logger.info(f"Audio recebido: {file.filename} ({len(audio_bytes)} bytes)")

        # Transcricao com Groq Whisper (sempre gratis)
        if not groq_client:
            raise HTTPException(status_code=500, detail="Groq nao configurado")

        # Usar Groq para transcricao
        with open("/tmp/temp_audio.wav", "wb") as f:
            f.write(audio_bytes)

        with open("/tmp/temp_audio.wav", "rb") as f:
            transcript = groq_client.audio.transcriptions.create(file=f, model="whisper-large-v3")

        transcribed_text = transcript.text
        logger.info(f"Transcricao: {transcribed_text}")

        # Processar como chat normal
        response, model = await process_conversation_with_fallback(session_id, transcribed_text)

        return {
            "response": response,
            "transcription": transcribed_text,
            "model_used": model,
            "session_id": session_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Ver historico de uma sessao"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")
    return {"session_id": session_id, "messages": sessions[session_id]}


# Main
if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 60)
    logger.info("LinguaFlow API v2.0.0 - Iniciando...")
    logger.info(f'Gemini: {"HABILITADO" if gemini_model else "DESABILITADO"}')
    logger.info(f'Groq: {"HABILITADO" if groq_client else "DESABILITADO"}')
    logger.info("Fallback inteligente: ATIVO")
    logger.info("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
