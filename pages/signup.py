import streamlit as st
from utils.db import supabase

def show():
    st.title("📝 Signup")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account"):

        email = email.strip().lower()

        if not name or not email or not password:
            st.warning("Fill all fields")
            return

        # ❌ NO EMAIL RESTRICTION (TEMPORARY FIX)

        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            st.write(res)  # DEBUG

            if not res.user:
                st.error("Signup failed")
                return

            supabase.table("users").upsert({
                "id": res.user.id,
                "name": name,
                "email": email,
                "role": role
            }).execute()

            st.success("✅ Account created")
            st.session_state["page"] = "login"
            st.rerun()

        except Exception as e:
            st.error(e)
