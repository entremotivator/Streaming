import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2
import numpy as np

# --- Page configuration ---
st.set_page_config(
    page_title="🎥 Live Webcam Preview",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🎥 Live Webcam Preview in Streamlit")
st.header("📷 Your Live Camera Feed")
st.markdown(
    """
    This app lets you preview your webcam feed **live** in your browser, with optional real-time processing.
    - Click **Start** to begin streaming.
    - Use the sidebar to toggle effects.
    """
)

# --- Sidebar controls ---
st.sidebar.title("Video Options")
flip_video = st.sidebar.checkbox("Flip Video Vertically")
grayscale = st.sidebar.checkbox("Convert to Grayscale")
show_edges = st.sidebar.checkbox("Show Canny Edges")

st.sidebar.markdown("---")
st.sidebar.info(
    "If the webcam does not appear, check your browser permissions and reload the page. "
    "For deployments on Streamlit Cloud, TURN server configuration may be required for WebRTC to work properly."
)

# --- Video transformer class ---
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Apply effects based on user selection
        if flip_video:
            img = np.flipud(img)
        if grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if show_edges:
            edges = cv2.Canny(img, 100, 200)
            img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return img

# --- Start the webcam stream ---
webrtc_streamer(
    key="live-webcam",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# --- Additional instructions and troubleshooting ---
st.markdown(
    """
    ---
    ### ℹ️ How to use this app
    1. **Allow camera access** when prompted by your browser.
    2. Use the sidebar to toggle video effects in real time.
    3. If you see a blank screen:
        - Make sure your webcam is connected and not used by another app.
        - Reload the page and allow permissions again.
        - For cloud deployments, [TURN server setup](https://github.com/whitphx/streamlit-webrtc#configure-the-turn-server-if-necessary) may be needed[4][6].
    ---
    """
)
