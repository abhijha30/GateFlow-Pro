import streamlit as st
st.markdown("""
<style>
/* Fix text visibility */
html, body, [class*="css"]  {
    color: #ffffff;
}

/* Input fields */
input, textarea {
    color: black !important;
}

/* Labels */
label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Fix selectbox text */
div[data-baseweb="select"] {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="GateFlow",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.image("assets/logo.png", width=120)
# ================== IMPORTS ==================
from pages import login, signup, forgot, student, faculty, superadmin, scanner
from components.ui import apply_style
from components.navbar import show_navbar

# ================== APPLY UI ==================
apply_style()

# ================== SESSION INIT ==================
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

# ================== AUTO REDIRECT AFTER LOGIN ==================
if st.session_state["user"]:

    role = st.session_state["role"]

    if role == "student":
        st.session_state["page"] = "student"

    elif role == "faculty":
        st.session_state["page"] = "faculty"

    elif role == "staff":
        st.session_state["page"] = "faculty"

    elif role == "superadmin":
        st.session_state["page"] = "superadmin"

# ================== NAVBAR ==================
if st.session_state["user"]:
    show_navbar()

# ================== PAGE ROUTING ==================
page = st.session_state["page"]

if page == "login":
    login.show()

elif page == "signup":
    signup.show()

elif page == "forgot":
    forgot.show()

elif page == "student":
    student.show()

elif page == "faculty":
    faculty.show()

elif page == "superadmin":
    superadmin.show()

elif page == "scanner":
    scanner.show()

else:
    st.session_state["page"] = "login"
    st.rerun()

# ================== AUTH NAVIGATION ==================
if not st.session_state["user"]:

    st.divider()
    st.markdown("### 🔐 Quick Access")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    with col2:
        if st.button("📝 Signup", use_container_width=True):
            st.session_state["page"] = "signup"
            st.rerun()

    with col3:
        if st.button("🔑 Forgot Password", use_container_width=True):
            st.session_state["page"] = "forgot"
            st.rerun()

# ================== FOOTER ==================
st.markdown("""
<hr>
<center style="color: gray;">
🚀 GateFlow  
Smart Event & Entry Management System
</center>
""", unsafe_allow_html=True)
