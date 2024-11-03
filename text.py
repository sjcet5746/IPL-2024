import os
import streamlit as st
from datetime import datetime

# Set up YouTube API
API_KEY = "AIzaSyA20DXMC3HeqHs9sOMQUQ041wEkgsoFXb4"  # Replace with your YouTube Data API v3 key
youtube = build('youtube', 'v3', developerKey=API_KEY)

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

# Streamlit UI
st.title("YouTube Video Search")
st.write("Search for YouTube videos using text or voice.")

# Button for voice search
if st.button("Search by Voice"):
    search_query = voice_search()
else:
    # User search input
    search_query = st.text_input("Enter search query", value="Python programming")

if search_query:
    st.write(f"Results for '{search_query}':")
    videos = search_youtube(search_query)

    # Display videos one by one
    for video in videos:
        st.image(video['thumbnail'])
        st.write(f"**Title:** {video['title']}")
        st.write(f"[Watch on YouTube]({video['url']})")
        
        # Add a button to play the video
        st.video(video['url'])  # This embeds the YouTube video player
        
        st.write("---")

# Display last seen date and time
st.sidebar.write("### Last Seen")
last_seen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.write(f"Last seen on: {last_seen_time}")

# Footer section at the bottom of the page
st.write("---")
st.write("### Footer")
st.write("This application is built for educational purposes.")
st.write("YouTube Data API is used for video searching.")
st.write("Developed by SriKrishna")
