import streamlit as st
import wikipediaapi
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from gtts import gTTS
import speech_recognition as sr

# Wikipedia summary function with character limit and summary levels
def get_wikipedia_summary(query, lang_code, char_limit, summary_level):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    wiki = wikipediaapi.Wikipedia(language=lang_code, extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent=user_agent)
    page = wiki.page(query)
    if not page.exists():
        return "Page not found."
    if summary_level == "Brief":
        return page.summary[:char_limit]
    elif summary_level == "Detailed":
        return page.summary  # Full summary
    elif summary_level == "Bullet Points":
        points = page.summary.split('. ')
        return '\n'.join(f"- {p.strip()}" for p in points if p)[:char_limit]

# Save chat history as PDF with a user-defined filename
def save_chat_history_as_pdf(chat_history, file_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf = canvas.Canvas(tmp_file.name, pagesize=letter)
        pdf.setTitle(file_name)
        pdf.drawString(30, 750, f"{file_name} - Saved on {timestamp}")
        y_position = 720
        for query, response in chat_history:
            pdf.drawString(30, y_position, f"User: {query}")
            y_position -= 20
            pdf.drawString(30, y_position, f"Bot: {response}")
            y_position -= 40
            if y_position < 40:
                pdf.showPage()
                y_position = 750
        pdf.save()
    return tmp_file.name

# Text-to-speech using gTTS
def text_to_speech(text, filename, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

# Voice search function
def voice_search(lang_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            # Recognize the speech based on the specified language
            query = recognizer.recognize_google(audio, language=lang_code)
            st.success(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Initialize the Streamlit app
def main():
    st.set_page_config(page_title="Wikipedia Summary & Text-to-Speech", layout="wide")

    # Sidebar options
    st.sidebar.title("Options")
    lang_map = {
        "English": "en",
        "Spanish": "es",
        "Chinese": "zh",
        "Hindi": "hi",
        "Telugu": "te"
    }
    selected_lang = st.sidebar.selectbox("Wikipedia Language", list(lang_map.keys()), key="language_selector")
    summary_levels = ["Brief", "Detailed", "Bullet Points"]
    summary_level = st.sidebar.selectbox("Summarization Level", summary_levels)
    char_limit = st.sidebar.slider("Character Limit", min_value=100, max_value=2000, value=500, step=100)

    # Chat history and favorites in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    st.title("Wikipedia Summary & Text-to-Speech")
    
    # Text input for manual search
    query = st.text_input("Enter a topic to search on Wikipedia:")

    # Button for voice search
    if st.button("Voice Search"):
        lang_code = lang_map[selected_lang]  # Get the language code for the selected language
        voice_query = voice_search(lang_code)  # Pass the language code to the voice search
        if voice_query:
            query = voice_query  # Use the voice query if recognized

    # Display summary based on query and language selection
    if query:
        lang_code = lang_map[selected_lang]
        summary = get_wikipedia_summary(query, lang_code, char_limit, summary_level)
        st.markdown(f"### Summary for: {query}")
        st.write(summary)
        st.session_state.chat_history.append((query, summary))

        # Save to favorites
        if st.button("Add to Favorites"):
            st.session_state.favorites.append((query, summary))
            st.success("Added to favorites!")

        # Text-to-speech
        tts_filename = f"{query}_speech.mp3"
        if st.button("Play Text-to-Speech"):
            text_to_speech(summary, tts_filename, lang=lang_code)
            st.audio(tts_filename, format="audio/mp3")

    # Save chat history as PDF
    file_name = st.sidebar.text_input("File Name to Save Chat", value="chat_history")
    if st.sidebar.button("Save Chat as PDF"):
        pdf_path = save_chat_history_as_pdf(st.session_state.chat_history, file_name)
        with open(pdf_path, "rb") as pdf_file:
            st.sidebar.download_button("Download PDF", pdf_file, file_name=f"{file_name}.pdf", mime="application/pdf")

    # Display favorites
    st.sidebar.write("### Favorites")
    for i, (fav_query, fav_summary) in enumerate(st.session_state.favorites, 1):
        st.sidebar.write(f"**{i}. {fav_query}**")
        st.sidebar.write(fav_summary[:100] + "...")

if __name__ == "__main__":
    main()
