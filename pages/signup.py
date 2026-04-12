import streamlit as st
from utils.db import supabase

def show():
    st.title("📝 Signup")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account"):

        if not name or not email or not password:
            st.warning("Fill all fields")
            return

        if not email.lower().endswith("@its.edu.in"):
            st.error("Use college email (@its.edu.in)")
            return

        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                supabase.table("users").insert({
                    "id": res.user.id,
                    "name": name,
                    "email": email,
                    "role": role
                }).execute()

                st.success("✅ Account created! Now login")
                st.session_state["page"] = "login"
                st.rerun()

            else:
                st.error("Signup failed")

        except Exception as e:
            st.error(str(e))
