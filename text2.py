import streamlit as st
from gtts import gTTS

def text_to_speech(text, filename, lang):
    # Create a gTTS object with the specified language
    tts = gTTS(text=text, lang=lang)
    
    # Save the spoken text to an MP3 file
    tts.save(filename)
    return filename

# Streamlit app
st.title("Text to Speech Converter")

# User input
user_input = st.text_area("Enter the text you want to be spoken:", "")
filename = st.text_input("Enter the filename to save the audio (including .mp3 extension):", "output.mp3")

# Language selection
language = st.selectbox("Select the language:", ["en", "hi", "te"], format_func=lambda x: "English" if x == "en" else "Hindi" if x == "hi" else "Telugu")

# Ensure the filename ends with .mp3
if filename and not filename.endswith('.mp3'):
    filename += '.mp3'

if st.button("Convert to Speech"):
    if user_input and filename:
        saved_file = text_to_speech(user_input, filename, language)
        st.success(f"Saved audio as {saved_file}")
        
        # Display audio player
        st.audio(saved_file, format='audio/mp3')
    else:
        st.error("Please enter both the text and a valid filename.")
