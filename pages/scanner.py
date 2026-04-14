import streamlit as st
from utils.db import supabase
import av
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from datetime import datetime

# ================= QR SCANNER CLASS =================
class QRScanner(VideoTransformerBase):
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        data, bbox, _ = self.detector.detectAndDecode(img)

        if data:
            st.session_state["scanned_qr"] = data

        return img


# ================= MAIN =================
def show():

    st.title("📷 Auto QR Scanner")

    # 🔥 SELECT EVENT
    events = supabase.table("events").select("*").execute().data or []

    if not events:
        st.warning("No events")
        return

    event_map = {e["name"]: e["id"] for e in events}
    selected_event = st.selectbox("🎯 Select Event", list(event_map.keys()))
    event_id = event_map[selected_event]

    # 🔥 LIVE COUNT
    total = supabase.table("registrations") \
        .select("*", count="exact") \
        .eq("event_id", event_id) \
        .execute()

    checked = supabase.table("registrations") \
        .select("*", count="exact") \
        .eq("event_id", event_id) \
        .eq("checked_in", True) \
        .execute()

    st.markdown(f"""
    ### 📊 Live Stats  
    ✅ Checked In: {checked.count}  
    👥 Total: {total.count}
    """)

    st.divider()

    # 🔥 CAMERA STREAM
    webrtc_streamer(
        key="scanner",
        video_transformer_factory=QRScanner,
        media_stream_constraints={"video": True, "audio": False},
    )

    # 🔥 AUTO DETECT RESULT
    qr_data = st.session_state.get("scanned_qr")

    if qr_data:

        st.success(f"QR Detected: {qr_data}")

       try:
    res = supabase.table("registrations") \
        .select("*") \
        .eq("qr_id", qr_data) \
        .execute()

    if not res.data:
        st.error("❌ Invalid QR")
        return

    user = res.data[0]

except Exception as e:
    st.error(f"DB Error: {e}")
    return
            user = res.data[0]

            if user.get("checked_in"):
                st.warning(f"⚠ Already Entered: {user['name']}")
            else:
                supabase.table("registrations").update({
                    "checked_in": True,
                    "scanned_at": datetime.now().isoformat()
                }).eq("id", user["id"]).execute()

                # 🔊 BEEP
                st.markdown("""
                <audio autoplay>
                    <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
                </audio>
                """, unsafe_allow_html=True)

                st.success(f"""
                ✅ ENTRY ALLOWED  

                👤 {user['name']}  
                📧 {user['email']}  
                🎯 Event: {selected_event}
                """)

                st.balloons()

                # reset QR to avoid multiple scans
                st.session_state["scanned_qr"] = None

        else:
            st.error("❌ Invalid QR")
