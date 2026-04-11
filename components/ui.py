import streamlit as st

# 🌈 GLOBAL STYLE
def apply_style():
    st.markdown("""
    <style>

    /* 🔥 Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    /* 🧊 Glass Card */
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.3s;
    }

    .card:hover {
        transform: scale(1.02);
        border: 1px solid #38bdf8;
    }

    /* 🔘 Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8, #6366f1);
        color: white;
        border-radius: 10px;
        padding: 10px;
        border: none;
        font-weight: bold;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #0ea5e9, #4f46e5);
    }

    /* 📥 Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div {
        border-radius: 10px;
    }

    /* 🧾 Section Title */
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


# 🎯 CARD COMPONENT
def card(title, body):
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <p>{body}</p>
    </div>
    """, unsafe_allow_html=True)


# 📊 METRIC CARD
def metric_card(title, value):
    st.markdown(f"""
    <div class="card">
        <h3>{value}</h3>
        <p>{title}</p>
    </div>
    """, unsafe_allow_html=True)


# ⚡ SECTION HEADER
def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
