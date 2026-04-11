import streamlit as st
from utils.db import supabase

def is_valid_college_email(email):
    # ✅ allow ITS domain
    return email.endswith("@its.edu.in")

def show():
    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Select Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account", use_container_width=True):

        if not name or not email or not password:
            st.warning("⚠️ Fill all fields")
            return

        # ✅ FIXED EMAIL CHECK
        if not is_valid_college_email(email):
            st.error("❌ Use college email (@its.edu.in)")
            return

        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                # ✅ store extra user data
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
                st.error("Signup failed")

        except Exception as e:
            st.error(f"❌ {e}")
