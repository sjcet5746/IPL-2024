import streamlit as st
import pickle
import base64
import os

# File to store uploaded PDFs and their metadata
DATA_FILE = "pdf_files_data.pkl"

# Function to load PDF data from file with error handling
def load_pdfs():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        except EOFError:
            # If the file is empty or corrupted, return an empty list
            return []
    return []

# Function to save PDF data to file
def save_pdfs(pdf_data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(pdf_data, f)

# Initialize the PDF list in session state, loading from file if available
if "pdf_files" not in st.session_state:
    st.session_state["pdf_files"] = load_pdfs()

# Sidebar for uploading PDFs
st.sidebar.header("Upload and View PDF Files")
pdf_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
custom_name = st.sidebar.text_input("Custom Name for PDF")

# Button to add PDF to the list
if st.sidebar.button("Add PDF"):
    if pdf_file:
        # Use the custom name if provided, otherwise use the original file name
        file_name = custom_name if custom_name else pdf_file.name
        # Store the PDF in session state as (file_name, file_data)
        st.session_state.pdf_files.append((file_name, pdf_file.getvalue()))
        save_pdfs(st.session_state.pdf_files)  # Save PDF data to file
        st.sidebar.success(f"PDF '{file_name}' added!")
    else:
        st.sidebar.warning("Please upload a PDF file.")

# Display section for viewing uploaded PDFs
st.header("Uploaded PDF Files")
st.write("Here are your uploaded PDFs:")

# Display each PDF with a view button
if st.session_state.pdf_files:
    for file_name, file_data in st.session_state.pdf_files:
        # Display the file name
        st.write(f"### {file_name}")
        
        # Button to view PDF
        with st.expander("View PDF"):
            # Generate a base64-encoded PDF link
            b64 = base64.b64encode(file_data).decode()
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.write("No PDF files uploaded yet.")
