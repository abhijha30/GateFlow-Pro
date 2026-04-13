import streamlit as st
from utils.db import supabase

def is_college_email(email):
    return email.lower().strip().endswith("@its.edu.in")

def show():
    st.title("📝 Signup")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account", use_container_width=True):

        # ✅ CLEAN INPUTS
        name = name.strip()
        email = email.strip()
        password = password.strip()

        # ✅ VALIDATION FIX
        if not name or not email or not password:
            st.warning("⚠️ Fill all fields properly")
            return

        # ✅ EMAIL VALIDATION
        if not is_college_email(email):
            st.error("❌ Use college email (@its.edu.in only)")
            return

        try:
            # 🔥 SIGNUP
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            # ✅ HANDLE RESPONSE SAFELY
            if res.user:

                supabase.table("users").insert({
                    "id": res.user.id,
                    "name": name,
                    "email": email,
                    "role": role
                }).execute()

                st.success("✅ Account created! Please login")
                st.session_state["page"] = "login"
                st.rerun()

            else:
                st.warning("⚠️ Signup pending. Check your email for verification")

        except Exception as e:

            # 🔥 HANDLE COMMON ERRORS
            error_msg = str(e)

            if "User already registered" in error_msg:
                st.error("❌ Email already registered. Please login")

            elif "Email rate limit exceeded" in error_msg:
                st.error("⚠️ Too many attempts. Try after some time")

            else:
                st.error(f"❌ Signup failed: {error_msg}")
