import streamlit as st
from datetime import datetime, date
import pandas as pd
import pickle
import os

# Define a file to save events
EVENTS_FILE = 'events.pkl'

# Load events from the pickle file
def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'rb') as f:
            return pickle.load(f)
    return []

# Save events to the pickle file
def save_events(events):
    with open(EVENTS_FILE, 'wb') as f:
        pickle.dump(events, f)

# Ensure session state exists for necessary variables
if 'events' not in st.session_state:
    st.session_state.events = load_events()
if 'age_history' not in st.session_state:
    st.session_state.age_history = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Function to check password
def check_password():
    password = st.sidebar.text_input("Password", type="password")
    if password == "907618125620":  # Change this to your desired password
        return True
    st.sidebar.warning("Please enter the correct password.")
    return False

# Event management functions
def add_event(event_date, event_name, reminder_type):
    st.session_state.events.append({
        'date': event_date,
        'name': event_name,
        'reminder': reminder_type
    })
    save_events(st.session_state.events)
    st.success(f"Event '{event_name}' added on {event_date}.")

def delete_event(selected_date, event_name):
    events_to_delete = [event for event in st.session_state.events if event['date'] == selected_date and event['name'] == event_name]
    if events_to_delete:
        for event in events_to_delete:
            st.session_state.events.remove(event)
        save_events(st.session_state.events)
        st.success(f"Event(s) '{event_name}' on {selected_date} deleted.")
    else:
        st.error("No matching event found to delete.")

def view_events(selected_date):
    events_on_date = [event for event in st.session_state.events if event['date'] == selected_date]
    if events_on_date:
        for event in events_on_date:
            st.write(f"{event['name']} on {event['date']} - Reminder: {event['reminder']}")
    else:
        st.write(f"No events on {selected_date}.")

def search_event(search_query):
    found_events = [event for event in st.session_state.events if search_query.lower() in event['name'].lower()]
    if found_events:
        for event in found_events:
            st.write(f"{event['name']} on {event['date']} - Reminder: {event['reminder']}")
    else:
        st.write("No events found.")

# Age calculation functions
def calculate_age(dob):
    today = date.today()
    birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    st.session_state.age_history.append({'date': today.strftime("%Y-%m-%d"), 'age': age})
    st.success(f"Calculated age: {age} years.")

def calculate_age_between(dob1, dob2):
    dob1 = datetime.strptime(dob1, "%Y-%m-%d").date()
    dob2 = datetime.strptime(dob2, "%Y-%m-%d").date()
    age1 = date.today().year - dob1.year - ((date.today().month, date.today().day) < (dob1.month, dob1.day))
    age2 = date.today().year - dob2.year - ((date.today().month, date.today().day) < (dob2.month, dob2.day))
    return age1, age2

# Reminders functions
def show_reminders():
    if st.session_state.reminders:
        for reminder in st.session_state.reminders:
            st.write(reminder)
    else:
        st.write("No reminders set.")


# Astrology function
def determine_astrological_sign(dob):
    dob = datetime.strptime(dob, "%Y-%m-%d")
    if dob.month == 1:
        return "Capricorn" if dob.day < 20 else "Aquarius"
    elif dob.month == 2:
        return "Aquarius" if dob.day < 18 else "Pisces"
    elif dob.month == 3:
        return "Pisces" if dob.day < 20 else "Aries"
    elif dob.month == 4:
        return "Aries" if dob.day < 20 else "Taurus"
    elif dob.month == 5:
        return "Taurus" if dob.day < 21 else "Gemini"
    elif dob.month == 6:
        return "Gemini" if dob.day < 21 else "Cancer"
    elif dob.month == 7:
        return "Cancer" if dob.day < 23 else "Leo"
    elif dob.month == 8:
        return "Leo" if dob.day < 23 else "Virgo"
    elif dob.month == 9:
        return "Virgo" if dob.day < 23 else "Libra"
    elif dob.month == 10:
        return "Libra" if dob.day < 23 else "Scorpio"
    elif dob.month == 11:
        return "Scorpio" if dob.day < 22 else "Sagittarius"
    else:
        return "Sagittarius"

# Main application logic
def main():
    st.title("Event and Age Tracker")

    if check_password():
        st.sidebar.header("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Event Management", "Age Calculation", "Reminders", "Astrology"])

        # Home page
        if page == "Home":
            st.write("Welcome to the Event and Age Tracker application!")

        # Event management page
        elif page == "Event Management":
            st.subheader("Manage Events")
            event_date = st.date_input("Select event date", datetime.today())
            event_name = st.text_input("Event Name")
            reminder_type = st.selectbox("Set Reminder", ["None", "1 Day", "1 Week"])

            if st.button("Add Event"):
                add_event(event_date, event_name, reminder_type)

            # Display existing events
            selected_date = st.date_input("Select date to view events", datetime.today())
            if st.button("View Events"):
                view_events(selected_date)

            # Deleting events by name and date
            if st.session_state.events:
                event_to_delete = st.selectbox("Select event to delete", options=[f"{event['name']} on {event['date']}" for event in st.session_state.events])
                if st.button("Delete Event"):
                    event_name = event_to_delete.split(' on ')[0]
                    event_date_str = event_to_delete.split(' on ')[1]
                    delete_event(datetime.strptime(event_date_str, '%Y-%m-%d').date(), event_name)
            else:
                st.write("No events to delete.")

            search_query = st.text_input("Search for an event")
            if st.button("Search Event"):
                if search_query:
                    search_event(search_query)

        # Age calculation page
        elif page == "Age Calculation":
            st.subheader("Calculate Age")
            dob = st.date_input("Enter Date of Birth")
            if st.button("Calculate Age"):
                calculate_age(dob.strftime("%Y-%m-%d"))

            st.subheader("Age History")
            if st.session_state.age_history:
                for entry in st.session_state.age_history:
                    st.write(f"{entry['date']}: {entry['age']} years old")

            st.subheader("Calculate Age Between Two Persons")
            dob1 = st.date_input("Enter Date of Birth for Person 1", key="dob1")
            dob2 = st.date_input("Enter Date of Birth for Person 2", key="dob2")
            if st.button("Calculate Ages"):
                age1, age2 = calculate_age_between(dob1.strftime("%Y-%m-%d"), dob2.strftime("%Y-%m-%d"))
                st.success(f"Person 1 is {age1} years old and Person 2 is {age2} years old.")

        # Reminders page
        elif page == "Reminders":
            st.subheader("Set Reminders")
            reminder = st.text_input("Enter Reminder")
            if st.button("Add Reminder"):
                st.session_state.reminders.append(reminder)
                st.success("Reminder added!")
                show_reminders()
            st.write("Reminders List:")
            show_reminders()

        # Astrology page
        elif page == "Astrology":
            st.subheader("Determine Astrological Sign")
            dob_for_astrology = st.date_input("Enter Date of Birth for Astrology")
            if st.button("Get Astrological Sign"):
                sign = determine_astrological_sign(dob_for_astrology.strftime("%Y-%m-%d"))
                st.success(f"Your astrological sign is: {sign}")

if __name__ == "__main__":
    main()
