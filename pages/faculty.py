import streamlit as st
from utils.db import *
import base64

def show():

    if "user" not in st.session_state:
        st.warning("Login first")
        return

    st.markdown("## 🛠 Faculty Dashboard")

    # CREATE EVENT
    name = st.text_input("Event Name")
    venue = st.text_input("Venue")
    capacity = st.number_input("Capacity", min_value=1)

    poster = st.file_uploader("Poster")

    if st.button("Create Event"):

        poster_data = None
        if poster:
            poster_data = base64.b64encode(poster.read()).decode()

        create_event({
            "name": name,
            "venue": venue,
            "capacity": int(capacity),
            "poster": poster_data
        })

        st.success("Created")

    # VIEW REGISTRATIONS
    st.markdown("### 📊 Registrations")

    data = get_all().data or []

    for u in data:

        st.write(f"{u['name']} - {u['status']}")

        col1, col2 = st.columns(2)

        if col1.button("Approve", key=u["id"]):
            update_status(u["id"], "approved", "qr123")
            st.rerun()

        if col2.button("Reject", key="r"+u["id"]):
            update_status(u["id"], "rejected", "")
            st.rerun()
