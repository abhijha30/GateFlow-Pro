import streamlit as st

def show():

    st.markdown("## 📱 QR Scanner")

    qr = st.text_input("Scan QR Code")

    if st.button("Verify"):

        if qr:
            st.success("✅ Valid Pass")
        else:
            st.error("❌ Invalid")
