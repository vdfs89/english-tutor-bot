# 🚀 PRÓXIMA FASE: FastAPI + Render Deploy

> Plano Estratégico para Migrar do Streamlit para FastAPI Backend Profissional

## 🌟 Visão Geral

O projeto LinguaFlow será transformado em uma arquitetura profissional:

```
Antes (Monolítico):
Streamlit UI + Lógica IA (mesmo servidor)

Depois (Desacoplado):
퉑 Frontend: Flutter + HTML/CSS (web)
퉑 Backend: FastAPI (API RESTful)
퉑 Hospedagem: Render (free tier)
```

## 📄 Checklist Prático Completo

### Passo 1: Preparar Environment (Semana 1)

- [ ] Criar arquivo `api.py` na raiz do projeto
- [ ] Atualizar `requirements.txt` com dependências FastAPI:

  ```txt
  fastapi==0.104.0
  uvicorn[standard]==0.24.0
  pydantic==2.5.0
  python-multipart==0.0.6
  python-dotenv==1.0.0
  # Suas libs de IA
  groq==0.4.1
  langchain==0.1.0
  ```

- [ ] Testar `pip install -r requirements.txt` localmente

### Passo 2: Migrar Lógica para FastAPI (Semana 1)

**Estrutura básica de `api.py`:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LinguaFlow", version="0.1.0")

# CORS - Permitir requisições do Flutter e HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mudar para URLs específicas em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "LinguaFlow API is running"}

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """Process chat message and return AI response."""
    # Sua lógica de IA aqui (do conversacao_ingles.py ou similar)
    response = get_ai_response(request.message)
    return ChatResponse(response=response, session_id=request.session_id)

def get_ai_response(message: str) -> str:
    """Sua função de IA existente."""
    # Migrar lógica do conversacao_ingles.py
    # ou integrar com Groq/LangChain
    return "Response from AI"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

- [ ] Implementar `get_ai_response()` com sua lógica
- [ ] Adicionar modelo Pydantic para validação
- [ ] Configurar CORS para Flutter/HTML

### Passo 3: Testar Localmente (Semana 1)

- [ ] Executar: `uvicorn api:app --reload`
- [ ] Acessar: <http://127.0.0.1:8000/docs> (Swagger UI)
- [ ] Testar endpoint POST /chat
- [ ] Verificar resposta JSON

**Teste via curl:**

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

### Passo 4: Deploy no Render (Semana 2)

1. **Preparar GitHub:**
   - [ ] Fazer commit de `api.py` e `requirements.txt`
   - [ ] Push para repositório GitHub

2. **Criar Web Service no Render:**
   - [ ] Ir para <https://dashboard.render.com>
   - [ ] Criar novo "Web Service"
   - [ ] Conectar repositório GitHub
   - [ ] Configurar:

     ```
     Name: linguaflow-api
     Runtime: Python 3
     Branch: main
     Root Directory: . (ou vazio)
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
     ```

3. **Variáveis de Ambiente:**
   - [ ] No dashboard do Render, adicionar:

     ```
     GROQ_API_KEY=seu_api_key
     OPENAI_API_KEY=seu_api_key (se usar)
     ```

   - [ ] NUNCA hardcode essas chaves no código

4. **Deploy:**
   - [ ] Render fará deploy automático
   - [ ] Copiar URL final: `https://linguaflow-api-xxxx.onrender.com`
   - [ ] Testar via Postman ou curl

### Passo 5: Integrar Flutter (Semana 2-3)

**Em `lib/services/api_service.dart`:**

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String apiUrl = 'https://linguaflow-api-xxxx.onrender.com';

  static Future<String> sendMessage(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': message,
          'session_id': 'default',
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(utf8.decode(response.bodyBytes));
        return data['response'];
      } else {
        return 'Erro na conexão';
      }
    } catch (e) {
      return 'Erro: $e';
    }
  }
}
```

- [ ] Adicionar `http` package: `flutter pub add http`
- [ ] Integrar `ApiService` na tela de chat
- [ ] Substituir lógica local por chamadas à API
- [ ] Testar com app rodando

### Passo 6: Landing Page (Semana 3)

- [ ] Restaurar 3 cards no `index.html`:
  1. Card Azul: Flutter App (Em Breve)
  2. Card Vermelho: Streamlit Web
  3. Card Python: GitHub Source

## ⚠️ Pontos Importantes

### Cold Start

- Render dorme após 15 min inatividade
- Primeira requisição pode demorar ~50 segundos
- 📝 Solução: Ping automático a cada 10 min

### CORS

- Em desenvolvimento: `allow_origins=["*"]`
- Em produção: especificar URLs exatas

  ```python
  allow_origins=[
      "https://linguaflow.com",
      "https://meu-app.onrender.com"
  ]
  ```

### Variáveis de Ambiente

```python
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

### Encoding UTF-8 (Flutter)

```dart
final data = jsonDecode(utf8.decode(response.bodyBytes));
```

## 📄 Cronograma Sugerido

**Semana 1 (Hoje-6 Jan):**

- Passo 1: Environment
- Passo 2: Migrar lógica
- Passo 3: Testes locais

**Semana 2 (7-13 Jan):**

- Passo 4: Deploy Render
- Passo 5: Início integração Flutter

**Semana 3 (14-20 Jan):**

- Passo 5: Completar Flutter
- Passo 6: Landing page
- Testes end-to-end

## 📁 Arquivos Principais

```
✅ api.py (novo)
✅ requirements.txt (atualizado)
✅ .env (local)
✅ lib/services/api_service.dart (novo)
✅ index.html (atualizado com 3 cards)
```

## 🚀 Resultado Final

- API profissional rodando em `https://linguaflow-api.onrender.com`
- Flutter conectado à API
- HTML/Web acessando API
- Landing page com 3 opções
- Projeto pronto para escalar!

---

**Data**: 27/12/2025
**Status**: Planejamento Completo
**Próxima Ação**: Começar Passo 1
