import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Page configuration
st.set_page_config(page_title="🎥 Live Webcam Preview", layout="centered")

st.title("🎥 Live Webcam Preview in Streamlit")
st.header("📷 Your Live Camera Feed")

# Optional: Define a transformer if you want to process the video
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # You can modify the frame here (e.g., grayscale, filters, overlays)
        return frame

# Stream the webcam feed
webrtc_streamer(
    key="live",
    video_transformer_factory=VideoTransformer,  # Optional processing
    media_stream_constraints={"video": True, "audio": False},  # Explicit settings
)
