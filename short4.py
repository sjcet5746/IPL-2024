import streamlit as st
import pickle
import os

# File to store shortcut data
DATA_FILE = "shortcuts_data.pkl"

# Function to load shortcuts from file
def load_shortcuts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []

# Function to save shortcuts to file
def save_shortcuts(shortcuts):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(shortcuts, f)

# Initialize shortcuts in session state, loading from file if available
if "shortcuts" not in st.session_state:
    st.session_state["shortcuts"] = load_shortcuts()

# Sidebar inputs for adding shortcuts
st.sidebar.header("Add a Website Shortcut")
name = st.sidebar.text_input("Shortcut Name")
link = st.sidebar.text_input("Website Link (https://...)")
icon_file = st.sidebar.file_uploader("Upload an Icon", type=["png", "jpg", "jpeg"])

# Button to add the shortcut
if st.sidebar.button("Add Shortcut"):
    if name and link and icon_file:
        # Append new shortcut to session state
        st.session_state.shortcuts.append((name, link, icon_file.getvalue()))
        save_shortcuts(st.session_state.shortcuts)  # Save to file
        st.sidebar.success(f"Shortcut '{name}' added!")
    else:
        st.sidebar.warning("Please enter all details including an icon.")

# Display shortcuts with Google Apps-style icon
st.header("My Shortcuts")
with st.expander("Click to View Shortcuts"):
    st.write("Here are your added shortcuts:")

    # Display each shortcut with its custom icon
    if st.session_state.shortcuts:
        for name, link, icon_data in st.session_state.shortcuts:
            st.image(icon_data, width=40)  # Display icon
            st.markdown(f"[{name}]({link})", unsafe_allow_html=True)  # Display name as link
    else:
        st.write("No shortcuts added yet.")
