import streamlit as st

def show_navbar():

    if "user" not in st.session_state:
        return

    role = st.session_state.get("role")

    col1, col2, col3 = st.columns([6,1,1])

    with col1:
        st.markdown(f"### 🎓 GateFlow | {role.upper()}")

    # 🔄 PAGE NAVIGATION
    if role == "student":
        if col2.button("🏠 Home"):
            st.session_state["page"] = "student"

    elif role == "faculty":
        if col2.button("🛠 Dashboard"):
            st.session_state["page"] = "faculty"

    elif role == "superadmin":
        if col2.button("👑 Panel"):
            st.session_state["page"] = "superadmin"

    # 📱 Scanner (common for admin roles)
    if role in ["faculty", "staff", "superadmin"]:
        if col3.button("📱 Scan"):
            st.session_state["page"] = "scanner"

    # 🚪 LOGOUT
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
