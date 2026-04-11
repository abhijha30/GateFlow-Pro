import streamlit as st
from utils.db import *

def show():

    if "user" not in st.session_state:
        st.warning("Login first")
        return

    user = st.session_state["user"]

    st.markdown(f"## 🎓 Welcome {user['name']}")

    events = get_events().data or []

    if not events:
        st.info("No events")
        return

    # 🔍 SEARCH
    search = st.text_input("🔍 Search Event")

    filtered = [e for e in events if search.lower() in e["name"].lower()]

    for e in filtered:

        if st.button(f"🎯 {e['name']} - Register", key=e["id"]):

            st.session_state["selected_event"] = e

    # 📝 FORM AFTER CLICK
    if "selected_event" in st.session_state:

        e = st.session_state["selected_event"]

        st.markdown(f"### 📝 Register for {e['name']}")

        mobile = st.text_input("Mobile")
        course = st.selectbox("Course", ["BBA","BCA"])
        year = st.selectbox("Year", ["1st","2nd","3rd"])

        if st.button("Submit"):

            register_user({
                "user_id": user["id"],
                "event_id": e["id"],
                "name": user["name"],
                "email": user["email"],
                "mobile": mobile,
                "course": course,
                "year": year,
                "status": "pending"
            })

            st.success("✅ Applied")

    # 📊 TRACK
    st.markdown("### 📊 My Applications")

    data = get_all().data or []
    my = [d for d in data if d["email"] == user["email"]]

    for r in my:
        st.write(f"{r['event_id']} - {r['status']}")
