import streamlit as st
from utils.db import supabase
import cv2
import numpy as np

def show():

    st.title("📷 GateFlow Scanner")

    # 🔥 SELECT EVENT
    events = supabase.table("events").select("*").execute().data or []

    if not events:
        st.warning("No events found")
        return

    event_map = {e["name"]: e["id"] for e in events}
    selected_event = st.selectbox("🎯 Select Event", list(event_map.keys()))
    event_id = event_map[selected_event]

    # 🔥 LIVE COUNTER
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
    👥 Total Registered: {total.count}
    """)

    st.divider()

    # 🔥 CAMERA
    img_file = st.camera_input("📷 Scan QR Code")

    if img_file is not None:

        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if data:

            st.success(f"🎯 QR Detected")

            # 🔥 CHECK DB
            res = supabase.table("registrations") \
                .select("*") \
                .eq("qr_id", data) \
                .eq("event_id", event_id) \
                .execute()

            if res.data:

                user = res.data[0]

                if user.get("checked_in"):
                    st.warning(f"⚠ Already Entered: {user['name']}")
                else:
                    supabase.table("registrations").update({
                        "checked_in": True
                    }).eq("id", user["id"]).execute()

                    # 🔊 BEEP SOUND
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

                    st.rerun()

            else:
                st.error("❌ Invalid QR for this event")

        else:
            st.error("❌ No QR detected")
