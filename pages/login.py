import streamlit as st
from utils.db import supabase

def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:
                # 🔥 GET ROLE FROM DB
                user_data = supabase.table("users") \
                    .select("*") \
                    .eq("email", email) \
                    .single() \
                    .execute()

                role = user_data.data["role"]

                st.session_state["user"] = email
                st.session_state["role"] = role

                if role == "student":
                    st.session_state["page"] = "student"
                elif role in ["faculty", "staff"]:
                    st.session_state["page"] = "faculty"
                elif role == "superadmin":
                    st.session_state["page"] = "superadmin"

                st.rerun()

            else:
                st.error("Invalid credentials")

        except Exception as e:
            st.error("❌ Invalid login credentials")
