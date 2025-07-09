import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="🎥 Live Webcam Preview", layout="centered")
st.title("🎥 Live Webcam Preview in Streamlit")

st.header("📷 Your Live Camera Feed")

# The function must be called inside the script, not at the top level or inside __main__
webrtc_streamer(
    key="example",
    video=True,
    audio=False,
)
