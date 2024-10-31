import streamlit as st
import wikipediaapi
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import pyttsx3
import speech_recognition as sr

# Function to get Wikipedia summary with a user-defined character limit
def get_wikipedia_summary(query, lang_code, char_limit, summary_level):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    
    wiki_wiki = wikipediaapi.Wikipedia(
        language=lang_code,
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent=user_agent
    )
    
    page = wiki_wiki.page(query)
    if not page.exists():
        return "Page not found."
    
    # Create summary based on the selected level
    if summary_level == "Brief":
        return page.summary[:char_limit]
    elif summary_level == "Detailed":
        return page.summary  # Full summary
    elif summary_level == "Bullet Points":
        bullet_points = page.summary.split('. ')  # Split the summary into sentences
        return '\n'.join([f"- {point.strip()}" for point in bullet_points if point])[:char_limit]

# Function to save chat history as a PDF with a user-defined filename
def save_chat_history_as_pdf(chat_history, file_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf = canvas.Canvas(tmp_file.name, pagesize=letter)
        pdf.setTitle(file_name)
        pdf.drawString(30, 750, f"{file_name} - Saved on {timestamp}")

        # Write chat history to PDF
        y_position = 720
        for query, response in chat_history:
            pdf.drawString(30, y_position, f"User: {query}")
            y_position -= 20
            pdf.drawString(30, y_position, f"Bot: {response}")
            y_position -= 40
            if y_position < 40:  # Create a new page if content exceeds page length
                pdf.showPage()
                y_position = 750
        pdf.save()

    return tmp_file.name  # Return the temporary file path for download

# Function to display a 404 error page
def display_404():
    st.title("404 Not Found")
    st.write("Oops! The page you are looking for does not exist.")
    st.write("Please go back to the home page or try again.")
    st.button("Go Back", on_click=lambda: st.session_state.clear())  # Clear state to simulate going back

# Function to read text aloud
def read_summary(summary):
    engine = pyttsx3.init()
    engine.say(summary)
    engine.runAndWait()

# Function for voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            st.success(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return None

# Initialize the app
def main():
    st.set_page_config(page_title="Wikipedia Summary Finder", layout="wide")

    # Custom CSS styles for a Google-like UI
    st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            font-family: 'Roboto', sans-serif;
        }
        .stButton {
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 24px;
            padding: 12px 24px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }
        .stButton:hover {
            background-color: #357ae8;
            transform: translateY(-1px);
        }
        .stTextInput {
            border-radius: 24px;
            border: 1px solid #dcdcdc;
            padding: 10px 16px;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .stTextInput:focus {
            border-color: #4285f4;
            outline: none;
            box-shadow: 0 0 5px rgba(66, 133, 244, 0.5);
        }
        .summary-box {
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .summary-box:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            margin: 10px;
            font-size: 20px;
        }
        .footer a {
            margin-right: 10px;
            text-decoration: none;
            color: #4285f4;
            transition: color 0.3s;
        }
        .footer a:hover {
            color: #357ae8;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display last login time
    if 'last_login' not in st.session_state:
        st.session_state['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.write(f"**Last Login:** {st.session_state['last_login']}")

    # New Chat button - clears chat history
    if st.sidebar.button("New Chat"):
        st.session_state.chat_history = []
        st.session_state.favorites = []  # Reset favorites when starting a new chat

    # Initialize session state for favorites if it doesn't exist
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    # Language selection
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te"
    }
    selected_lang = st.sidebar.selectbox("Select Wikipedia Language:", list(lang_map.keys()))

    # Summarization level selection
    summary_levels = ["Brief", "Detailed", "Bullet Points"]
    selected_summary_level = st.sidebar.selectbox("Select Summarization Level:", summary_levels)

    # Sidebar layout
    with st.sidebar:
        st.title("Options")
        char_limit = st.number_input("Enter the character limit for the summary:", min_value=100, max_value=2000, value=1000, step=100)
        save_name = st.text_input("Enter filename to save chat:", value="chat_history")
        if st.button("Save Chat History"):
            pdf_path = save_chat_history_as_pdf(st.session_state.chat_history, save_name)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button("Download PDF", pdf_file, file_name=f"{save_name}.pdf", mime="application/pdf")
        
        # Voice input button
        if st.button("Voice Search"):
            query = voice_input()  # Capture voice input
            if query:  # If a query was captured
                st.session_state.query = query  # Store it in session state for further processing
        
        # Favorites management
        st.title("Favorites")
        if st.session_state.favorites:
            for i, (fav_query, fav_summary) in enumerate(st.session_state.favorites, 1):
                st.write(f"**Favorite {i}: {fav_query}**")
                st.write(f"{fav_summary}")
                
                # Button to remove from favorites
                if st.button(f"Remove Favorite {i}"):
                    st.session_state.favorites.pop(i - 1)  # Remove the favorite
                    st.success(f"Favorite {i} removed!")
                    st.rerun()  # Use st.rerun() to refresh the view
            st.write("---")
        else:
            st.write("No favorites added yet.")

    # Main content
    st.title("Wikipedia Summary Finder")
    
    # Text input for query
    query = st.text_input("Enter a topic to search on Wikipedia:", value=st.session_state.get('query', ''), key='query_input')

    # Handle chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Generate summary on input
    if query:
        lang_code = lang_map[selected_lang]  # Get selected language code
        summary = get_wikipedia_summary(query, lang_code, char_limit, selected_summary_level)

        # Display summary in a styled box
        st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
        st.markdown(f"**Summary for: {query}**")
        st.write(summary)

        # Save favorite button
        if st.button("Save to Favorites"):
            st.session_state.favorites.append((query, summary))
            st.success("Summary saved to favorites!")

        st.markdown("</div>", unsafe_allow_html=True)
        st.session_state.chat_history.append((query, summary))  # Update chat history

        # Option to read the summary aloud
        if st.button("Read Aloud"):
            read_summary(summary)

    # Footer with links
    footer = """
    <div class="footer">
        <a href="https://www.wikipedia.org" target="_blank" title="Wikipedia"><img src="https://img.icons8.com/color/48/000000/wikipedia.png"/></a>
        <a href="https://github.com" target="_blank" title="GitHub"><img src="https://img.icons8.com/color/48/000000/github.png"/></a>
        <a href="https://www.gemini.com" target="_blank" title="Gemini"><img src="https://img.icons8.com/color/48/000000/gemini.png"/></a>
        <p style="margin-top: 10px;">© 2024 Your Name. This application is a project for educational purposes.</p>
    </div>
    <script>
        function showAboutUs() {
            alert("About Us:\\n\\nThis application was developed as an educational project to demonstrate the use of Streamlit for building interactive applications.");
        }
    </script>
    """
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
