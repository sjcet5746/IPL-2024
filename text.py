import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Define countries dictionary
countries = {
    'us': 'United States',
    'in': 'India',
    'gb': 'United Kingdom',
    'ca': 'Canada',
    'au': 'Australia',
    'de': 'Germany',
    'fr': 'France',
    'it': 'Italy',
    'jp': 'Japan',
    'cn': 'China',
    'br': 'Brazil',
    'za': 'South Africa',
    'ru': 'Russia',
}

def get_news(api_key, query=None, country='us', language='en', from_date=None, to_date=None):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': query,
        'from': from_date,
        'to': to_date,
        'language': language,
        'pageSize': 100
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()
        if news_data['status'] == 'ok':
            return news_data['articles']
        else:
            st.error("Error fetching news: {}".format(news_data['message']))
            return []

    except requests.exceptions.RequestException as e:
        st.error("HTTP Request failed: {}".format(e))
        return []

# Important queries
important_queries = [
    "COVID-19", "Technology", "Politics", "Economy", "Health", 
    "Environment", "Sports", "Entertainment", "Science", 
    "Education", "Travel"
]

# Streamlit UI setup
st.set_page_config(page_title="News Fetcher", layout="wide")
st.title("News Fetcher")

# Store the last seen timestamp in session state
if 'last_seen' not in st.session_state:
    st.session_state['last_seen'] = datetime.now()
last_seen = st.session_state['last_seen']

# Display last seen timestamp
st.sidebar.write(f"Last accessed: {last_seen.strftime('%Y-%m-%d %H:%M:%S')}")

# Language selection
language = st.selectbox("Select your preferred language:", 
    options=[
        ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), 
        ('de', 'German'), ('it', 'Italian'), ('pt', 'Portuguese'), 
        ('ar', 'Arabic'), ('zh', 'Chinese'), ('hi', 'Hindi'), 
        ('te', 'Telugu')
    ])

# Country selection in the sidebar
country = st.sidebar.selectbox("Select your country:", options=list(countries.keys()), format_func=lambda x: countries[x])

# Sidebar for important queries
st.sidebar.header("Important Queries")
for query in important_queries:
    if st.sidebar.button(query):
        st.session_state.query = query

# Input field for user queries
if 'query' in st.session_state:
    query = st.session_state.query
else:
    query = st.text_input("Enter a search query:", placeholder="Type something...")

# Date pickers for filtering news articles
st.write("Select the date range for previous news articles:")
from_date = st.date_input("From", value=datetime.now() - timedelta(days=30))
to_date = st.date_input("To", value=datetime.now())

# Button to fetch news
if st.button("Fetch News"):
    API_KEY ='43283de608cc43b7a49ad17ceda39636' # Replace with your actual News API key
    news_articles = get_news(API_KEY, query=query, country=country, language=language, from_date=from_date, to_date=to_date)

    if news_articles:
        for i, article in enumerate(news_articles):
            st.subheader(article['title'])
            st.write(article['description'])
            st.write("Published At:", article['publishedAt'])
            st.write("Source:", article['source']['name'])
            st.markdown("---")

    else:
        st.write("No articles found.")

# Footer
st.markdown("---")
st.write("Developed by SriKrishna | © 2024 | All rights reserved.")
st.write(f"Last accessed on: {last_seen.strftime('%Y-%m-%d %H:%M:%S')}")
