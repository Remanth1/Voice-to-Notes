# 📝 Lecture Voice-to-Notes Generator

A minimalist, AI-powered study buddy that automatically converts your lecture audio recordings into structured notes, functional summaries, and study flashcards.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)

---

## 🚀 Features

- **Blazing Fast Transcription**: Uses Hugging Face's `distil-whisper` to accurately and quickly convert spoken lectures into raw text, chunking large files to prevent memory overload.
- **Intelligent Summarization**: Uses Facebook's `BART-large-cnn` model to condense pages of transcript into structured, readable notes.
- **Auto-Generated Flashcards**: Automatically extracts key concepts from the summary to generate Q&A flashcards using Google's `FLAN-T5` model.
- **Minimalist Interface**: Features a custom, distraction-free UI with subtle 2D geometric patterns.
- **100% Free & Local**: Runs entirely locally on your machine using open-source models. No API keys or paid subscriptions required.

---

## 🛠️ Installation Requirements

### 1. System Dependencies
This application requires **FFmpeg** to extract and process audio streams.
- The app uses `imageio-ffmpeg` to automatically download a local binary for you.
- *Optional*: You can install FFmpeg system-wide (e.g., via `winget install Gyan.FFmpeg` on Windows or `brew install ffmpeg` on macOS).

### 2. Python Dependencies
Create a virtual environment (optional but recommended) and install the requirements:

```bash
pip install -U -r requirements.txt
```

---

## 💻 Usage

1. Start the Streamlit server:
```bash
streamlit run app.py
```
2. Open your browser to `http://localhost:8501`.
3. Drag and drop your lecture audio file (`.mp3`, `.wav`, or `.m4a`).
4. Click **Process Audio** and wait for the AI to generate your study materials.
5. Download your Notes, Transcripts, or Flashcards directly from the interface tabs.

---

## 🧠 Models Used
*   **Speech-to-Text**: `distil-whisper/distil-small.en`
*   **Summarization**: `facebook/bart-large-cnn`
*   **Text Generation (Flashcards)**: `google/flan-t5-base`

*Note: On your very first run, these models will be automatically downloaded to your local Hugging Face cache. This may take a few minutes depending on your internet connection.*
