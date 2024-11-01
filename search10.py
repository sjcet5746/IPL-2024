import streamlit as st
import requests
import json
import os
import speech_recognition as sr
import pandas as pd
import altair as alt
from PIL import Image
from io import BytesIO

# Function to perform Google Search
def google_search(api_key, cse_id, query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key, 'cx': cse_id, 'q': query, 'num': num_results}
    response = requests.get(url, params=params)
    return response.json()

# Initialize search history and data storage for analytics
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'search_data' not in st.session_state:
    st.session_state.search_data = pd.DataFrame(columns=["Query", "Source", "Timestamp"])

def main():
    st.title("Enhanced Google Search Application")

    # User inputs for API key, CSE ID, and search query
    api_key = "AIzaSyBvnTpjwspsYBMlHN4nMEvybEmZL8mwAQ4"
    cse_id = "464947c4e602c4ee8"
    query = st.text_input("Enter your search query", "", key='query_input')

    # Voice search feature
    if st.button("Use Voice Search"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio)
                st.write(f"You said: {query}")
                if api_key and cse_id and query:
                    results = google_search(api_key, cse_id, query)
                    update_search_history(query, "Voice")
                    display_results(results)
            except sr.UnknownValueError:
                st.error("Could not understand audio.")
            except sr.RequestError:
                st.error("Could not request results from Google.")

    # Trigger search on Enter or when search button is clicked
    if st.button("Search") or st.session_state.get('query_input'):
        if api_key and cse_id and query:
            results = google_search(api_key, cse_id, query)
            update_search_history(query, "Text")
            display_results(results)
        else:
            st.error("Please enter API Key, CSE ID, and a search query.")
    
    # Button to show search history
    if st.button("Show Search History"):
        if st.session_state.search_history:
            st.write("Search History:")
            for h in st.session_state.search_history:
                st.write(h)
        else:
            st.write("No search history found.")

    # Button to clear search history
    if st.button("Clear Search History"):
        st.session_state.search_history.clear()
        st.session_state.search_data = pd.DataFrame(columns=["Query", "Source", "Timestamp"])
        st.success("Search history cleared.")

    # Interactive Analytics Dashboard
    st.subheader("Search Analytics")
    if not st.session_state.search_data.empty:
        # Chart of search counts over time
        search_trends = alt.Chart(st.session_state.search_data).mark_line().encode(
            x='Timestamp:T',
            y='count():Q',
            color='Source:N',
            tooltip=['Query:N', 'count():Q', 'Source:N']
        ).properties(width=600, height=300)
        st.altair_chart(search_trends, use_container_width=True)

        # Most popular queries
        st.write("**Top Search Queries**")
        top_queries = (
            st.session_state.search_data['Query']
            .value_counts()
            .head(5)
            .reset_index()
            .rename(columns={'index': 'Query', 'Query': 'Count'})
        )
        st.write(top_queries)

def display_results(results):
    if results and 'items' in results:
        st.session_state.results = results
        for i, item in enumerate(results['items']):
            st.write(f"**{i + 1}. {item['title']}**")
            st.write(f"[Link]({item['link']})")
            st.write(f"{item['snippet']}\n")
            
            # Check if 'pagemap' and 'cse_image' exist and if 'src' is in 'cse_image'
            if 'pagemap' in item and 'cse_image' in item['pagemap']:
                image_data = item['pagemap']['cse_image'][0]
                image_url = image_data.get('src')  # Use .get() to avoid KeyError
                
                # Try to load and display the image if 'src' exists
                if image_url:
                    try:
                        response = requests.get(image_url)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, width=100)
                    except Exception as e:
                        st.write("**Image could not be loaded.**")
                else:
                    st.write("**Image source not available.**")
            else:
                st.write("No image available for this result.")
    else:
        st.write("No results found.")

def update_search_history(query, source):
    # Update search history and analytics data
    st.session_state.search_history.append(query)
    new_data = pd.DataFrame({
        "Query": [query],
        "Source": [source],
        "Timestamp": [pd.Timestamp.now()]
    })
    st.session_state.search_data = pd.concat([st.session_state.search_data, new_data], ignore_index=True)

if __name__ == "__main__":
    main()
