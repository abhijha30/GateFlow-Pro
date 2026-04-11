import streamlit as st

st.set_page_config(page_title="GateFlow Pro", layout="wide")

from pages import login, signup, forgot, student, faculty, superadmin, scanner

page = st.session_state.get("page", "login")

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
