import streamlit as st
import os
import tempfile
import imageio_ffmpeg

# Automatically add the imageio-ffmpeg binaries folder to the PATH so Whisper can access ffmpeg.exe
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

from transcriber import transcribe_audio
from summarizer import summarize_text
from quiz_generator import generate_quiz_and_flashcards

st.set_page_config(page_title="Lecture Notes", layout="centered", initial_sidebar_state="collapsed")

# Injecting Custom CSS for Minimalism
st.markdown("""
<style>
    /* Hide Streamlit components for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2D Background Pattern and Shapes */
    .stApp {
        background-color: #f8fafc;
        background-image: 
            radial-gradient(#94a3b8 1.8px, transparent 1.8px),
            radial-gradient(#94a3b8 1.8px, transparent 1.8px);
        background-size: 40px 40px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: -15vh;
        left: -10vw;
        width: 45vw;
        height: 45vw;
        border-radius: 50%;
        background-color: #cbd5e1;
        z-index: -1;
        opacity: 0.35;
    }
    
    .stApp::after {
        content: "";
        position: fixed;
        bottom: 10vh;
        right: -5vw;
        width: 30vw;
        height: 30vw;
        border: 4px solid #94a3b8;
        transform: rotate(45deg);
        z-index: -1;
        opacity: 0.35;
    }
    
    /* Typography & Spacing */
    body, p, h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 300;
        color: #2c3e50;
        background-color: transparent !important;
    }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 700px;
    }
    
    /* Clean headers */
    h1 {
        font-weight: 200;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: transparent !important;
        color: #2c3e50 !important;
        border: 1px solid #bdc3c7 !important;
        border-radius: 4px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2c3e50 !important;
        color: white !important;
        border-color: #2c3e50 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 0px !important;
        border-bottom: 2px solid transparent !important;
        padding-bottom: 10px;
        font-weight: 400;
        color: #7f8c8d !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #2c3e50 !important;
        color: #2c3e50 !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>voice to notes.</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload your lecture audio to generate minimalist transcripts, functional summaries, and study materials.</div>", unsafe_allow_html=True)

st.write("---")

uploaded_file = st.file_uploader("Select an audio file", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file is not None:
    st.write("") # Spacer
    if st.button("Process Audio"):
        # Save uploaded file to temp file to pass to Whisper
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # 1. Transcription
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(tmp_file_path)

            # 2. Summarization
            with st.spinner("Summarizing text..."):
                summary = summarize_text(transcript)

            # 3. Quiz & Flashcards
            with st.spinner("Generating study materials..."):
                qa_data = generate_quiz_and_flashcards(summary)

            st.write("---")
            
            # Display Results in Minimalist Tabs
            tab1, tab2, tab3 = st.tabs(["Transcript", "Summary", "Flashcards"])
            
            with tab1:
                st.write(transcript)
                st.download_button("Download Transcript", transcript, file_name="transcript.txt", key="dl_transcript")
                
            with tab2:
                st.write(summary)
                st.download_button("Download Summary", summary, file_name="notes.txt", key="dl_summary")
                
            with tab3:
                st.write(qa_data)
                st.download_button("Download Flashcards", qa_data, file_name="flashcards.txt", key="dl_flashcards")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_file_path):
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
