import streamlit as st

def main():
    st.title("HTML, CSS, and JavaScript Code Editor")

    # Static example of HTML code with CSS and JavaScript
    example_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample HTML with CSS and JavaScript</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: blue; }
        p { color: green; }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample HTML code with CSS and JavaScript.</p>
    <button onclick="displayMessage()">Click Me</button>
    <script>
        function displayMessage() {
            alert('Button clicked!');
        }
    </script>
</body>
</html>"""

    # Initialize session state for HTML code if it doesn't exist
    if 'html_code' not in st.session_state:
        st.session_state.html_code = example_html

    # Sidebar for controls
    st.sidebar.header("Controls")
    filename = st.sidebar.text_input("Enter filename for download (without extension):", "my_html_code")

    # Buttons in the sidebar
    if st.sidebar.button("New File"):
        st.session_state.html_code = example_html  # Reset to example code
        st.success("New file created with example code.")

    # File uploader for "Open File" functionality
    uploaded_file = st.sidebar.file_uploader("Open File", type=["html", "htm"])
    if uploaded_file is not None:
        # Read the file as a string and set it as the HTML code
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state.html_code = file_content
        st.success(f"Loaded content from {uploaded_file.name}")

    if st.sidebar.button("Download HTML"):
        full_filename = f"{filename}.html"
        st.download_button(
            label="Download",
            data=st.session_state.html_code,
            file_name=full_filename,
            mime="text/html"
        )

    # HTML code editor
    updated_code = st.text_area("Edit HTML, CSS, and JavaScript Code Here", st.session_state.html_code, height=300)
    
    # Check if the code has changed
    if updated_code != st.session_state.html_code:
        st.session_state.html_code = updated_code

    # Display the live output of the HTML, CSS, and JavaScript code below the editor
    st.markdown("## Live Output:")
    output_html = f"""
    <iframe srcdoc="{st.session_state.html_code}" style='width: 100%; height: 500px; border: none;'></iframe>
    """
    st.markdown(output_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
