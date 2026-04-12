import streamlit as st
from utils.db import supabase

# ✅ VERY RELAXED EMAIL VALIDATION (NO BUG)
def is_valid_college_email(email):
    email = email.strip().lower()

    # allow ANY email containing its.edu.in
    if "its.edu.in" in email:
        return True
    return False


def show():
    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("College Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Select Role", ["student", "faculty", "staff", "superadmin"])

    if st.button("Create Account", use_container_width=True):

        # ✅ BASIC VALIDATION
        if not name or not email or not password:
            st.warning("⚠️ Fill all fields")
            return

        # 🔥 DEBUG (REMOVE LATER)
        clean_email = email.strip().lower()
        st.write("DEBUG EMAIL:", clean_email)

        # ✅ FIXED EMAIL CHECK (NO MORE ERROR)
        if not is_valid_college_email(clean_email):
            st.error("❌ Please use your college email (its.edu.in)")
            return

        try:
            # 🔥 SIGNUP
            res = supabase.auth.sign_up({
                "email": clean_email,
                "password": password
            })

            # 🔍 HANDLE ERRORS PROPERLY
            if hasattr(res, "error") and res.error:
                st.error(f"❌ {res.error.message}")
                return

            if not res.user:
                st.error("❌ Signup failed (user not created)")
                return

            # ✅ STORE USER DATA
            supabase.table("users").upsert({
                "id": res.user.id,
                "name": name,
                "email": clean_email,
                "role": role
            }).execute()

            st.success("✅ Account created! Please login")
            st.session_state["page"] = "login"
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {e}")
