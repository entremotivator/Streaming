import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="🎥 Live Webcam Preview", layout="centered")
st.title("🎥 Live Webcam Preview in Streamlit")

st.header("📷 Your Live Camera Feed")

webrtc_streamer(
    key="example",
    video=True,
    audio=False,  # Set to True if you want to capture audio as well
)

st.markdown("---")
st.markdown("""
**Note:**  
This app shows a live webcam feed in your browser.  
It does NOT broadcast or stream your video to YouTube, Twitch, or any other platform.
""")
