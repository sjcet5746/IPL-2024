import streamlit as st
import pandas as pd
import pickle
import os
from PIL import Image

# Function to load data from a pickle file
def load_data():
    if os.path.exists('student_data.pkl'):
        with open('student_data.pkl', 'rb') as f:
            return pickle.load(f)
    return {}

# Function to save data to a pickle file
def save_data(data):
    with open('student_data.pkl', 'wb') as f:
        pickle.dump(data, f)

# Load existing data
student_data = load_data()

# Application password
PASSWORD = "907618125620"

# Password input for the application
password_input = st.text_input("Enter Password", type="password")

if password_input == PASSWORD:
    # Title of the application
    st.title("Student Marks Management System")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    selection = st.sidebar.radio("Select an action", ["Add Student", "Show Results", "Top Students", "Delete Student", "Students Details"])

    if selection == "Add Student":
        st.header("Add New Student")

        # Input for student details
        student_name = st.text_input("Student Name")
        roll_number = st.text_input("Roll Number")
        branch = st.text_input("Branch")
        image_file = st.file_uploader("Upload Student Image", type=["jpg", "jpeg", "png"])

        if st.button("Add Student"):
            if not roll_number or not image_file:
                st.warning("Please enter the roll number and upload the student photo.")
            elif roll_number in student_data:
                st.warning("Student with this roll number already exists.")
            else:
                student_data[roll_number] = {
                    "name": student_name,
                    "branch": branch,
                    "image": image_file,
                    "semesters": {}
                }
                save_data(student_data)
                st.success(f"Student {student_name} added successfully!")

        # Input for semester and subject marks
        semester = st.number_input("Semester", min_value=1, step=1)
        subject = st.text_input("Subject Name")
        marks = st.number_input("Marks", min_value=0, max_value=100, step=1)

        if st.button("Add Subject Marks"):
            if roll_number in student_data:
                if semester not in student_data[roll_number]["semesters"]:
                    student_data[roll_number]["semesters"][semester] = {}

                student_data[roll_number]["semesters"][semester][subject] = marks
                save_data(student_data)
                st.success(f"Added {subject} marks for {student_name} in Semester {semester}.")
            else:
                st.warning("Please add the student before adding marks.")

    elif selection == "Show Results":
        st.header("Student Results")

        # Branch-wise results
        branches = set(info["branch"] for info in student_data.values())
        selected_branch = st.selectbox("Select Branch for Results", list(branches))

        if st.button("Show All Results"):
            filtered_students = {roll: info for roll, info in student_data.items() if info["branch"] == selected_branch}
            
            if filtered_students:
                # Create a DataFrame for displaying student results
                student_details = []
                for roll, info in filtered_students.items():
                    row = {
                        "SI No": len(student_details) + 1,
                        "Name": info["name"],
                        "Roll No": roll,
                    }
                    total_marks = 0
                    total_subjects = 0
                    for sem, results in info["semesters"].items():
                        sem_total = sum(results.values())
                        row[f"Sem {sem} Total"] = sem_total
                        total_marks += sem_total
                        total_subjects += len(results)
                        for subject, marks in results.items():
                            row[subject] = marks
                    row["Total Marks"] = total_marks
                    if total_subjects > 0:
                        row["Percentage"] = (total_marks / (total_subjects * 100)) * 100
                    student_details.append(row)

                # Create DataFrame
                df = pd.DataFrame(student_details)
                st.dataframe(df)

            else:
                st.warning("No data available for this branch.")

    elif selection == "Top Students":
        st.header("Top Students")
        
        top_n = st.number_input("Number of top students to show", min_value=1, step=1)
        if st.button("Show Top Students"):
            top_students = []

            for roll, info in student_data.items():
                total_marks = sum(sum(res.values()) for res in info["semesters"].values())
                top_students.append((info['name'], roll, total_marks))

            # Sorting by total marks
            top_students.sort(key=lambda x: x[2], reverse=True)
            top_students = top_students[:top_n]

            if top_students:
                st.write("Top Students:")
                for name, roll, total in top_students:
                    st.write(f"{name} (Roll: {roll}) - Total Marks: {total}")
            else:
                st.warning("No students found.")

    elif selection == "Delete Student":
        st.header("Delete Student")
        
        # Dropdown to select the branch
        branches = set(info["branch"] for info in student_data.values())
        selected_branch = st.selectbox("Select Branch", list(branches))

        # Dropdown to select the student based on the selected branch
        student_names = [info["name"] for roll, info in student_data.items() if info["branch"] == selected_branch]
        student_to_delete = st.selectbox("Select Student to Delete", student_names)

        if st.button("Delete Student"):
            roll_number_to_delete = next(roll for roll, info in student_data.items() if info["name"] == student_to_delete)
            del student_data[roll_number_to_delete]
            save_data(student_data)
            st.success(f"Student {student_to_delete} deleted successfully!")

    elif selection == "Students Details":
        st.header("Student Details")

        # Dropdown to select branch first
        branches = set(info["branch"] for info in student_data.values())
        selected_branch = st.selectbox("Select Branch", list(branches))

        # Then select student based on the branch
        student_names = [info["name"] for roll, info in student_data.items() if info["branch"] == selected_branch]
        selected_student_name = st.selectbox("Select Student", student_names)

        if selected_student_name:
            # Get student details
            student_info = next((info for info in student_data.values() if info["name"] == selected_student_name), None)
            
            if student_info:
                col1, col2 = st.columns([2, 1])

                # Display student details
                with col1:
                    st.subheader("Details")
                    roll_number = next(roll for roll, info in student_data.items() if info['name'] == student_info['name'])
                    st.write(f"**Name:** {student_info['name']}")    
                    st.write(f"**Roll No:** {roll_number}")
                    st.write(f"**Branch:** {student_info['branch']}")
                    
                    # Display results
                    st.write("**Results:**")
                    for sem, results in student_info['semesters'].items():
                        st.write(f"**Semester {sem} Results:**")
                        for subject, marks in results.items():
                            st.write(f"{subject}: {marks}")
                    
                    # Calculate and display total marks and percentage
                    total_marks = sum(sum(marks for marks in results.values()) for results in student_info['semesters'].values())
                    total_subjects = sum(len(results) for results in student_info['semesters'].values())
                    if total_subjects > 0:
                        percentage = (total_marks / (total_subjects * 100)) * 100
                        st.write(f"**Total Marks:** {total_marks}")
                        st.write(f"**Percentage:** {percentage:.2f}%")
                    else:
                        st.write("No results available.")

                with col2:
                    st.subheader("Photo")
                    if student_info['image'] is not None:
                        image = Image.open(student_info['image'])
                        st.image(image, use_column_width=True)
                    else:
                        st.write("No photo uploaded.")

    # Display first student by total marks
    if st.button("Show First Student"):
        if student_data:
            first_student = max(student_data.items(), key=lambda x: sum(sum(res.values()) for res in x[1]['semesters'].values()))
            info = first_student[1]
            st.write(f"First Student: {info['name']} (Roll: {first_student[0]}, Branch: {info['branch']})")
        else:
            st.warning("No data available.")
else:
    st.warning("Incorrect password. Please try again.")
