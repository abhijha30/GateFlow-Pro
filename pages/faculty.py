import streamlit as st
import uuid
from utils.qr import generate_qr
from utils.mail import send_qr
from utils.db import supabase
import base64

# ================= GET EVENTS =================
def get_events():
    return supabase.table("events").select("*").execute()

# ================= GET REGISTRATIONS =================
def get_registrations(event_id):
    return supabase.table("registrations") \
        .select("*") \
        .eq("event_id", event_id) \
        .execute()

# ================= UPDATE STATUS =================
def update_status(user_id, status):
    return supabase.table("registrations") \
        .update({"status": status}) \
        .eq("id", user_id) \
        .execute()

# ================= MAIN =================
def show():

    if "user" not in st.session_state:
        st.warning("Login first")
        return

    st.markdown("## 🛠 Faculty Dashboard")

    # ================= CREATE EVENT =================
    st.subheader("📅 Create Event")

    name = st.text_input("Event Name")
    venue = st.text_input("Venue")
    capacity = st.number_input("Capacity", min_value=1)

    poster = st.file_uploader("Upload Poster", type=["png","jpg","jpeg"])

    if st.button("Create Event", use_container_width=True):

        poster_data = None
        if poster:
            poster_data = base64.b64encode(poster.read()).decode()

        supabase.table("events").insert({
            "name": name,
            "venue": venue,
            "capacity": int(capacity),
            "poster": poster_data
        }).execute()

        st.success("✅ Event Created")
        st.rerun()

    st.divider()

    # ================= EVENT FILTER =================
    st.subheader("📊 Registrations")

    events = get_events().data or []

    if not events:
        st.info("No events available")
        return

    event_map = {e["name"]: e["id"] for e in events}

    selected_event_name = st.selectbox("Select Event", list(event_map.keys()))
    selected_event_id = event_map[selected_event_name]

    # ✅ CORRECT INDENTATION STARTS HERE
    data = get_registrations(selected_event_id).data or []

    if not data:
        st.info("No registrations for this event")
        return

    # ================= REGISTRATION LIST =================
    for i, u in enumerate(data, start=1):

        st.markdown(f"""
        **{i}. 👤 {u.get('name','N/A')}**  
        📧 {u.get('email','')}  
        🎓 {u.get('course','')}  
        📌 Status: {u.get('status','pending')}
        """)

        col1, col2 = st.columns(2)

        if col1.button("✅ Approve", key=f"a_{u['id']}"):

    try:
        # 🔥 Generate unique QR
        qr_id = str(uuid.uuid4())

        # 🔥 Generate QR image
        qr_path = generate_qr(qr_id)

        # 🔥 Update DB
        supabase.table("registrations").update({
            "status": "approved",
            "qr_id": qr_id
        }).eq("id", u["id"]).execute()

        # 🔥 SEND EMAIL
        send_qr(u["email"], qr_path)

        st.success("✅ Approved & Mail Sent")

    except Exception as e:
        st.error(f"Error: {e}")

    st.rerun()

        if col2.button("❌ Reject", key=f"r_{u['id']}"):
            update_status(u["id"], "rejected")
            st.error("Rejected")
            st.rerun()

        st.divider()
