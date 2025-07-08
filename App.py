import streamlit as st
from obswebsocket import obsws, requests, exceptions
import time

# ----------- Constants -----------
PLATFORMS = {
    "YouTube": "",
    "Facebook": "",
    "Twitch": "",
    "Twitter (X)": "",
    "LinkedIn": ""
}

# ----------- Session State Init -----------
if 'obs' not in st.session_state:
    st.session_state.obs = None
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'stream_status' not in st.session_state:
    st.session_state.stream_status = {p: "🔴 Stopped" for p in PLATFORMS}
if 'saved_rtmps' not in st.session_state:
    st.session_state.saved_rtmps = {p: "" for p in PLATFORMS}

# ----------- App Layout -----------
st.set_page_config(page_title="OBS Multi-Streaming Studio", layout="centered")
st.title("🎥 OBS Multi-Streaming Studio")
st.markdown("Control streaming to multiple platforms from your OBS with just a few clicks.")

# ----------- Sidebar: OBS Settings -----------
with st.sidebar:
    st.header("🔌 OBS WebSocket Settings")
    host = st.text_input("Host", "localhost")
    port = st.number_input("Port", 4455)
    password = st.text_input("Password", type="password")
    
    connect_button = st.button("Connect to OBS")

    if connect_button:
        try:
            st.session_state.obs = obsws(host, port, password)
            st.session_state.obs.connect()
            st.session_state.connected = True
            st.success("✅ Connected to OBS")
        except exceptions.OBSSDKError as e:
            st.session_state.connected = False
            st.error(f"❌ Failed to connect: {e}")
        except Exception as e:
            st.session_state.connected = False
            st.error(f"❌ Error: {e}")

    if st.session_state.connected:
        st.success("🟢 OBS Connection Active")
    else:
        st.warning("🔴 Not connected to OBS")

# ----------- Stream Target Input -----------
st.subheader("🎯 Configure RTMP Endpoints")

with st.expander("📺 RTMP Stream Key Inputs"):
    for platform in PLATFORMS:
        value = st.text_input(
            f"{platform} RTMP URL + Stream Key",
            value=st.session_state.saved_rtmps.get(platform, ""),
            key=f"rtmp_{platform}",
            type="password",
            help="Example: rtmp://a.rtmp.youtube.com/live2/your_stream_key"
        )
        st.session_state.saved_rtmps[platform] = value.strip()

# ----------- Streaming Controls -----------
st.subheader("🧪 Stream Control Panel")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start All Active Streams") and st.session_state.connected:
        for platform, url in st.session_state.saved_rtmps.items():
            if url.strip() == "":
                continue

            output_name = f"{platform}_Output"

            try:
                # Clean up any existing outputs
                try:
                    st.session_state.obs.call(requests.StopOutput(output_name))
                    st.session_state.obs.call(requests.RemoveOutput(output_name))
                except:
                    pass

                # Create and start output
                st.session_state.obs.call(requests.CreateOutput(
                    outputName=output_name,
                    outputKind="rtmp_output",
                    outputSettings={
                        "server": url,
                        "key": "",
                        "use_auth": False
                    }
                ))

                st.session_state.obs.call(requests.StartOutput(output_name))
                st.session_state.stream_status[platform] = "🟢 Live"
                st.success(f"{platform}: Streaming started ✅")

            except Exception as e:
                st.session_state.stream_status[platform] = "🔴 Failed"
                st.error(f"{platform} Error: {e}")

with col2:
    if st.button("🛑 Stop All Streams") and st.session_state.connected:
        for platform in PLATFORMS:
            output_name = f"{platform}_Output"
            try:
                st.session_state.obs.call(requests.StopOutput(output_name))
                st.session_state.obs.call(requests.RemoveOutput(output_name))
                st.session_state.stream_status[platform] = "🔴 Stopped"
                st.warning(f"{platform}: Stream stopped")
            except Exception as e:
                st.error(f"{platform}: Couldn't stop stream ({e})")

# ----------- Stream Status Summary -----------
st.subheader("📡 Stream Status")

for platform in PLATFORMS:
    st.markdown(f"**{platform}:** {st.session_state.stream_status[platform]}")

# ----------- Info Footer -----------
st.markdown("---")
st.caption("🧠 Tip: OBS WebSocket must be enabled. Default port is 4455 with optional password.")
