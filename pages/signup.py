import streamlit as st
from utils.db import supabase

def show():
    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Select Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account", use_container_width=True):

        # ✅ VALIDATION
        if not name or not email or not password:
            st.warning("⚠️ Fill all fields")
            return

       def is_valid_college_email(email):
    email = email.strip().lower()
    return "@its.edu.in" in email

if not is_valid_college_email(email):
    st.error("❌ Use college email (@its.edu.in)")
    return

        try:
            # 🔥 SIGNUP
            res = supabase.auth.sign_up({
                "email": email.strip().lower(),
                "password": password
            })

            # 🔍 DEBUG (IMPORTANT)
            if hasattr(res, "error") and res.error:
                st.error(f"❌ {res.error.message}")
                return

            if not res.user:
                st.error("❌ Signup failed (user not created)")
                return

            # ✅ INSERT INTO USERS TABLE
            supabase.table("users").upsert({
                "id": res.user.id,
                "name": name,
                "email": email,
                "role": role
            }).execute()

            st.success("✅ Account created! Please login")
            st.session_state["page"] = "login"
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {e}")
