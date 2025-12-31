# 🤖 Jarvis – Personal Assistant (Python)

A lightweight, local desktop assistant built in Python. It fetches Wikipedia content, summarizes it with a compact AI model, and delivers clear, concise answers via a simple GUI. Supports context-aware follow-ups and optional offline voice output—all running on CPU without browsers, APIs, or heavy dependencies.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?logo=tkinter)](https://docs.python.org/3/library/tkinter.html)

## ✨ Features

- **🖥️ Intuitive Tkinter GUI**: Clean input field, scrollable response area, and non-blocking threads for smooth interaction.
- **📚 Wikipedia-Powered Knowledge**: Reliable, structured info without scraping or browser automation.
- **🧠 Lightweight AI Summarization**: Uses DistilBART-CNN for fast, CPU-friendly text condensation.
- **🗣️ Offline Voice Output**: Optional text-to-speech with pyttsx3—no internet required.
- **🧾 Smart Follow-Ups**: Remembers context (e.g., "AI" → "AI applications" for "applications").
- **⚡ Performance & Safety**: Token truncation prevents crashes; fully offline after initial fetch.
- **🔒 Privacy-First**: No data storage, no cloud services.

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.8+ | Core scripting |
| **GUI** | Tkinter | Simple, native interface |
| **Knowledge** | wikipedia-api | Wikipedia access |
| **AI Model** | Transformers + DistilBART-CNN-6-6 | Summarization |
| **Backend** | PyTorch (CPU) | Model inference |
| **Voice** | pyttsx3 | Offline TTS |

## 📂 Project Structure

```
jarvis-python/
│
├── main.py              # Core application (GUI, logic, and helpers)
├── requirements.txt     # Dependencies
└── README.md            # This file
```

Everything is consolidated into `main.py` for simplicity and ease of modification.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/jarvis-python.git
   cd jarvis-python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (Or manually: `pip install wikipedia transformers torch pyttsx3`)

### Usage
1. Launch the app:
   ```bash
   python main.py
   ```

2. Interact in the GUI:
   - Initial query: `Artificial Intelligence` or `CORS`
   - Follow-up: `applications` or `future trends`

   The assistant will fetch, summarize, simplify, display, and (optionally) speak the response.

   Example flow:
   - Input: `AI`
   - Response: "Artificial intelligence (AI) is... [simplified summary]. What would you like to know next—examples, history, or ethics?"
   - Follow-up: `examples` → Expands to "AI examples" automatically.

## 🧠 How It Works

1. **Query Input**: User types a question in the GUI.
2. **Normalization**: Expands shorthand (e.g., "AI" → "Artificial Intelligence") and handles follow-ups via context.
3. **Fetch**: Pulls Wikipedia page content using the `wikipedia` library.
4. **Prep**: Truncates text to ~800 tokens to avoid model limits.
5. **Summarize**: DistilBART generates a concise, readable version.
6. **Polish**: Adds assistant tone, full sentences, and follow-up prompts.
7. **Output**: Displays in GUI; speaks via pyttsx3 if enabled.
8. **Reset**: Clears context on new topics or manual reset.

This flow ensures stability: no infinite loops, no overflows, and quick responses (<10s on average CPU).

## 🔐 Stability & Limitations

### Safety Measures
- **Token Limits**: Hard truncation prevents Transformer crashes.
- **Threading**: UI stays responsive during processing.
- **Offline Mode**: Voice and model run locally; only Wikipedia needs internet.

### Known Limits (Intentional)
- Single-topic focus (not a full chatbot).
- Wikipedia-dependent (may lack niche/current events).
- No voice input or multi-turn debates yet.
- CPU-only (no GPU acceleration needed).

For production, consider caching Wikipedia fetches.

## 🔮 Roadmap

- **Voice Input**: Add speech-to-text (e.g., via SpeechRecognition).
- **Modes**: Quick answers vs. detailed explanations.
- **Memory**: Persistent session history.
- **Extensions**: Local doc Q&A or custom knowledge bases.
- **Polish**: Themed GUIs or exportable summaries.
