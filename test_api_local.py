#!/usr/bin/env python3
"""Passo 3: Script para testar a API FastAPI localmente"""

import json
from typing import Dict

import requests

# Configuracao
BASE_URL = "http://localhost:8000"
SESSION_ID = "test_session_001"


def test_health_check():
    """Teste de health check - verificar se API esta online"""
    print("\n[1] Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False


def test_chat_endpoint(message: str) -> Dict:
    """Teste do endpoint /chat - conversa de texto"""
    print(f"\n[2] Testando Chat Endpoint...")
    print(f"Mensagem: {message}")

    payload = {"session_id": SESSION_ID, "message": message}

    try:
        response = requests.post(
            f"{BASE_URL}/chat", json=payload, headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except Exception as e:
        print(f"Erro: {e}")
        return {}


def main():
    """Executar todos os testes"""
    print("=" * 60)
    print("PASSO 3: TESTES LOCAIS DA API FastAPI")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    print("\nPre-requisitos:")
    print("1. Executar: python api.py")
    print("2. Aguardar: 'Application startup complete'")
    print("3. Executar este script em outro terminal")
    print("=" * 60)

    health_ok = test_health_check()

    if health_ok:
        test_chat_endpoint("Ola! Como voce esta?")
        test_chat_endpoint("Me explique sobre FastAPI")
        print("\n" + "=" * 60)
        print("TESTES CONCLUIDOS COM SUCESSO!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERRO: API nao esta respondendo")
        print("Certifique-se de executar: python api.py")
        print("=" * 60)


if __name__ == "__main__":
    main()
