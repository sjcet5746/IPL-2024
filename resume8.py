import streamlit as st
from fpdf import FPDF
import os

# Function to generate the resume PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_social_links(self, social_links, social_photos):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Social Links", ln=True)
        self.set_font("Arial", size=12)
        for name, link in social_links.items():
            self.cell(0, 10, name, ln=True, link=link)
            if name in social_photos:
                try:
                    photo_path = social_photos[name]
                    self.image(photo_path, w=10, h=10)  # Small icon size
                except RuntimeError as e:
                    print(f"Error adding image for {name}: {e}")

    def add_photo(self, photo):
        if photo:
            photo_path = "profile_photo.jpg"
            try:
                with open(photo_path, "wb") as f:
                    f.write(photo.getbuffer())
                self.image(photo_path, x=10, y=10, w=30)  # Adjust size and position as needed
            except Exception as e:
                print(f"Error saving profile photo: {e}")
            finally:
                if os.path.exists(photo_path):
                    os.remove(photo_path)

# Function to generate the resume PDF
def create_resume(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add profile photo if provided
    pdf.add_photo(data["photo"])

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, data["name"], ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, data["profession"], ln=True, align='C')
    pdf.cell(0, 10, data["contact_info"], ln=True, align='C')
    pdf.ln(10)

    # Add student summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, data["summary"])  # Allow multiline summary

    pdf.ln(10)

    # Add social links (now at the end)
    pdf.add_social_links(data["social_links"], data["social_photos"])

    # Education Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", size=12)
    for education in data["education"]:
        pdf.cell(0, 10, education, ln=True)

    pdf.ln(10)

    # Skills Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", size=12)
    for skill in data["skills"]:
        pdf.cell(0, 10, skill, ln=True)

    pdf.ln(10)

    # Certifications Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Certifications", ln=True)
    pdf.set_font("Arial", size=12)
    for cert in data["certifications"]:
        pdf.cell(0, 10, cert, ln=True)

    pdf.ln(10)

    # Honors & Awards Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Honors & Awards", ln=True)
    pdf.set_font("Arial", size=12)
    for award in data["awards"]:
        pdf.cell(0, 10, award, ln=True)

    # Save PDF to a file
    pdf_file = "resume.pdf"
    pdf.output(pdf_file)

    return pdf_file

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
        pdf_file = create_resume(user_data)
        
        # Provide download button
        with open(pdf_file, "rb") as file:
            st.download_button("Download Resume", file, file_name=pdf_file, mime='application/pdf')
        
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
