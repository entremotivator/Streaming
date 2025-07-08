import streamlit as st
import os
from obswebsocket import obsws, requests
import time

# Constants
VIDEO_FOLDER = "uploaded_videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

st.set_page_config(page_title="📼 Video Broadcaster", layout="centered")
st.title("📼 Live Stream a Prerecorded Video")

# 1. Video Upload and Preview
st.header("🎞️ Upload or Select a Video")
video_file = st.file_uploader("Upload MP4 file", type=["mp4"])

if video_file:
    video_path = os.path.join(VIDEO_FOLDER, video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    st.video(video_path)
    st.success("✅ Video ready for streaming via OBS")

# 2. OBS WebSocket Settings
st.sidebar.header("🔌 OBS WebSocket Settings")
obs_host = st.sidebar.text_input("OBS Host", "localhost")
obs_port = st.sidebar.number_input("OBS Port", 4455)
obs_password = st.sidebar.text_input("OBS Password", type="password")

# 3. RTMP Inputs
st.header("📡 RTMP Stream Destinations")
platform_rtmp = st.text_input("RTMP URL (with stream key)", help="e.g., rtmp://a.rtmp.youtube.com/live2/yourkey")

# 4. Stream Controls
if st.button("🚀 Start Live Stream in OBS"):
    if not video_file:
        st.warning("Please upload a video first.")
    else:
        try:
            ws = obsws(obs_host, obs_port, obs_password)
            ws.connect()
            st.success("✅ Connected to OBS")

            # Add local video source to a scene
            scene_name = "VideoScene"
            source_name = "StreamVideo"

            # Create scene
            ws.call(requests.CreateScene(scene_name))
            ws.call(requests.SetCurrentProgramScene(scene_name))

            # Add media source
            ws.call(requests.CreateInput(
                sceneName=scene_name,
                inputName=source_name,
                inputKind="ffmpeg_source",
                inputSettings={
                    "local_file": video_path,
                    "looping": False,
                    "is_local_file": True
                }
            ))

            time.sleep(1)

            # Set up RTMP streaming output
            ws.call(requests.SetStreamServiceSett
