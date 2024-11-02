import streamlit as st

# Initialize the session state for shortcuts if not already done
if "shortcuts" not in st.session_state:
    st.session_state["shortcuts"] = []

# Sidebar inputs for adding shortcuts
st.sidebar.header("Add a Website Shortcut")
name = st.sidebar.text_input("Shortcut Name")
link = st.sidebar.text_input("Website Link (https://...)")
icon_file = st.sidebar.file_uploader("Upload an Icon", type=["png", "jpg", "jpeg"])

# Button to add the shortcut
if st.sidebar.button("Add Shortcut"):
    if name and link and icon_file:
        # Save the shortcut details as a tuple (name, link, icon) to session state
        st.session_state.shortcuts.append((name, link, icon_file.getvalue()))
        st.sidebar.success(f"Shortcut '{name}' added!")
    else:
        st.sidebar.warning("Please enter all details including an icon.")

# Display Google Apps-style icon or dots button
st.header("My Shortcuts")
with st.expander("Click to View Shortcuts"):
    st.write("Here are your added shortcuts:")

    # Display each shortcut with its custom icon
    if st.session_state.shortcuts:
        for name, link, icon_data in st.session_state.shortcuts:
            # Display icon with specified size and name as a link
            st.image(icon_data, width=40)  # Show uploaded icon
            st.markdown(f"[{name}]({link})", unsafe_allow_html=True)  # Display link
    else:
        st.write("No shortcuts added yet.")
