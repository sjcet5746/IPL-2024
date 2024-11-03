import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Function to generate the resume PDF
def create_resume(data):
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, data["name"])
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 70, data["profession"])
    p.drawString(100, height - 90, data["contact_info"])

    # Add student summary
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 120, "Summary:")
    p.setFont("Helvetica", 12)
    y = height - 140
    for line in data["summary"].split('\n'):
        p.drawString(100, y, line)
        y -= 15  # Move down for the next line

    # Education Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Education:")
    p.setFont("Helvetica", 12)
    y -= 20
    for edu in data["education"]:
        p.drawString(100, y, edu)
        y -= 15

    # Skills Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Skills:")
    p.setFont("Helvetica", 12)
    y -= 20
    for skill in data["skills"]:
        p.drawString(100, y, skill)
        y -= 15

    # Certifications Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Certifications:")
    p.setFont("Helvetica", 12)
    y -= 20
    for cert in data["certifications"]:
        p.drawString(100, y, cert)
        y -= 15

    # Honors & Awards Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Honors & Awards:")
    p.setFont("Helvetica", 12)
    y -= 20
    for award in data["awards"]:
        p.drawString(100, y, award)
        y -= 15

    # Save the PDF to the buffer
    p.save()
    buffer.seek(0)

    return buffer

# Streamlit app
def main():
    st.title("Resume Builder")

    # Collecting user details
    name = st.text_input("Full Name", key="name")
    profession = st.text_input("Profession/Title", key="profession")
    email = st.text_input("Email", key="email")
    phone = st.text_input("Phone Number", key="phone")
    address = st.text_input("Address", key="address")
    contact_info = f"{email} | {phone} | {address}"

    # Summary
    summary = st.text_area("Summary", "Write a brief summary about yourself")

    social_links = {}
    social_photos = {}
    social_media_count = st.number_input("Number of Social Media Links", min_value=0, max_value=10, value=0, key="social_count")

    for i in range(social_media_count):
        social_name = st.text_input(f"Social Media Name {i + 1}", key=f"social_name_{i}")
        social_link = st.text_input(f"Social Media Link {i + 1}", key=f"social_link_{i}")
        social_photo = st.file_uploader(f"Upload Photo for {social_name}", type=["jpg", "jpeg", "png"], key=f"social_photo_{i}")
        
        if social_name and social_link:
            social_links[social_name] = social_link
            if social_photo:
                photo_path = f"social_photo_{i}.jpg"
                try:
                    with open(photo_path, "wb") as f:
                        f.write(social_photo.getbuffer())
                    social_photos[social_name] = photo_path
                except Exception as e:
                    print(f"Error saving social photo for {social_name}: {e}")

    # Photo upload
    photo = st.file_uploader("Upload a Profile Photo (optional)", type=["jpg", "jpeg", "png"])

    education = st.text_area("Education (list each line separately)", "Institution Name, Degree, Duration, Percentage")
    
    skills = st.text_area("Skills (list each line separately)", "Skill 1\nSkill 2\nSkill 3")
    
    certifications = []
    cert_count = st.number_input("Number of Certifications", min_value=0, max_value=10, value=0, key="cert_count")
    for i in range(cert_count):
        cert_name = st.text_input(f"Certification Name {i + 1}", key=f"cert_name_{i}")
        cert_link = st.text_input(f"Certification Link {i + 1}", key=f"cert_link_{i}")
        if cert_name and cert_link:
            certifications.append(cert_name)

    awards = st.text_area("Honors & Awards (list each line separately)", "Award 1\nAward 2")

    # Live Preview Section
    st.subheader("Live Preview")
    preview_markdown = f"""
    ### {name}
    **Profession:** {profession}

    **Contact Info:** {contact_info}

    **Summary:**
    {summary}

    **Social Links:**
    """
    for link_name, link in social_links.items():
        preview_markdown += f"- [{link_name}]({link})\n"

    preview_markdown += "\n**Education:**\n"
    for edu in education.strip().split('\n'):
        preview_markdown += f"- {edu}\n"

    preview_markdown += "\n**Skills:**\n"
    for skill in skills.strip().split('\n'):
        preview_markdown += f"- {skill}\n"

    preview_markdown += "\n**Certifications:**\n"
    for cert in certifications:
        preview_markdown += f"- {cert}\n"

    preview_markdown += "\n**Honors & Awards:**\n"
    for award in awards.strip().split('\n'):
        preview_markdown += f"- {award}\n"

    st.markdown(preview_markdown)

    if st.button("Generate Resume"):
        user_data = {
            "name": name,
            "profession": profession,
            "contact_info": contact_info,
            "social_links": social_links,
            "social_photos": social_photos,
            "photo": photo,
            "summary": summary,
            "education": education.strip().split('\n'),
            "skills": skills.strip().split('\n'),
            "certifications": certifications,
            "awards": awards.strip().split('\n'),
        }

        # Create resume PDF
        pdf_buffer = create_resume(user_data)
        
        # Provide download button
        st.download_button("Download Resume", pdf_buffer, file_name="resume.pdf", mime='application/pdf')

        # Display the resume
        st.header("Your Resume")
        st.write(f"**Name:** {name}")
        st.write(f"**Profession:** {profession}")
        st.write(f"**Contact Info:** {contact_info}")
        st.write(f"**Summary:** {summary}")

        st.subheader("Social Links:")
        for link_name, link in social_links.items():
            st.write(f"- [{link_name}]({link})")
        
        st.subheader("Education:")
        for edu in education.strip().split('\n'):
            st.write(f"- {edu}")

        st.subheader("Skills:")
        for skill in skills.strip().split('\n'):
            st.write(f"- {skill}")

        st.subheader("Certifications:")
        for cert in certifications:
            st.write(f"- {cert}")

        st.subheader("Honors & Awards:")
        for award in awards.strip().split('\n'):
            st.write(f"- {award}")

if __name__ == "__main__":
    main()
