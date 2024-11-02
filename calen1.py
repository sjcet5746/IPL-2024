import streamlit as st
from datetime import datetime, timedelta

# Initialize dictionary to store events
if "events" not in st.session_state:
    st.session_state["events"] = {}

# Function to add an event
def add_event(date, event_name):
    if date in st.session_state["events"]:
        st.session_state["events"][date].append(event_name)
    else:
        st.session_state["events"][date] = [event_name]
    st.success("Event added successfully!")

# Function to delete an event
def delete_event(date, event_index):
    if date in st.session_state["events"]:
        st.session_state["events"][date].pop(event_index)
        if not st.session_state["events"][date]:  # Remove date if no events left
            del st.session_state["events"][date]
        st.success("Event deleted successfully!")
    else:
        st.warning("No events found on this date.")

# Function to view all events
def view_events():
    if not st.session_state["events"]:
        st.info("No events available.")
    else:
        for date, event_list in sorted(st.session_state["events"].items()):
            st.write(f"**Date:** {date}")
            for event in event_list:
                st.write(f"  - {event}")

# Function to search for an event
def search_event(query):
    found = False
    for date, event_list in st.session_state["events"].items():
        for event in event_list:
            if query.lower() in event.lower():
                st.write(f"Event found on {date}: {event}")
                found = True
    if not found:
        st.warning("No matching events found.")

# Function to calculate age
def calculate_age(dob):
    try:
        dob = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        st.error("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    today = datetime.today()
    age_years = today.year - dob.year
    age_months = today.month - dob.month
    age_days = today.day - dob.day

    # Adjust months and days if negative
    if age_days < 0:
        age_days += (dob + timedelta(days=30)).day
        age_months -= 1
    if age_months < 0:
        age_months += 12
        age_years -= 1

    # Calculate total days
    total_days = (today - dob).days

    st.write(f"**Your age is:** {age_years} years, {age_months} months, and {age_days} days.")
    st.write(f"**Total days:** {total_days}")

# Streamlit layout
st.title("📅 Calendar App")

# Add Event Section
st.header("Add Event")
date = st.date_input("Select event date:")
event_name = st.text_input("Enter event name")
if st.button("Add Event"):
    if date and event_name:
        add_event(date.strftime("%Y-%m-%d"), event_name)
    else:
        st.warning("Please enter both date and event name.")

# Delete Event Section
st.header("Delete Event")
delete_date = st.date_input("Select date to delete event:")
if delete_date.strftime("%Y-%m-%d") in st.session_state["events"]:
    events_on_date = st.session_state["events"][delete_date.strftime("%Y-%m-%d")]
    event_to_delete = st.selectbox("Select event to delete", events_on_date)
    if st.button("Delete Event"):
        event_index = events_on_date.index(event_to_delete)
        delete_event(delete_date.strftime("%Y-%m-%d"), event_index)
else:
    st.info("No events on this date.")

# View All Events Section
st.header("View All Events")
if st.button("Show All Events"):
    view_events()

# Search Event Section
st.header("Search Event")
search_query = st.text_input("Enter event name to search")
if st.button("Search Event"):
    if search_query:
        search_event(search_query)
    else:
        st.warning("Please enter an event name to search.")

# Age Calculation Section
st.header("Calculate Age")
dob = st.text_input("Enter your Date of Birth (YYYY-MM-DD)")
if st.button("Calculate Age"):
    if dob:
        calculate_age(dob)
    else:
        st.warning("Please enter your date of birth.")
