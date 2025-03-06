# DocUCare 🏥

DocUCare is an intelligent medical form processing system that helps automate the tedious process of filling out medical forms. Using advanced AI technology, it identifies empty fields in medical forms and allows users to fill them through voice input, making the process more efficient and accessible.

## 🌟 Features

- **Intelligent Form Processing**: Automatically identifies empty fields in uploaded medical forms
- **Voice Input**: Fill out forms naturally using voice commands
- **Real-time Processing**: Instant transcription and form annotation
- **Visual Feedback**: Clear visualization of filled information on the form
- **User-friendly Interface**: Simple, intuitive web interface built with Streamlit

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: 
  - Transformers (MOLMO-7B model)
  - Whisper (Speech Recognition)
  - Ollama (Field Extraction)
- **Image Processing**: OpenCV, PIL
- **Audio Processing**: PyAudio, PvRecorder
- **Other**: NumPy, Matplotlib

## 📋 Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended)
- FFmpeg (for audio processing)