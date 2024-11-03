import datetime
import pytz
import streamlit as st
import time

# Define regions and corresponding time zones
REGION_TIMEZONES = {
    "Africa": [
        "Africa/Cairo", "Africa/Johannesburg", "Africa/Lagos", "Africa/Nairobi", "Africa/Accra"
    ],
    "America": [
        "America/New_York", "America/Los_Angeles", "America/Chicago",
        "America/Sao_Paulo", "America/Mexico_City", "America/Denver"
    ],
    "Asia": [
        "Asia/Kolkata", "Asia/Tokyo", "Asia/Shanghai", "Asia/Dubai", "Asia/Bangkok", "Asia/Seoul"
    ],
    "Europe": [
        "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
        "Europe/Rome", "Europe/Amsterdam"
    ],
    "Australia/Oceania": [
        "Australia/Sydney", "Australia/Melbourne", "Pacific/Auckland", "Australia/Perth"
    ],
    "Antarctica": [
        "Antarctica/Casey", "Antarctica/Davis", "Antarctica/McMurdo"
    ]
}

# Configure the page
st.set_page_config(page_title="Enhanced Time Application", layout="wide")

# Title and header
st.title("🌐 Enhanced Time Application")
st.header("Choose your options below to see time in various formats and zones!")

# Sidebar: Show current time on button click
st.sidebar.markdown("### 🕒 Real-Time Clock")
if st.sidebar.button("Show Current Time"):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f"**Current Time:** {current_time}")

# Sidebar: Select a region to filter time zones
st.sidebar.markdown("### 🌍 Select Your Region")
selected_region = st.sidebar.selectbox(
    "Choose a Region/Continent:",
    list(REGION_TIMEZONES.keys())
)

# Sidebar: Select a timezone based on the selected region
filtered_timezones = REGION_TIMEZONES[selected_region]
selected_timezone = st.sidebar.selectbox(
    "Choose a Timezone:",
    filtered_timezones
)

# Sidebar: Select multiple time zones for the World Clock
st.sidebar.markdown("### 🌐 Select Multiple Time Zones for World Clock")
world_clock_timezones = st.sidebar.multiselect(
    "Choose Timezones for World Clock:",
    [tz for sublist in REGION_TIMEZONES.values() for tz in sublist]  # Flatten the list of time zones
)

# Sidebar: Select an option
st.sidebar.markdown("### ⚙️ Options")
option = st.sidebar.selectbox("Choose an option", [
    "Display Current Time",
    "Display Time in a Specific Timezone",
    "Convert Time Format",
    "Set Alarm",
    "World Clock Display",
    "Time Difference Calculator",
    "Countdown Timer",
    "Stopwatch"
])

# Function to get the current time in a specific timezone
def get_current_time_in_timezone(timezone):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Handling each option
if option == "Display Current Time":
    st.subheader("🕰️ Current Time (UTC)")
    st.write(get_current_time_in_timezone("UTC"))

elif option == "Display Time in a Specific Timezone":
    st.subheader(f"🕰️ Current Time in {selected_timezone}")
    st.write(get_current_time_in_timezone(selected_timezone))

elif option == "Convert Time Format":
    st.subheader("🔄 Convert Time Format")
    time_format = st.radio("Choose time format conversion:", ["12-hour to 24-hour", "24-hour to 12-hour"])
    time_str = st.text_input("Enter time (e.g., 02:30 PM or 14:30)")

    if time_format == "12-hour to 24-hour" and time_str:
        try:
            in_time = datetime.datetime.strptime(time_str, "%I:%M %p")
            out_time = in_time.strftime("%H:%M")
            st.success(f"**24-hour format:** {out_time}")
        except ValueError:
            st.error("Invalid 12-hour format. Please use `HH:MM AM/PM`.")

    elif time_format == "24-hour to 12-hour" and time_str:
        try:
            in_time = datetime.datetime.strptime(time_str, "%H:%M")
            out_time = in_time.strftime("%I:%M %p")
            st.success(f"**12-hour format:** {out_time}")
        except ValueError:
            st.error("Invalid 24-hour format. Please use `HH:MM`.")

elif option == "Set Alarm":
    st.subheader("⏰ Set an Alarm")
    alarm_time = st.time_input("Select Alarm Time:", datetime.time(0, 0))
    st.session_state.alarm_set = False

    if st.button("Set Alarm"):
        st.session_state.alarm_time = alarm_time
        st.session_state.alarm_set = True
        st.success(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")

    if st.session_state.get('alarm_set', False):
        current_time = datetime.datetime.now().time()
        if current_time >= st.session_state.alarm_time:
            st.warning("⏰ Alarm! Time to wake up!")
            st.session_state.alarm_set = False  # Reset alarm after triggering

elif option == "World Clock Display":
    st.subheader("🌍 World Clock Display")
    if world_clock_timezones:
        st.write("### Current Times in Selected Time Zones:")
        for timezone in world_clock_timezones:
            st.write(f"**{timezone}:** {get_current_time_in_timezone(timezone)}")
    else:
        st.warning("Please select at least one timezone from the sidebar.")

elif option == "Time Difference Calculator":
    st.subheader("🕒 Time Difference Calculator")
    
    # Select first timezone
    timezone1 = st.selectbox("Select First Time Zone:", [tz for sublist in REGION_TIMEZONES.values() for tz in sublist])
    time1_str = st.text_input("Enter Date and Time in First Time Zone (YYYY-MM-DD HH:MM):")

    # Select second timezone
    timezone2 = st.selectbox("Select Second Time Zone:", [tz for sublist in REGION_TIMEZONES.values() for tz in sublist])
    
    if st.button("Calculate Time Difference"):
        try:
            # Parse the date and time from string
            time1 = datetime.datetime.strptime(time1_str, "%Y-%m-%d %H:%M")
            # Convert the first time to the second time zone
            tz1 = pytz.timezone(timezone1)
            tz2 = pytz.timezone(timezone2)

            # Localize the input time to the first timezone
            local_time1 = tz1.localize(time1)
            # Convert to the second timezone
            time_in_timezone2 = local_time1.astimezone(tz2)

            st.success(f"The corresponding time in {timezone2} is: **{time_in_timezone2.strftime('%Y-%m-%d %H:%M:%S')}**")
        except ValueError:
            st.error("Invalid date and time format. Please use `YYYY-MM-DD HH:MM`.")

elif option == "Countdown Timer":
    st.subheader("⏳ Countdown Timer")
    
    # Countdown timer state
    if 'countdown_time' not in st.session_state:
        st.session_state.countdown_time = 0  # Initialize countdown time
        st.session_state.is_running = False  # Initialize running state

    # Input for countdown duration
    countdown_duration = st.number_input("Enter countdown duration in seconds:", min_value=1, step=1)

    # Start/Stop buttons
    if st.button("Start Countdown"):
        st.session_state.countdown_time = countdown_duration
        st.session_state.is_running = True

    if st.button("Stop Countdown"):
        st.session_state.is_running = False

    # Countdown logic using a placeholder
    countdown_placeholder = st.empty()

    while st.session_state.is_running and st.session_state.countdown_time > 0:
        countdown_placeholder.write(f"**Time Remaining:** {st.session_state.countdown_time} seconds")
        time.sleep(1)  # Wait for a second
        st.session_state.countdown_time -= 1  # Decrease the remaining time
    
    # If countdown has finished
    if st.session_state.is_running and st.session_state.countdown_time == 0:
        countdown_placeholder.write("**Time's up!**")
        st.session_state.is_running = False  # Stop the countdown when time is up

elif option == "Stopwatch":
    st.subheader("⏱️ Stopwatch")

    # Stopwatch state
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0  # Elapsed time in seconds
        st.session_state.is_running_stopwatch = False  # Initialize running state

    # Start/Stop buttons
    start_button = st.button("Start Stopwatch")
    stop_button = st.button("Stop Stopwatch")
    reset_button = st.button("Reset Stopwatch")

    if start_button and not st.session_state.is_running_stopwatch:
        st.session_state.is_running_stopwatch = True

    if stop_button and st.session_state.is_running_stopwatch:
        st.session_state.is_running_stopwatch = False

    if reset_button:
        st.session_state.elapsed_time = 0  # Reset elapsed time
        st.session_state.is_running_stopwatch = False  # Ensure stopwatch is not running

    # Update elapsed time display
    if st.session_state.is_running_stopwatch:
        start_time = time.time()
        while st.session_state.is_running_stopwatch:
            elapsed = int(time.time() - start_time + st.session_state.elapsed_time)  # Calculate elapsed time
            st.write(f"**Elapsed Time:** {int(elapsed // 3600)}:{int((elapsed % 3600) // 60):02}:{int(elapsed % 60):02}")  # Display time in HH:MM:SS
            time.sleep(1)  # Update every second
            st.session_state.elapsed_time = elapsed  # Update the elapsed time

    else:
        st.write(f"**Elapsed Time:** {int(st.session_state.elapsed_time // 3600)}:{int((st.session_state.elapsed_time % 3600) // 60):02}:{int(st.session_state.elapsed_time % 60):02}")  # Display time in HH:MM:SS
