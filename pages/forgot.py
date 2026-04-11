import streamlit as st
from utils.db import supabase

def show():

    st.markdown("## 🔑 Forgot Password")

    email = st.text_input("Enter Email")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Reset Password"):

        supabase.table("users") \
            .update({"password": new_pass}) \
            .eq("email", email) \
            .execute()

        st.success("✅ Password Updated")
