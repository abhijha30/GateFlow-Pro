import streamlit as st
from utils.db import supabase

def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:
                user_data = supabase.table("users") \
                    .select("*") \
                    .eq("id", res.user.id) \
                    .execute()

                role = user_data.data[0]["role"]

                st.session_state["user"] = res.user
                st.session_state["role"] = role

                # 🔥 redirect
                if role == "student":
                    st.session_state["page"] = "student"
                elif role == "faculty":
                    st.session_state["page"] = "faculty"
                elif role == "superadmin":
                    st.session_state["page"] = "superadmin"
                elif role == "staff":
                    st.session_state["page"] = "faculty"

                st.rerun()

        except Exception as e:
            st.error("Invalid credentials")
