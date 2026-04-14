import streamlit as st
from utils.db import supabase
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from datetime import datetime

# ================= QR SCANNER =================
class QRScanner(VideoTransformerBase):
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        data, bbox, _ = self.detector.detectAndDecode(img)

        if data and "scanned_qr" not in st.session_state:
            st.session_state["scanned_qr"] = data

        return img


# ================= MAIN =================
def show():

    st.title("📷 GateFlow Scanner")

    # 🔥 SELECT EVENT
    events = supabase.table("events").select("*").execute().data or []

    if not events:
        st.warning("No events")
        return

    event_map = {e["name"]: e["id"] for e in events}
    selected_event = st.selectbox("🎯 Select Event", list(event_map.keys()))
    event_id = event_map[selected_event]

    st.divider()

    # 🔥 START / STOP CONTROL
    if "scanner_on" not in st.session_state:
        st.session_state["scanner_on"] = False

    col1, col2 = st.columns(2)

    if col1.button("▶ Start Scanner"):
        st.session_state["scanner_on"] = True

    if col2.button("⏹ Stop Scanner"):
        st.session_state["scanner_on"] = False

    # 🔥 CAMERA STREAM
    if st.session_state["scanner_on"]:
        webrtc_streamer(
            key="scanner",
            video_transformer_factory=QRScanner,
            media_stream_constraints={"video": True, "audio": False},
        )

    # 🔥 QR RESULT
    qr_data = st.session_state.get("scanned_qr")

    if qr_data:

        try:
            res = supabase.table("registrations") \
                .select("*") \
                .eq("qr_id", qr_data) \
                .eq("event_id", event_id) \
                .execute()

            if not res.data:
                st.error("❌ Invalid QR")
                return

            user = res.data[0]

        except Exception as e:
            st.error(f"DB Error: {e}")
            return

        # 🔥 STOP CAMERA AFTER SCAN
        st.session_state["scanner_on"] = False

        # 🔥 CHECK ENTRY
        if user.get("checked_in"):
            st.warning(f"⚠ Already Present: {user['name']}")
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

            # 🎯 SHOW DETAILS
            st.success(f"""
            ✅ ENTRY MARKED  

            👤 Name: {user['name']}  
            📧 Email: {user['email']}  
            🎓 Course: {user.get('course','')}  
            🎯 Event: {selected_event}
            """)

        # 🔥 RESET BUTTON
        if st.button("🔄 Scan Next Student"):
            st.session_state["scanned_qr"] = None
            st.session_state["scanner_on"] = True
            st.rerun()
