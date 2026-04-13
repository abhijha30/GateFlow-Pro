import streamlit as st
from utils.db import supabase

def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        email = email.strip()
        password = password.strip()

        if not email or not password:
            st.warning("⚠️ Enter email & password")
            return

        try:
            # 🔥 LOGIN AUTH
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:

                # 🔥 GET FULL USER DATA FROM DB
                user_data = supabase.table("users") \
                    .select("*") \
                    .eq("id", res.user.id) \
                    .single() \
                    .execute()

                if not user_data.data:
                    st.error("User not found in database")
                    return

                user = user_data.data

                # ✅ STORE FULL USER OBJECT
                st.session_state["user"] = user
                st.session_state["role"] = user["role"]

                # ✅ ROLE BASED REDIRECT
                if user["role"] == "student":
                    st.session_state["page"] = "student"

                elif user["role"] in ["faculty", "staff"]:
                    st.session_state["page"] = "faculty"

                elif user["role"] == "superadmin":
                    st.session_state["page"] = "superadmin"

                st.success("✅ Login successful")
                st.rerun()

            else:
                st.error("❌ Invalid credentials")

        except Exception as e:
            error_msg = str(e)

            if "Invalid login credentials" in error_msg:
                st.error("❌ Wrong email or password")

            elif "Email not confirmed" in error_msg:
                st.error("⚠️ Please verify your email first")

            else:
                st.error(f"Login failed: {error_msg}")
