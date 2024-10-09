import streamlit as st
import time

# App Title
st.title("Stop/Start Timer")

# Initialize state variables for tracking time
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# Function to start the timer
def start_timer():
    if not st.session_state.is_running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.is_running = True

# Function to stop the timer
def stop_timer():
    if st.session_state.is_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.is_running = False

# Function to reset the timer
def reset_timer():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.is_running = False

# Display buttons for controlling the timer
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start", on_click=start_timer):
        pass
with col2:
    if st.button("Stop", on_click=stop_timer):
        pass
with col3:
    if st.button("Reset", on_click=reset_timer):
        pass

# Display the timer
if st.session_state.is_running:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time

st.write(f"Elapsed Time: {st.session_state.elapsed_time:.2f} seconds")
