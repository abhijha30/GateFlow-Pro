import streamlit as st
from utils.db import supabase, create_event, update_status
import base64
import uuid

# 🔹 GET EVENTS
def get_events():
    return supabase.table("events").select("*").execute()

# 🔹 GET REGISTRATIONS (EVENT-WISE)
def get_registrations(event_id):
    return supabase.table("registrations") \
        .select("*") \
        .eq("event_id", event_id) \
        .execute()


def show():

    # 🔐 LOGIN CHECK
    if "user" not in st.session_state:
        st.warning("Login first")
        return

    st.markdown("## 🛠 Faculty Dashboard")

    # ================== CREATE EVENT ==================
    st.markdown("### 📅 Create Event")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Event Name")
        venue = st.text_input("Venue")

    with col2:
        capacity = st.number_input("Capacity", min_value=1)

    poster = st.file_uploader("Upload Poster", type=["png", "jpg", "jpeg"])

    if st.button("Create Event", use_container_width=True):

        if not name or not venue:
            st.warning("Fill all fields")
            return

        poster_data = None
        if poster:
            poster_data = base64.b64encode(poster.read()).decode()

        create_event({
            "name": name,
            "venue": venue,
            "capacity": int(capacity),
            "poster": poster_data
        })

        st.success("✅ Event Created")
        st.rerun()

    st.divider()

    # ================== EVENT FILTER ==================
    st.markdown("### 📊 Registrations")

    events = get_events().data or []

    if not events:
        st.info("No events available")
        return

    event_names = [e["name"] for e in events]

    selected_event = st.selectbox("Filter by Event", event_names)

    data = get_registrations(selected_event).data or []

    if not data:
        st.info("No registrations for this event")
        return

    # ================== STATS ==================
    total = len(data)
    approved = len([u for u in data if u["status"] == "approved"])
    pending = len([u for u in data if u["status"] == "pending"])
    rejected = len([u for u in data if u["status"] == "rejected"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("Approved", approved)
    c3.metric("Pending", pending)
    c4.metric("Rejected", rejected)

    st.divider()

    # ================== LIST ==================
    for u in data:

        st.markdown(f"""
        **👤 {u['name']}**  
        📧 {u['email']}  
        📊 Status: `{u['status']}`
        """)

        if u["status"] == "pending":

            col1, col2 = st.columns(2)

            # ✅ APPROVE
            if col1.button("✅ Approve", key=f"a_{u['id']}"):

                qr_id = str(uuid.uuid4())

                update_status(u["id"], "approved", qr_id)

                st.success("Approved")
                st.rerun()

            # ❌ REJECT
            if col2.button("❌ Reject", key=f"r_{u['id']}"):

                update_status(u["id"], "rejected", "")

                st.error("Rejected")
                st.rerun()

        st.divider()

    # ================== DOWNLOAD ==================
    import pandas as pd

    df = pd.DataFrame(data)

    st.download_button(
        "⬇️ Download Event Data",
        df.to_csv(index=False),
        file_name=f"{selected_event}_registrations.csv",
        key="download_event_data"
    )
