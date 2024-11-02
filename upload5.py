import streamlit as st
import pickle
import base64
import os

# Static password
PASSWORD = "907618125620"

# File to store uploaded files and their metadata
DATA_FILE = "uploaded_files_data.pkl"

# Set maximum file size limit to 1 GB
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB in bytes

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

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = load_files()

# Authentication section
if not st.session_state["logged_in"]:
    st.header("Login")
    password_input = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password_input == PASSWORD:
            st.session_state["logged_in"] = True
            st.success("Login successful!")
        else:
            st.error("Incorrect password. Please try again.")
else:
    # Sidebar for searching files
    st.sidebar.header("Search & Upload Files")

    # Search input
    search_query = st.sidebar.text_input("Search Files")
    if search_query:
        matching_files = [f for f in st.session_state["uploaded_files"] if search_query.lower() in f[0].lower()]
        st.sidebar.write(f"Found {len(matching_files)} matching file(s):")
        for file_name, _, _ in matching_files:
            st.sidebar.write(f"- {file_name}")

    # File uploader with increased size limit
    uploaded_file = st.sidebar.file_uploader("Upload a File", type=["pdf", "jpeg", "jpg", "png", "mp3", "mp4", "mkv"], key="file_uploader", help="Maximum file size is 1 GB.")
    custom_name = st.sidebar.text_input("Custom Name for File")
    
    # Ensure uploaded file is within size limit
    if uploaded_file and uploaded_file.size > MAX_FILE_SIZE:
        st.sidebar.warning("File size exceeds the 1 GB limit. Please upload a smaller file.")
    else:
        # Button to add file to the list
        if st.sidebar.button("Add File"):
            if uploaded_file:
                file_name = custom_name if custom_name else uploaded_file.name
                # Append file as (file_name, file_data, file_type)
                st.session_state["uploaded_files"].append((file_name, uploaded_file.getvalue(), uploaded_file.type))
                save_files(st.session_state["uploaded_files"])  # Save files data to file
                st.sidebar.success(f"File '{file_name}' added!")
            else:
                st.sidebar.warning("Please upload a file.")

    # Categorize files based on type
    categorized_files = {"PDFs": [], "Images": [], "Audio": [], "Videos": []}
    for file_name, file_data, file_type in st.session_state["uploaded_files"]:
        if file_type == "application/pdf":
            categorized_files["PDFs"].append((file_name, file_data))
        elif file_type in ["image/jpeg", "image/png"]:
            categorized_files["Images"].append((file_name, file_data))
        elif file_type in ["audio/mpeg"]:
            categorized_files["Audio"].append((file_name, file_data))
        elif file_type in ["video/mp4", "video/x-matroska"]:
            categorized_files["Videos"].append((file_name, file_data))

    # Dropdown for selecting category
    st.header("Uploaded Files by Category")
    category_choice = st.selectbox("Choose Category", list(categorized_files.keys()))

    # Display files based on chosen category
    def download_button(file_data, file_name):
        b64 = base64.b64encode(file_data).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download</a>'

    def delete_file(file_name):
        # Update the session state
        st.session_state["uploaded_files"] = [
            (fn, fd, ft) for fn, fd, ft in st.session_state["uploaded_files"] if fn != file_name
        ]
        save_files(st.session_state["uploaded_files"])

    files_in_category = categorized_files.get(category_choice, [])
    if files_in_category:
        for file_name, file_data in files_in_category:
            col1, col2, col3 = st.columns([6, 2, 2])
            col1.write(f"**{file_name}**")
            
            # Download button
            download_link = download_button(file_data, file_name)
            col2.markdown(download_link, unsafe_allow_html=True)

            # Delete button
            if col3.button("Delete", key=f"delete_{file_name}"):
                delete_file(file_name)
                
            # Display file preview
            if category_choice == "PDFs":
                with st.expander(f"View PDF - {file_name}"):
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(file_data).decode()}" width="700" height="500" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            elif category_choice == "Images":
                st.image(file_data, caption=file_name)
            elif category_choice == "Audio":
                st.audio(file_data, format="audio/mp3")
            elif category_choice == "Videos":
                st.video(file_data)
    else:
        st.write(f"No files in the {category_choice} category.")
