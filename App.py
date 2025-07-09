import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Page configuration
st.set_page_config(page_title="🎥 Live Webcam Preview", layout="centered")
st.title("🎥 Live Webcam Preview in Streamlit")
st.header("📷 Your Live Camera Feed")

# Optional: Define a transformer if you want to process video frames
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Return the original frame or modify it
        return frame

# Correct usage: no 'video' parameter; use media_stream_constraints
webrtc_streamer(
    key="example",
    video_transformer_factory=VideoTransformer,  # Optional: omit if no processing
    media_stream_constraints={"video": True, "audio": False},
)
