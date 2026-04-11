import streamlit as st
from utils.db import supabase

def login_user(email, password):
    res = supabase.table("users").select("*") \
        .eq("email", email).eq("password", password).execute()

    if res.data:
        user = res.data[0]
        st.session_state["user"] = user
        st.session_state["role"] = user["role"]
        st.session_state["page"] = user["role"]
    else:
        st.error("Invalid credentials")

def signup_user(data):
    return supabase.table("users").insert(data).execute()

def logout():
    st.session_state.clear()
    st.session_state["page"] = "login"
