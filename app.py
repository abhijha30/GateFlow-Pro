import streamlit as st

# ================== PAGE CONFIG (MUST BE FIRST) ==================
st.set_page_config(
    page_title="GateFlow",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== GLOBAL CSS ==================
st.markdown("""
<style>
button {
    height: 50px !important;
    font-size: 18px !important;
}

.stTextInput input {
    font-size: 18px !important;
}

.stSelectbox div {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Background */
body {
    background-color: #0e1117;
}

/* Fix text visibility */
html, body, [class*="css"]  {
    color: #ffffff;
}

/* Inputs */
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

/* Selectbox fix */
div[data-baseweb="select"] {
    color: black !important;
}

/* Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ================== IMPORTS ==================
from pages import login, signup, forgot, student, faculty, superadmin, scanner
from components.ui import apply_style
from components.navbar import show_navbar

# ================== APPLY UI ==================
apply_style()

# ================== LOGO ==================
st.image("assets/logo.png", width=120)

# ================== SESSION INIT ==================
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

# ================== AUTO REDIRECT ==================
if st.session_state["user"]:

    role = st.session_state["role"]

    if role == "student":
        st.session_state["page"] = "student"

    elif role in ["faculty", "staff"]:
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

# ================== AUTH NAV ==================
if not st.session_state["user"]:

    st.divider()
    st.markdown("### 🔐 Quick Access")

    col1, col2, col3 = st.columns(3)

    if col1.button("🔐 Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()

    if col2.button("📝 Signup", use_container_width=True):
        st.session_state["page"] = "signup"
        st.rerun()

    if col3.button("🔑 Forgot Password", use_container_width=True):
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
