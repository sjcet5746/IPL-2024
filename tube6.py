import streamlit as st
import yt_dlp

def download_youtube_video(url):
    ydl_opts = {'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        st.success(f"Video downloaded successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("YouTube Video Downloader")
    
    # Input field for YouTube URL
    url = st.text_input("Enter the YouTube video URL:")
    
    # Button to trigger download
    if st.button("Download Video"):
        if url:
            st.write("Downloading the video...")
            download_youtube_video(url)
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
