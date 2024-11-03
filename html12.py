import streamlit as st
from bs4 import BeautifulSoup, FeatureNotFound

def beautify_html(html_code):
    """Format HTML code using BeautifulSoup."""
    soup = BeautifulSoup(html_code, 'html.parser')
    return soup.prettify()

def check_html_errors(html_code):
    """Check for common HTML errors such as unclosed tags or invalid structure."""
    errors = []
    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        # Check for unclosed tags (BeautifulSoup automatically fixes them, so we notify the user)
        fixed_html = soup.prettify()
        if fixed_html != html_code:
            errors.append("Warning: The HTML code has been modified to fix unclosed tags or other issues.")
    except FeatureNotFound as e:
        errors.append(f"Parsing Error: {str(e)}")
    except Exception as e:
        errors.append(f"Error: {str(e)}")
    return errors

def main():
    st.title("HTML Code Editor with Error Checking")

    # Static example of HTML code
    example_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample HTML</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample HTML code.</p>
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

    if st.sidebar.button("Format HTML"):
        st.session_state.html_code = beautify_html(st.session_state.html_code)
        st.success("HTML formatted successfully!")

    # Error-checking button
    if st.sidebar.button("Check for Errors"):
        errors = check_html_errors(st.session_state.html_code)
        if errors:
            st.session_state.html_errors = errors
        else:
            st.session_state.html_errors = ["No errors found."]

    # HTML code editor
    updated_code = st.text_area("Edit HTML Code Here", st.session_state.html_code, height=300)
    
    # Check if the code has changed
    if updated_code != st.session_state.html_code:
        st.session_state.html_code = updated_code

    # Display any HTML errors below the editor
    if "html_errors" in st.session_state and st.session_state.html_errors:
        st.markdown("## Error Messages:")
        for error in st.session_state.html_errors:
            st.warning(error)

    # Display the live output of the HTML code below the editor
    st.markdown("## Live Output:")
    output_html = f"<div style='height: 500px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;'><iframe srcdoc='{st.session_state.html_code}' style='width: 100%; height: 100%; border: none;'></iframe></div>"
    st.markdown(output_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
