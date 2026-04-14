import streamlit as st
from utils.db import supabase

# ================= GET EVENTS =================
def get_events():
    return supabase.table("events").select("*").execute()

# ================= GET ALL REGISTRATIONS =================
def get_all():
    return supabase.table("registrations").select("*").execute()

# ================= MAIN =================
def show():

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Login first")
        return

    user = st.session_state["user"]

    st.markdown(f"## 🎓 Welcome {user.get('name', 'User')}")

    events = get_events().data or []

    if not events:
        st.info("No events available")
        return

    # 🔍 SEARCH
    search = st.text_input("🔍 Search Event")

    filtered = [e for e in events if search.lower() in e["name"].lower()]

    # ================= EVENT LIST =================
    for e in filtered:
        if st.button(f"🎯 {e['name']} - Register", key=f"event_{e['id']}"):
            st.session_state["selected_event"] = e
            st.rerun()

    # ================= FORM =================
    if "selected_event" in st.session_state:

        e = st.session_state.get("selected_event")
        if not e:
            return

        st.divider()
        st.markdown(f"### 📝 Register for {e['name']}")

        mobile = st.text_input("Mobile")
        course = st.selectbox("Course", ["BBA", "BCA"])
        year = st.selectbox("Year", ["1st", "2nd", "3rd"])

        if st.button("Submit Application", use_container_width=True):

            mobile = mobile.strip()

            if not mobile:
                st.warning("Enter mobile number")
                return

            # 🔥 CHECK DUPLICATE
            existing = supabase.table("registrations") \
                .select("*") \
                .eq("email", user["email"]) \
                .eq("event_id", e["id"]) \
                .execute()

            if existing.data:
                st.warning("Already applied for this event")
                return

            # ✅ INSERT DATA
            supabase.table("registrations").insert({
                "user_id": user["id"],
                "event_id": e["id"],
                "name": user["name"],
                "email": user["email"],
                "mobile": mobile,
                "course": course,
                "year": year,
                "status": "pending"
            }).execute()

            st.success("✅ Application submitted")

            del st.session_state["selected_event"]
            st.rerun()

    # ================= TRACK =================
    st.divider()
    st.markdown("### 📊 My Applications")

    data = get_all().data or []

    my = [d for d in data if d.get("email") == user.get("email")]

    if not my:
        st.info("No applications yet")
        return

    for r in my:
        st.write(f"📌 Event: {r.get('event_id')} | Status: {r.get('status')}")
