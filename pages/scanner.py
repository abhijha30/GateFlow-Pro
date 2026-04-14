import streamlit as st
from utils.db import supabase
import cv2
import numpy as np

def show():

    st.title("📷 QR Scanner (Camera)")

    img_file = st.camera_input("Scan QR Code")

    if img_file is not None:

        # Convert image to OpenCV format
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if data:
            st.success(f"QR Detected: {data}")

            # 🔥 CHECK IN DB
            res = supabase.table("registrations") \
                .select("*") \
                .eq("qr_id", data) \
                .execute()

            if res.data:

                user = res.data[0]

                if user.get("checked_in"):
                    st.warning("⚠ Already Entered")
                else:
                    supabase.table("registrations").update({
                        "checked_in": True
                    }).eq("id", user["id"]).execute()

                    st.success(f"✅ Entry Allowed: {user['name']}")

            else:
                st.error("❌ Invalid QR")

        else:
            st.error("❌ No QR detected")
