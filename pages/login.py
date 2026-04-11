import streamlit as st
from utils.db import supabase

def show():

    st.markdown("## 🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        res = supabase.table("users") \
            .select("*") \
            .eq("email", email) \
            .eq("password", password) \
            .execute()

        if res.data:
            user = res.data[0]

            st.session_state["user"] = user
            st.session_state["role"] = user["role"]

            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.info("Don't have account? Go to Signup")
