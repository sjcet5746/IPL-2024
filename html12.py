import streamlit as st

def main():
    st.title("HTML, CSS, and JavaScript Code Editor")

    # Example HTML with CSS and JavaScript
    example_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample HTML with CSS and JavaScript</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; }
        h1 { color: #3333ff; }
        p { color: #555555; }
        button { padding: 10px 20px; background-color: #28a745; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #218838; }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample HTML page with CSS and JavaScript.</p>
    <button onclick="displayMessage()">Click Me</button>
    <script>
        function displayMessage() {
            alert('Button clicked!');
        }
    </script>
</body>
</html>"""

    # Initialize session state for HTML code and run state if they don't exist
    if 'html_code' not in st.session_state:
        st.session_state.html_code = example_html
    if 'run_clicked' not in st.session_state:
        st.session_state.run_clicked = False

    # Sidebar for controls
    st.sidebar.header("Controls")
    filename = st.sidebar.text_input("Enter filename for download (without extension):", "my_html_code")

    # Buttons in the sidebar
    if st.sidebar.button("New File"):
        st.session_state.html_code = example_html  # Reset to example code
        st.session_state.run_clicked = False
        st.success("New file created with example code.")

    # File uploader for "Open File" functionality
    uploaded_file = st.sidebar.file_uploader("Open File", type=["html", "htm"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state.html_code = file_content
        st.session_state.run_clicked = False
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
        st.session_state.run_clicked = False  # Reset run state when code changes

    # Run button
    if st.button("Run"):
        st.session_state.run_clicked = True

    # Display the live output of the HTML, CSS, and JavaScript code only when Run is clicked
    if st.session_state.run_clicked:
        st.markdown("## Live Output:")
        # Embedding the HTML code in an iframe with srcdoc to support live rendering
        output_html = f"""
        <iframe srcdoc="{st.session_state.html_code.replace('"', '&quot;')}" style="width: 100%; height: 500px; border: none;"></iframe>
        """
        st.components.v1.html(output_html, height=500)
    else:
        st.info("Click 'Run' to display the output.")

if __name__ == "__main__":
    main()
