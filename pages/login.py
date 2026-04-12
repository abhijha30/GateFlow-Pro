import streamlit as st
from utils.db import supabase
st.write(res)
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
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            # 🔥 IMPORTANT FIX
            if res is None or res.user is None:
                st.error("❌ Invalid credentials")
                return

            # ✅ LOGIN SUCCESS
            user_id = res.user.id

            # 🔍 fetch role
            db_user = supabase.table("users") \
                .select("*") \
                .eq("id", user_id) \
                .execute()

            if not db_user.data:
                st.error("⚠️ User profile missing. Contact admin.")
                return

            user = db_user.data[0]
            role = user["role"]

            # 💾 SESSION
            st.session_state["user"] = user
            st.session_state["role"] = role

            # 🚀 REDIRECT
            if role == "student":
                st.session_state["page"] = "student"
            elif role == "faculty":
                st.session_state["page"] = "faculty"
            elif role == "staff":
                st.session_state["page"] = "faculty"
            elif role == "superadmin":
                st.session_state["page"] = "superadmin"

            st.success("✅ Login successful")
            st.rerun()

        except Exception as e:
            st.error(f"Login error: {e}")
