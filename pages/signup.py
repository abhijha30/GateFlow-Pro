import streamlit as st
from utils.db import supabase

def show():
    st.title("📝 Signup")

    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Signup"):

        # ✅ CLEAN EMAIL
        email = email.strip().lower()

        # ✅ VALIDATIONS
        if not email or not password:
            st.warning("⚠️ Fill all fields")
            return

        # 🔥 COLLEGE EMAIL CHECK (FIXED)
        if not email.endswith("@its.edu.in"):
            st.error("❌ Use college email id only (@its.edu.in)")
            return

        try:
            # ✅ SIGNUP WITH SUPABASE AUTH
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            # ✅ CHECK USER CREATED
            if res.user:

                # 🔥 STORE ROLE IN DB
                supabase.table("users").insert({
                    "email": email,
                    "role": role
                }).execute()

                st.success("✅ Account created successfully! Please login")

                # 🔁 REDIRECT TO LOGIN
                st.session_state["page"] = "login"
                st.rerun()

            else:
                st.error("❌ Signup failed. Try again.")

        except Exception as e:
            st.error(f"❌ Signup failed: {e}")
