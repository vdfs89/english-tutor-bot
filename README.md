# LinguaFlow - English Tutor AI

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Online-brightgreen?style=flat-square&logo=github)](https://vdfs89.github.io/english-tutor-bot/)
[![Streamlit App](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://linguaflow.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**[English](#-linguaflow-english-tutor-ai) | [Portugues](#-linguaflow-tutor-de-ingles-com-ia)**

---

## 🌊 LinguaFlow - English Tutor AI

> Your 24/7 AI English Learning Partner. Practice conversation, get instant grammar corrections, and build your confidence in English—one chat at a time. 🚀

### Overview

**LinguaFlow** is an AI-powered English tutor that uses advanced language models to provide real-time conversational practice with instant feedback. Whether you're preparing for a job interview, planning a trip, or simply want to improve your daily speaking skills, LinguaFlow offers a judgment-free environment to practice and learn.

### Key Features

- 🤖 **AI Tutor**: Conversational practice with intelligent AI powered by Groq's Llama 3
- 🎯 **Real-time Corrections**: Instant feedback on grammar, vocabulary, and pronunciation
- 🎤 **Voice Interaction**: Practice speaking with Speech-to-Text & Text-to-Speech
- 📚 **Personalized Learning**: Adapts to your conversation level
- 🌐 **Web-Based**: Access from anywhere with a browser
- ⚡ **Fast & Responsive**: Powered by cutting-edge AI models

### Quick Start

#### Live Demo
🔗 **[Visit LinguaFlow](https://linguaflow.streamlit.app)**

#### Local Installation

**Prerequisites:**
- Python 3.8+
- pip or conda
- Groq API Key (free at [console.groq.com](https://console.groq.com))

**Steps:**

```bash
# Clone repository
git clone https://github.com/vdfs89/english-tutor-bot.git
cd english-tutor-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run the application
streamlit run interface_streamlit.py
```

### Technologies

| Technology | Purpose |
|----------|--------|
| **Python** | Backend language |
| **Streamlit** | Web framework |
| **Groq API** | LLM provider (Llama 3, Whisper) |
| **LangChain** | LLM orchestration |
| **GitHub Pages** | Static site hosting |

### Project Structure

```
english-tutor-bot/
├── interface_streamlit.py      # Main application
├── conversacao_ingles.py       # Conversation logic
├── exemplo_groq.py            # API examples
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── index.html                # Landing page
├── README.md                 # This file
└── .github/workflows/        # CI/CD
```

### Getting API Keys

**Groq API:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create an API key
4. Add to `.env`: `GROQ_API_KEY=your_key`

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

### License

MIT License - see [LICENSE](LICENSE) file

### Roadmap

- [ ] Mobile app (Flutter/React Native)
- [ ] Advanced pronunciation analysis
- [ ] Vocabulary spaced repetition system
- [ ] User progress dashboard
- [ ] Interactive exercises & quizzes
- [ ] Multiple language support

### Support

- [Open an Issue](https://github.com/vdfs89/english-tutor-bot/issues)
- [Check Discussions](https://github.com/vdfs89/english-tutor-bot/discussions)

### Author

**vdfs89** - Full-stack developer passionate about language learning & AI
- GitHub: [@vdfs89](https://github.com/vdfs89)
- Portfolio: [vdfs89.github.io](https://vdfs89.github.io)

### Show Your Support

If you find this helpful:
- ⭐ Star the repository
- 🔀 Fork and contribute
- 📢 Share with others
- 💬 Provide feedback

---

## 🌊 LinguaFlow - Tutor de Ingles com IA

> Seu parceiro de IA para fluencia em ingles 24/7. Pratique conversacao, receba correcoes instantaneas e ganhe confianca no ingles—uma conversa por vez. 🚀

### Visao Geral

**LinguaFlow** eh um tutor de ingles powered by IA que usa modelos de linguagem avancados para oferecer pratica conversacional em tempo real com feedback instantaneo. Se voce esta se preparando para uma entrevista de emprego, um viagem, ou simplesmente quer melhorar suas habilidades diarias de fala, LinguaFlow oferece um ambiente livre de julgamentos para praticar e aprender.

### Principais Funcionalidades

- 🤖 **Tutor IA**: Pratica de conversacao com IA inteligente powered by Groq Llama 3
- 🎯 **Correcoes em Tempo Real**: Feedback instantaneo sobre gramatica, vocabulario e pronuncia
- 🎤 **Interacao por Voz**: Pratique fala com Speech-to-Text & Text-to-Speech
- 📚 **Aprendizado Personalizado**: Adapta-se ao seu nivel de fluencia
- 🌐 **Baseado na Web**: Acesse de qualquer lugar com navegador
- ⚡ **Rapido e Responsivo**: Powered by modelos de IA de ponta

### Comece Agora

#### Demo ao Vivo
🔗 **[Visite LinguaFlow](https://linguaflow.streamlit.app)**

#### Instalacao Local

**Requisitos:**
- Python 3.8+
- pip ou conda
- Chave de API Groq (gratis em [console.groq.com](https://console.groq.com))

**Passos:**

```bash
# Clone o repositorio
git clone https://github.com/vdfs89/english-tutor-bot.git
cd english-tutor-bot

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale dependencias
pip install -r requirements.txt

# Configure variaveis de ambiente
echo "GROQ_API_KEY=sua_chave_aqui" > .env

# Execute a aplicacao
streamlit run interface_streamlit.py
```

### Tecnologias

| Tecnologia | Proposito |
|----------|----------|
| **Python** | Linguagem backend |
| **Streamlit** | Framework web |
| **Groq API** | Provedor LLM (Llama 3, Whisper) |
| **LangChain** | Orquestracao LLM |
| **GitHub Pages** | Hospedagem de site estatico |

### Estrutura do Projeto

```
english-tutor-bot/
├── interface_streamlit.py      # Aplicacao principal
├── conversacao_ingles.py       # Logica de conversacao
├── exemplo_groq.py            # Exemplos de API
├── requirements.txt           # Dependencias
├── .env.example              # Template de ambiente
├── index.html                # Landing page
├── README.md                 # Este arquivo
└── .github/workflows/        # CI/CD
```

### Obtendo Chaves de API

**Groq API:**
1. Visite [console.groq.com](https://console.groq.com)
2. Cadastre-se gratuitamente
3. Crie uma chave de API
4. Adicione ao `.env`: `GROQ_API_KEY=sua_chave`

### Contribuindo

Contribuicoes sao bem-vindas! Por favor:
1. Faca um fork do repositorio
2. Crie uma branch com sua feature
3. Faca commit das mudancas
4. Faca push para sua fork
5. Abra um Pull Request

### Licenca

Licenca MIT - veja arquivo [LICENSE](LICENSE)

### Roadmap

- [ ] App mobile (Flutter/React Native)
- [ ] Analise avancada de pronuncia
- [ ] Sistema de repeticao espacada de vocabulario
- [ ] Dashboard de progresso do usuario
- [ ] Exercicios interativos e quizzes
- [ ] Suporte para multiplos idiomas

### Suporte

- [Abra uma Issue](https://github.com/vdfs89/english-tutor-bot/issues)
- [Verifique Discussoes](https://github.com/vdfs89/english-tutor-bot/discussions)

### Autor

**vdfs89** - Desenvolvedor full-stack apaixonado por aprendizado de idiomas e IA
- GitHub: [@vdfs89](https://github.com/vdfs89)
- Portfolio: [vdfs89.github.io](https://vdfs89.github.io)

### Mostre seu Apoio

Se achou util:
- ⭐ Coloque uma estrela no repositorio
- 🔀 Faca um fork e contribua
- 📢 Compartilhe com outros
- 💬 Envie feedback

---

**Made with LOVE for English learners everywhere / Feito com AMOR para aprendizes de ingles em todo o mundo**
