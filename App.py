import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2
import numpy as np

# --- Page configuration ---
st.set_page_config(
    page_title="🎥 Live Webcam Preview",
    layout="centered"
)

st.title("🎥 Live Webcam Preview in Streamlit")
st.header("📷 Your Live Camera Feed")
st.markdown(
    """
    This app lets you preview your webcam feed **live** in your browser, with optional real-time processing.<br>
    - Click **Start** to begin streaming.<br>
    - Use the sidebar to toggle effects.<br>
    - **Share this app's link** so anyone can view and use it!
    """,
    unsafe_allow_html=True,
)

# --- Sidebar controls ---
st.sidebar.title("Video Options")
flip_video = st.sidebar.checkbox("Flip Video Vertically")
grayscale = st.sidebar.checkbox("Convert to Grayscale")
show_edges = st.sidebar.checkbox("Show Canny Edges")

st.sidebar.markdown("---")
st.sidebar.info(
    "If the webcam does not appear, check your browser permissions and reload the page. "
    "For cloud deployments, TURN server configuration may be required for WebRTC to work properly."
)

# --- Video transformer class ---
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if flip_video:
            img = np.flipud(img)
        if grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if show_edges:
            edges = cv2.Canny(img, 100, 200)
            img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return img

# --- Start the webcam stream with public STUN server for cloud deployment ---
webrtc_streamer(
    key="live-webcam",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },  # This enables WebRTC to work on public servers
    async_processing=True,
)

st.markdown(
    """
    ---
    ### ℹ️ Deployment Instructions

    - **Deploy this app on [Streamlit Community Cloud](https://share.streamlit.io/)** for a public HTTPS link that anyone can access[1][2].
    - Make sure your `requirements.txt` includes:
        ```
        streamlit
        streamlit-webrtc
        opencv-python-headless
        numpy
        ```
    - After deployment, share the app's URL with others. They can access the webcam preview from anywhere!
    - For advanced usage or issues with connectivity (especially with users behind strict firewalls), consider adding a TURN server to `rtc_configuration`[2].

    ---
    """
)
