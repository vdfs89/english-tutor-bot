# 🌊 LinguaFlow - English Tutor AI

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Online-brightgreen?style=flat-square&logo=github)](https://vdfs89.github.io/english-tutor-bot/)
[![Build Status](https://github.com/vdfs89/english-tutor-bot/actions/workflows/manual.yml/badge.svg)](https://github.com/vdfs89/english-tutor-bot/actions/workflows/manual.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> Your 24/7 AI English Learning Partner. Practice conversation, get instant grammar corrections, and build your confidence in English—one chat at a time. 🚀

---

## 🎯 Overview

**LinguaFlow** is an AI-powered English tutor that uses advanced language models to provide real-time conversational practice with instant feedback. Whether you're preparing for a job interview, planning a trip, or simply want to improve your daily speaking skills, LinguaFlow offers a judgment-free environment to practice and learn.

### ✨ Key Features

- 🤖 **AI Tutor**: Conversational practice with a friendly, intelligent AI powered by Groq's Llama 3
- 🎯 **Real-time Corrections**: Instant feedback on grammar, vocabulary, and pronunciation
- 🎤 **Voice Interaction**: Practice speaking and listening with Speech-to-Text & Text-to-Speech capabilities
- 📚 **Personalized Learning**: Adapts to your conversation level and learning goals
- 🌐 **Web-based**: Access from anywhere with a browser
- ⚡ **Fast & Responsive**: Powered by cutting-edge AI models for quick responses

---

## 🚀 Quick Start

### Live Demo

🔗 **Visit the web version:** [https://vdfs89.github.io/english-tutor-bot/](https://vdfs89.github.io/english-tutor-bot/)

### Local Installation

#### Prerequisites

- Python 3.8 or higher
- pip or conda
- Groq API Key (get it free at [console.groq.com](https://console.groq.com))

#### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/vdfs89/english-tutor-bot.git
   cd english-tutor-bot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**

   ```bash
   streamlit run interface_streamlit.py
   ```

The app will open at `http://localhost:8501`

---

## 🛠️ Technologies

| Technology | Purpose |
|----------|--------|
| **Python** | Backend language |
| **Streamlit** | Web framework for the interactive UI |
| **Groq API** | LLM provider (Llama 3 & Whisper) |
| **LangChain** | LLM orchestration & chain management |
| **GitHub Pages** | Static site hosting |

---

## 📁 Project Structure

```text
english-tutor-bot/
├── interface_streamlit.py      # Main Streamlit app
├── conversacao_ingles.py       # Conversation logic
├── exemplo_groq.py            # Groq API usage examples
├── exemplo_transcricao_groq.py # Audio transcription examples
├── exemplo_completo_audio_resumo.py # Complete audio example
├── index.html                 # Landing page for GitHub Pages
├── config.toml               # Streamlit configuration
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .github/
│   └── workflows/
│       └── static.yml       # GitHub Pages deployment workflow
└── README.md                # This file
```

---

## 🔑 Getting Your API Keys

### Groq API

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Create an API key
4. Add it to your `.env` file:

   ```env
   GROQ_API_KEY=your_key_here
   ```

---

## 📚 Usage Examples

### Basic Conversation

```python
from interface_streamlit import start_conversation

start_conversation()
```

### With Voice Input

The app supports voice input for more natural practice. Simply click the microphone icon and speak.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Roadmap

- [ ] Mobile app version (Flutter/React Native)
- [ ] Advanced pronunciation feedback with audio analysis
- [ ] Spaced repetition system for vocabulary
- [ ] User profile & learning progress dashboard
- [ ] Interactive exercises & quizzes
- [ ] Multiple language support
- [ ] Community features (discussion boards)

---

## 💡 Tips for Best Results

1. **Be conversational**: The AI responds best to natural, flowing conversation
2. **Ask for corrections**: Request specific feedback on grammar or pronunciation
3. **Practice consistently**: Regular short sessions are better than occasional long ones
4. **Vary topics**: Talk about different subjects to build versatile vocabulary
5. **Use voice**: Practice speaking out loud for better pronunciation improvement

---

## 🐛 Troubleshooting

### "API key not found"

- Make sure your `.env` file is in the root directory
- Check that `GROQ_API_KEY=` is set correctly
- Restart the Streamlit app after updating the `.env` file

### "Connection timeout"

- Check your internet connection
- Verify your Groq API key is valid
- Try again in a few moments

### "Intl.v8BreakIterator is deprecated"

- This warning appears in the browser console when using Flutter SDK versions older than 3.22.
- **Fix:** Update your Flutter SDK locally:
  `flutter upgrade`

---

## 📧 Support

For issues, questions, or suggestions, please:

- Open an [Issue](https://github.com/vdfs89/english-tutor-bot/issues)
- Check existing discussions
- Review the [Discussions](https://github.com/vdfs89/english-tutor-bot/discussions) tab

---

## 👨‍💻 Author

**vdfs89** - Full-stack developer passionate about language learning and AI

- GitHub: [@vdfs89](https://github.com/vdfs89)
- Project: [english-tutor-bot](https://github.com/vdfs89/english-tutor-bot)

---

## 🌟 Show Your Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🔀 Forking and contributing
- 📢 Sharing with others
- 💬 Providing feedback

---

Made with ❤️ for English learners everywhere
