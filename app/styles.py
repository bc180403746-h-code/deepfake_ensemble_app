# app/styles.py
import streamlit as st

def apply_theme(dark_mode=False):
    """Apply consistent color palette across the app."""
    if dark_mode:
        colors = {"bg": "#0f172a", "text": "#f8fafc", "accent": "#38bdf8", "header": "#e2e8f0"}
    else:
        colors = {"bg": "#f8fafc", "text": "#1e293b", "accent": "#2563eb", "header": "#0f172a"}

    st.markdown(f"""
        <style>
        body {{ background-color: {colors['bg']}; color: {colors['text']}; }}
        h1, h2, h3, h4, h5 {{ color: {colors['header']}; text-align: center; }}
        .stTabs [role="tablist"] > div {{ justify-content: center; }}
        div[data-testid="stMetricValue"] {{ color: {colors['accent']}; font-weight: bold; }}
        .stButton>button {{
            background: linear-gradient(90deg, {colors['accent']}, #1d4ed8);
            color: white; border-radius: 8px; padding: 0.5em 1em; border: none;
        }}
        </style>
    """, unsafe_allow_html=True)
