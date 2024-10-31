import streamlit as st
import wikipediaapi
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# Initialize the Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('english')

# Function to get Wikipedia summary with a user-defined character limit
def get_wikipedia_summary(query, char_limit):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:char_limit]
    else:
        return "Page not found."

# Function to save chat history as a PDF with timestamp
def save_chat_history_as_pdf(chat_history):
    # Timestamp for filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"chat_history_{timestamp}.pdf"
    
    # Create PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf = canvas.Canvas(tmp_file.name, pagesize=letter)
        pdf.setTitle("Chat History")
        pdf.drawString(30, 750, f"Chat History - Saved on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Write chat history to PDF
        y_position = 720
        for query, response in chat_history:
            pdf.drawString(30, y_position, f"User: {query}")
            y_position -= 20
            pdf.drawString(30, y_position, f"Bot: {response}")
            y_position -= 40
            if y_position < 40:  # Create a new page if the content exceeds page length
                pdf.showPage()
                y_position = 750
        pdf.save()
    
    return tmp_file.name  # Return the temporary file path for download

# Initialize the app
def main():
    st.set_page_config(page_title="Wikipedia Summary Finder", layout="wide")
    
    # Display last login time
    if 'last_login' not in st.session_state:
        st.session_state['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.write(f"**Last Login:** {st.session_state['last_login']}")
    
    # Sidebar toggle
    if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = "expanded"
    if st.button("Toggle Sidebar"):
        st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
    st.sidebar.button("New Chat")
    
    # Sidebar layout
    with st.sidebar:
        st.title("Options")
        char_limit = st.number_input("Enter the character limit for the summary:", min_value=100, max_value=2000, value=1000, step=100)

    # Main content
    st.title("Wikipedia Summary Finder")
    query = st.text_input("Enter a topic to search on Wikipedia:")
    
    # Handle chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Generate summary on input
    if query:
        summary = get_wikipedia_summary(query, char_limit)
        st.write("### Summary:")
        st.write(summary)
        st.session_state.chat_history.append((query, summary))

    # Display chat history
    if st.session_state.chat_history:
        st.write("## Chat History")
        for i, (q, s) in enumerate(st.session_state.chat_history, 1):
            st.write(f"**Q{i}:** {q}")
            st.write(f"**A{i}:** {s}")
            st.write("---")

    # Save chat as PDF and display download link
    if st.button("Save Chat History as PDF"):
        pdf_path = save_chat_history_as_pdf(st.session_state.chat_history)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("Download PDF", pdf_file, file_name=f"chat_history_{datetime.datetime.now().strftime('%Y-%m-%d')}.pdf", mime="application/pdf")

    # Placeholder for a share button (actual functionality requires integration with external services)
    if st.button("Share"):
        st.info("Sharing functionality will need integration with email or social media platforms.")

if __name__ == "__main__":
    main()
