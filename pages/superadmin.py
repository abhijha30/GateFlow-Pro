import streamlit as st
from utils.db import *

def show():

    if "user" not in st.session_state:
        st.warning("Login first")
        return

    st.markdown("## 👑 Super Admin Panel")

    data = get_all().data or []

    st.write("Total:", len(data))

    approved = len([d for d in data if d["status"]=="approved"])
    rejected = len([d for d in data if d["status"]=="rejected"])

    st.write("Approved:", approved)
    st.write("Rejected:", rejected)
