import streamlit as st
from utils.db import supabase

def show():
    st.title("📝 Signup")

    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Signup"):

        if not email or not password:
            st.warning("Fill all fields")
            return

        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                # store role in DB
                supabase.table("users").insert({
                    "email": email,
                    "role": role
                }).execute()

                st.success("✅ Account created! Please login")
                st.session_state["page"] = "login"
                st.rerun()

        except Exception as e:
            st.error(f"Signup failed: {e}")
