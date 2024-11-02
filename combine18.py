import os
import streamlit as st
from googleapiclient.discovery import build
import speech_recognition as sr
import wikipediaapi
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from gtts import gTTS
import requests
import json
import pandas as pd
import altair as alt
from datetime import date

# Set up YouTube API
API_KEY_YOUTUBE = "AIzaSyA20DXMC3HeqHs9sOMQUQ041wEkgsoFXb4"  # Replace with your YouTube Data API v3 key
youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)

# Function to search YouTube videos
def search_youtube(query, max_results=5):
    try:
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail = item['snippet']['thumbnails']['default']['url']
            url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({'title': title, 'url': url, 'video_id': video_id, 'thumbnail': thumbnail})
        return videos
    except Exception as e:
        st.write(f"Error fetching videos: {e}")
        return []

# Function for voice recognition
def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            st.success(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            st.error("Could not understand audio")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

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

# Function to perform Google Search
def google_search(api_key, cse_id, query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key, 'cx': cse_id, 'q': query, 'num': num_results}
    response = requests.get(url, params=params)
    return response.json()

# Display Google Search Results
def display_google_results(results):
    if "items" in results:
        for item in results['items']:
            st.write(f"**{item['title']}**")
            st.write(item['snippet'])
            st.write(f"[Read more]({item['link']})")
            st.write("---")
    else:
        st.error("No results found.")

# News Search Function
def search_news(query, from_date=None, to_date=None):
    api_key = '43283de608cc43b7a49ad17ceda39636'  # Replace with your News API key
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    if from_date and to_date:
        url += f"&from={from_date}&to={to_date}"
    response = requests.get(url)
    return response.json()

# Display News Results
def display_news(articles):
    if "articles" in articles:
        for article in articles['articles']:
            st.write(f"**{article['title']}**")
            st.write(article['description'])
            st.write(f"[Read more]({article['url']})")
            st.write("---")
    else:
        st.error("No news articles found.")

def main():
    st.set_page_config(page_title="Multi-Search Application", layout="wide")

    # Sidebar options
    st.sidebar.title("Options")
    if st.sidebar.button("Voice Search"):
        query = voice_search()
        if query:
            st.session_state.query = query  # Store query in session state for use in the main sections
    else:
        st.session_state.query = ""  # Reset if not using voice search

    search_type = st.sidebar.radio("Select Search Type", ("Wikipedia", "Google", "YouTube", "News"))

    # Last seen timestamp
    st.sidebar.write(f"Last seen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if search_type == "Wikipedia":
        lang_map = {"English": "en", "Spanish": "es", "Chinese": "zh", "Hindi": "hi", "Telugu": "te"}
        selected_lang = st.sidebar.selectbox("Wikipedia Language", list(lang_map.keys()))
        summary_levels = ["Brief", "Detailed", "Bullet Points"]
        summary_level = st.sidebar.selectbox("Summarization Level", summary_levels)
        char_limit = st.sidebar.slider("Character Limit", min_value=100, max_value=2000, value=500, step=100)

        st.title("Wikipedia Summary & Text-to-Speech")
        query = st.text_input("Enter a topic to search on Wikipedia:", value=st.session_state.query)

        if query:
            lang_code = lang_map[selected_lang]
            summary = get_wikipedia_summary(query, lang_code, char_limit, summary_level)
            st.markdown(f"### Summary for: {query}")
            st.write(summary)

            # Text-to-speech
            tts_filename = f"{query}_speech.mp3"
            if st.button("Play Text-to-Speech"):
                text_to_speech(summary, tts_filename, lang=lang_code)
                st.audio(tts_filename, format="audio/mp3")

        # Footer for Wikipedia
        st.write("---")
        st.write("### Footer")
        st.write("This is a Wikipedia search section. You can find detailed information and summaries here.")

    elif search_type == "Google":
        st.title("Google Search")
        query = st.text_input("Enter a search query for Google:", value=st.session_state.query)
        if query and st.button("Search"):
            results = google_search("AIzaSyBvnTpjwspsYBMlHN4nMEvybEmZL8mwAQ4", "464947c4e602c4ee8", query)  # Ensure you replace with actual API key and CSE ID
            display_google_results(results)

        # Footer for Google
        st.write("---")
        st.write("### Footer")
        st.write("This is a Google search section. Use it to find websites and online resources.")

    elif search_type == "YouTube":
        st.title("YouTube Search")
        query = st.text_input("Enter a topic to search on YouTube:", value=st.session_state.query)
        if query and st.button("Search"):
            videos = search_youtube(query)
            if videos:
                for video in videos:
                    st.write(f"[{video['title']}]({video['url']})")
                    st.image(video['thumbnail'])
                    st.video(video['url'])  # Embed video player
                    st.write("---")

        # Footer for YouTube
        st.write("---")
        st.write("### Footer")
        st.write("This is a YouTube search section. Watch videos directly from your search results.")

    elif search_type == "News":
        st.subheader("Select Date Range")
        start_date = st.date_input("From", datetime.date.today() - datetime.timedelta(days=7))
        end_date = st.date_input("To", datetime.date.today())
        
        st.title("News Search")
        query = st.text_input("Enter a news topic to search:", value=st.session_state.query)
        if query and st.button("Search"):
            articles = search_news(query, start_date, end_date)
            display_news(articles)

        # Footer for News
        st.write("---")
        st.write("### Footer")
        st.write("This is a news search section. Find the latest news articles here.")

    # Save chat history as PDF
    if st.button("Save Chat History as PDF"):
        chat_history = []
        if st.session_state.query:
            chat_history.append((st.session_state.query, "Your response here"))  # Replace with actual response
        file_name = st.text_input("Enter filename for PDF:", "chat_history.pdf")
        pdf_file = save_chat_history_as_pdf(chat_history, file_name)
        st.success(f"Chat history saved as PDF: {pdf_file}")

if __name__ == "__main__":
    main()
