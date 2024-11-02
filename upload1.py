import streamlit as st
import pickle
import base64
import os

# File to store uploaded files and their metadata
DATA_FILE = "uploaded_files_data.pkl"

# Function to load uploaded files data from file with error handling
def load_files():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return []
    return []

# Function to save uploaded files data to file
def save_files(file_data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(file_data, f)

# Initialize the files list in session state, loading from file if available
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = load_files()

# Sidebar for uploading files
st.sidebar.header("Upload and View Files")
uploaded_file = st.sidebar.file_uploader("Upload a File", type=["pdf", "jpeg", "jpg", "png", "mp3", "mp4", "mkv"])
custom_name = st.sidebar.text_input("Custom Name for File")

# Button to add file to the list
if st.sidebar.button("Add File"):
    if uploaded_file:
        # Use the custom name if provided, otherwise use the original file name
        file_name = custom_name if custom_name else uploaded_file.name
        # Store the file in session state as (file_name, file_data, file_type)
        st.session_state.uploaded_files.append((file_name, uploaded_file.getvalue(), uploaded_file.type))
        save_files(st.session_state.uploaded_files)  # Save files data to file
        st.sidebar.success(f"File '{file_name}' added!")
    else:
        st.sidebar.warning("Please upload a file.")

# Display section for viewing uploaded files
st.header("Uploaded Files")
st.write("Here are your uploaded files:")

# Display each file with a view/play option
if st.session_state.uploaded_files:
    for file_name, file_data, file_type in st.session_state.uploaded_files:
        # Display the file name
        st.write(f"### {file_name}")

        # Display file based on type
        if file_type == "application/pdf":
            # Display PDF in an iframe
            with st.expander("View PDF"):
                b64 = base64.b64encode(file_data).decode()
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        
        elif file_type in ["image/jpeg", "image/png"]:
            # Display image files
            st.image(file_data, caption=file_name)
        
        elif file_type == "audio/mpeg":
            # Play audio files
            st.audio(file_data, format="audio/mp3")
        
        elif file_type in ["video/mp4", "video/x-matroska"]:
            # Play video files
            st.video(file_data)
        
        else:
            st.write("File format not supported for inline viewing.")
else:
    st.write("No files uploaded yet.")
