import streamlit as st
from utils.db import supabase

def is_college_email(email):
    return email.lower().endswith("@its.edu.in")

def show():
    st.title("📝 Signup")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account", use_container_width=True):

        if not name or not email or not password:
            st.warning("Fill all fields")
            return

        if not is_college_email(email):
            st.error("❌ Use college email (@its.edu.in only)")
            return

        try:
            # 🔥 SIGNUP IN AUTH
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                # ✅ STORE IN DB (NO PASSWORD FIELD!)
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
                st.error("Signup failed. Try again")

        except Exception as e:
            st.error(f"Error: {e}")
