# 🔍 AI Research Agent

A powerful, multi-source research automation platform built with Python, Streamlit, and Google Gemini AI. This application combines Wikipedia, web search, and AI analysis to provide comprehensive research results with a beautiful web interface.

## ✨ Features

- **🤖 AI-Powered Analysis** - Google Gemini 1.5 Flash for intelligent summarization
- **📚 Multi-Source Research** - Wikipedia API + DuckDuckGo web search
- **🎨 Modern Web Interface** - Responsive Streamlit dashboard
- **📊 Real-time Analytics** - Live stats and metrics
- **💾 Auto-Save** - Results automatically stored locally
- **📥 Export Options** - Download as Markdown or JSON
- **🔧 Structured Output** - Clean, organized data with Pydantic models

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 🛠️ Technology Stack

- **Backend:** Python 3.12
- **AI/ML:** Google Gemini API, LangChain
- **Web Framework:** Streamlit
- **Data Processing:** Pydantic, JSON parsing
- **APIs:** Wikipedia API, DuckDuckGo Search API
- **Styling:** Custom CSS, responsive design

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-research-agent.git
   cd ai-research-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp sample.env .env
   # Edit .env and add your Google API key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔑 API Keys Required

- **Google Gemini API Key** - Get from [Google AI Studio](https://aistudio.google.com/)

## 📱 Usage

1. **Web Interface** - Open `http://localhost:8501` in your browser
2. **Enter API Key** - Add your Google API key in the sidebar
3. **Research Topic** - Type any topic you want to research
4. **Click Research** - Watch the AI agent gather and analyze information
5. **View Results** - See structured research with sources and tools used
6. **Download** - Export results as Markdown or JSON files

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │────│  Research Agent  │────│   AI Analysis   │
│   (Streamlit)   │    │   (LangChain)    │    │  (Google Gemini)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  User Input     │    │  Data Sources    │    │  Structured     │
│  & Results      │    │  Wikipedia + Web │    │  Output + Save  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
ai-research-agent/
├── app.py                 # Main Streamlit web application
├── main.py               # Command-line version
├── tools.py              # Research tools (Wikipedia, Web search, Save)
├── requirements.txt      # Python dependencies
├── sample.env           # Environment variables template
├── research_output.txt  # Generated research results
└── README.md           # This file
```

## 🎯 Key Features Explained

### Multi-Source Research Pipeline
- **Wikipedia Search** - Academic and historical information
- **Web Search** - Current, up-to-date information
- **AI Synthesis** - Intelligent combination and summarization

### Professional Web Interface
- **Responsive Design** - Works on desktop and mobile
- **Real-time Stats** - Word count, sources, tools used
- **Export Functionality** - Download results in multiple formats
- **Error Handling** - User-friendly error messages

### Structured Data Output
- **Pydantic Models** - Type-safe data structures
- **JSON Parsing** - Robust response processing
- **File Management** - Automatic result archiving

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click
4. Add environment variables in Streamlit Cloud settings

### Other Platforms
- **Heroku** - Add `Procfile` and deploy
- **Railway** - Connect GitHub and deploy
- **Render** - Web service deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [Your Portfolio](https://yourportfolio.com)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [LangChain](https://langchain.com/) for AI agent development
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for academic data

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-research-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-research-agent?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/ai-research-agent)
![GitHub license](https://img.shields.io/github/license/yourusername/ai-research-agent)

---

⭐ **Star this repository if you found it helpful!**