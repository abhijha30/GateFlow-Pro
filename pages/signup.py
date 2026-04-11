import streamlit as st
from utils.db import supabase

def show():

    st.markdown("## 📝 Signup")

    name = st.text_input("Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Select Role", [
        "student", "faculty", "staff", "superadmin"
    ])

    if st.button("Create Account", use_container_width=True):

        if "@college" not in email:
            st.warning("Use college email")
            return

        supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }).execute()

        st.success("✅ Account created")
        st.rerun()
