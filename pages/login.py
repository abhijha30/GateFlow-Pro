import streamlit as st
from utils.db import supabase

def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        email = email.strip().lower()

        if not email or not password:
            st.warning("Enter email and password")
            return

        try:
            auth_res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_res or not auth_res.user:
                st.error("Invalid login credentials")
                return

            user_id = auth_res.user.id

            user_data = supabase.table("users") \
                .select("*") \
                .eq("id", user_id) \
                .execute()

            if not user_data.data:
                st.error("Login succeeded, but profile not found in users table")
                return

            user = user_data.data[0]
            role = user.get("role", "student")

            st.session_state["user"] = {
                "id": user_id,
                "email": email,
                "name": user.get("name", "")
            }
            st.session_state["role"] = role

            if role == "student":
                st.session_state["page"] = "student"
            elif role == "faculty":
                st.session_state["page"] = "faculty"
            elif role == "staff":
                st.session_state["page"] = "faculty"
            elif role == "superadmin":
                st.session_state["page"] = "superadmin"
            else:
                st.session_state["page"] = "student"

            st.rerun()

        except Exception as e:
            st.error(f"Login failed: {e}")
