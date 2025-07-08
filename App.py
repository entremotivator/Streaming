# stream_to_socials.py

import streamlit as st
from obswebsocket import obsws, requests

# Streamlit UI
st.title("🎥 Multi-Platform Streaming with OBS + RTMP Keys")

st.markdown("Enter your RTMP URLs or Stream Keys below:")

platforms = {
    "YouTube": "",
    "Facebook": "",
    "Twitch": "",
    "Twitter (X)": "",
    "LinkedIn": ""
}

rtmp_inputs = {}
for platform in platforms:
    rtmp_inputs[platform] = st.text_input(f"{platform} RTMP URL/Key", type="password")

# OBS WebSocket connection settings
obs_host = st.text_input("OBS Host", "localhost")
obs_port = st.number_input("OBS Port", 4455)
obs_password = st.text_input("OBS WebSocket Password", type="password")

if st.button("Start Streaming to All Platforms"):
    try:
        ws = obsws(obs_host, obs_port, obs_password)
        ws.connect()
        st.success("Connected to OBS!")

        for platform, rtmp in rtmp_inputs.items():
            if rtmp.strip() != "":
                st.write(f"Setting up stream for {platform}...")

                # Create a new RTMP output (one per platform)
                response = ws.call(requests.CreateOutput(
                    outputName=f"{platform}_output",
                    outputKind="rtmp_output",
                    outputSettings={
                        "server": rtmp,  # Full RTMP URL with stream key
                        "key": "",       # Leave empty if included in server URL
                        "use_auth": False
                    }
                ))

                # Start streaming to this output
                ws.call(requests.StartOutput(f"{platform}_output"))
                st.success(f"Streaming started to {platform} ✅")

        ws.disconnect()
        st.success("✅ Streaming to all configured platforms!")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
