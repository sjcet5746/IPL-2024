import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="News Fetcher", layout="wide")

# CSS styling for Canva theme
st.markdown(
    """
    <style>
    /* General styling */
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background-color: #f8f9fa;  /* Light gray background */
        color: #333;  /* Dark gray font color */
    }
    
    /* Title styling */
    h1 {
        color: #00bcd4;  /* Canva teal */
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }

    /* Sidebar styling */
    .css-18e3th9 {
        background-color: #ffffff;  /* White background for sidebar */
        color: #333;  /* Dark text color */
        border-right: 1px solid #e0e0e0;  /* Light gray border */
        padding: 20px;
    }

    /* Sidebar header */
    .css-hxt7ib {
        color: #00bcd4;  /* Canva teal */
        font-weight: bold;
    }

    /* Button styling */
    button {
        background-color: #00bcd4 !important;  /* Canva teal button */
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 20px;
        border-radius: 5px;
    }

    /* Dropdown and input styling */
    .stTextInput, .stDateInput, .stSelectbox {
        border: 1px solid #e0e0e0 !important;  /* Light gray border */
        border-radius: 5px !important;
        padding: 10px !important;
        font-size: 1em !important;
    }

    /* News articles styling */
    .stMarkdown, .stSubheader {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background-color: #ffffff;  /* White background for articles */
        color: #212529;  /* Darker gray for articles text */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Footer styling */
    footer {
        font-size: 0.85em;
        color: #6c757d;  /* Gray footer text */
        text-align: center;
        margin-top: 50px;
        padding: 10px;
        border-top: 1px solid #e0e0e0;
    }

    /* Link styling */
    a {
        color: #00bcd4; /* Canva teal */
    }

    a:hover {
        color: #0097a7; /* Darker teal on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        'pageSize': 20
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
st.title("News Fetcher")

# Store and display the last seen timestamp
if 'last_seen' not in st.session_state:
    st.session_state['last_seen'] = datetime.now()
else:
    st.session_state['last_seen'] = datetime.now()
last_seen = st.session_state['last_seen']

# Sidebar layout
st.sidebar.title("Settings")
st.sidebar.write(f"Last accessed on: {last_seen.strftime('%Y-%m-%d %H:%M:%S')}")

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
    API_KEY = '43283de608cc43b7a49ad17ceda39636'   # Replace with your actual News API key
    news_articles = get_news(API_KEY, query=query, country=country, language=language, from_date=from_date, to_date=to_date)

    if news_articles:
        for i, article in enumerate(news_articles):
            st.subheader(article['title'])
            st.markdown(f"**Source**: {article['source']['name']} | **Published At**: {article['publishedAt']}")
            st.write(article['description'] or "No description available")
            st.markdown(f"[Read more]({article['url']})")
            st.markdown("---")

        # Visualization of trends in news topics
        dates = [article['publishedAt'][:10] for article in news_articles]
        date_counts = pd.Series(dates).value_counts().sort_index()

        st.subheader("Trends in News Topics Over Time")
        plt.figure(figsize=(10, 5))
        plt.plot(date_counts.index, date_counts.values, marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.title('Frequency of Articles Over Time')
        st.pyplot(plt)

    else:
        st.write("No articles found.")

# Footer
st.markdown("---")
st.markdown(
    """
    <footer>
        Developed by SriKrishna | © 2024 | All rights reserved.<br>
        Last accessed on: {}
    </footer>
    """.format(last_seen.strftime('%Y-%m-%d %H:%M:%S')),
    unsafe_allow_html=True
)
