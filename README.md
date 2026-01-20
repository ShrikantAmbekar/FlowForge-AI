# ⚡ FlowForge AI

> Transform Business Requirements Documents into beautiful Eraser.io flowcharts using AI

![FlowForge AI](https://img.shields.io/badge/AI-Powered-667eea?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## 🚀 Features

- **📄 BRD to Flowchart** - Paste your Business Requirements Document content
- **🤖 AI-Powered** - Uses Google Gemini AI for intelligent diagram generation
- **⚡ Instant Generation** - Get Eraser.io compatible code in seconds
- **🎨 Professional UI** - Modern, dark-themed interface

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd FlowDiagrams
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Configure your API key:**
   - Click on "🔑 Configure API Key" 
   - Enter your Google Gemini API key

3. **Generate flowcharts:**
   - Paste your BRD document content in the text area
   - (Optional) Add any additional context or instructions
   - Click "⚡ Generate Flowchart Code"

4. **Use the generated code:**
   - Copy the generated Eraser.io code
   - Go to [Eraser.io](https://app.eraser.io)
   - Paste the code to view your flowchart

## 📁 Project Structure

```
FlowDiagrams/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## 🎨 Customization

The app uses a modern dark theme with purple/violet accents. You can customize the appearance by modifying:
- CSS styles in `app.py`
- Theme settings in `.streamlit/config.toml`

## 🔑 API Key Security

- Your API key is stored only in session state
- It's never persisted or logged
- Consider using environment variables for production

## 📝 License

MIT License - Feel free to use and modify as needed.

---

<p align="center">
  Built with ❤️ using Streamlit & Google Gemini AI
</p>

