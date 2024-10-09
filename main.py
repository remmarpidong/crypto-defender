import streamlit as st
import time

def stop_start_timer():
  start_time = None
  elapsed_time = 0

  while True:
    if start_time is None:
      if st.button("Start Timer"):
        start_time = time.time()
    else:
      elapsed_time = time.time() - start_time
      if st.button("Stop Timer"):
        start_time = None
      st.write(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
  stop_start_timer()
