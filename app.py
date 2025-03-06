import streamlit as st
from utils import *
import warnings
warnings.filterwarnings("ignore")

def click_button():
    st.session_state.clicked = True

def stop_button():
    st.session_state.stop = True

def record_audio_to_file(output_path, device_index=-1, frame_length=512, sample_rate=16000):
    """
    Records audio using PvRecorder and saves it to a WAV file.

    Args:
        output_path (str): Path to save the recorded audio.
        device_index (int): Index of the audio device (-1 for default device).
        frame_length (int): Frame length for recording.
        sample_rate (int): Sample rate of the audio (default 16000 Hz).
    """
    recorder = PvRecorder(device_index=device_index, frame_length=frame_length)
    audio = []

    try:
        print("Recording... Click Stop Recording to stop.")
        recorder.start()

        while not st.session_state.stop:
            frame = recorder.read()
            audio.extend(frame)

        print("Recording stopped.")
        recorder.stop()
        with wave.open(output_path, 'w') as f:
            f.setparams((1, 2, sample_rate, 0, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
        print(f"Audio saved to {output_path}")
    finally:
        recorder.delete()

@st.cache_resource
def load_model(model_name):
    return load_model_and_processor(model_name)

st.session_state.move_beyond_image_upload = False
model_name = 'impactframes/molmo-7B-D-bnb-4bit'
audio_file_path = 'App Docs/audio.wav'
model, processor = load_model(model_name)
input_text = "list the 'empty' fields in the form in a new line list. No extra stuff."

st.title('DocUCare')
st.write('Welcome to DocUCare! Please upload your medical form to get started.')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # save the file to 'App Docs' folder
    filename = uploaded_file.name
    # if file is not an image, throw error
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        st.error('Please upload an image file (PNG, JPG, or JPEG)')
        st.stop()
        
    
    # Save the uploaded file
    image_path = os.path.join('App Docs', filename)
    with open(image_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f'File {filename} successfully uploaded!')
    st.session_state.move_beyond_image_upload = True
    

if st.session_state.move_beyond_image_upload:
    st.image(image_path, use_container_width =True)
    output = generate_output(model, processor, image_path, input_text)
    st.divider()
    st.write('**Details missing in the form:**')
    for item in output.split('\n'):
        st.write("•",item)
    st.divider()



    st.write('**Record audio to fill the form:**')
    audio_value = st.audio_input("Click to begin")
    if audio_value:
        print("Saving audio...")
        output_path = "App Docs/audio.wav"
        with open(output_path, "wb") as f:
            f.write(audio_value.getbuffer())
        st.divider()
        st.write("Processing...")
        transcription = transcribe_long_audio('App Docs/audio.wav')
        
        extracted_fields = extract_fields_with_ollama("llama3.2:3b", output.split('\n'), transcription)
        print("FIELDS\n", extracted_fields)
        image_path = "Forms/health_assessment_form.png"  # Replace with your local image path
        output_path = "annotated_form.png"
        
        annotate_form_with_values(f"App Docs/{filename}", extracted_fields, model, processor, 'App Docs/annotated_form.png')
        st.divider()
        st.write('**Annotated Form:**')
        
        st.image('App Docs/annotated_form.png', use_container_width =True)