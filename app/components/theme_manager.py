import streamlit as st

def apply_dynamic_theme(dark_mode: bool):
    """
    Apply a frosted-glass adaptive theme that updates dynamically when toggled.
    """
    if dark_mode:
        # --- Dark Mode ---
        bg_grad = "linear-gradient(120deg, rgba(15,23,42,0.9), rgba(30,41,59,0.9))"
        card_bg = "rgba(30, 41, 59, 0.55)"
        text_color = "rgba(248, 250, 252, 0.9)"
        accent = "#60a5fa"
        shadow = "0 4px 20px rgba(0, 0, 0, 0.35)"
        dock_bg = "rgba(30, 41, 59, 0.45)"
    else:
        # --- Light Mode ---
        bg_grad = "linear-gradient(120deg, rgba(241,245,249,0.85), rgba(255,255,255,0.8))"
        card_bg = "rgba(255, 255, 255, 0.55)"
        text_color = "rgba(30, 41, 59, 0.9)"
        accent = "#2563eb"
        shadow = "0 4px 20px rgba(0, 0, 0, 0.08)"
        dock_bg = "rgba(255, 255, 255, 0.4)"

    st.markdown(f"""
        <style>
        html, body, [class*="stApp"] {{
            background: {bg_grad} fixed;
            color: {text_color};
            font-family: 'Inter', 'Segoe UI', sans-serif;
            transition: all 0.4s ease-in-out;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: {card_bg};
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255,255,255,0.1);
        }}

        /* Main cards and containers */
        .block-container {{
            background: {card_bg};
            backdrop-filter: blur(20px);
            border-radius: 16px;
            box-shadow: {shadow};
            padding: 2rem;
        }}

        /* Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, {accent}, #1e3a8a);
            color: white !important;
            border: none;
            border-radius: 10px;
            box-shadow: {shadow};
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            opacity: 0.92;
            transform: scale(1.03);
        }}

        /* Download buttons (floating dock harmony) */
        .stDownloadButton>button {{
            background: {accent};
            color: white;
            border-radius: 10px;
            box-shadow: {shadow};
            padding: 0.5rem 1rem;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
            font-weight: 600;
        }}

        /* Download Dock styling hook */
        .download-dock {{
            background: {dock_bg} !important;
        }}

        /* Smooth transition for everything */
        * {{
            transition: background 0.4s ease, color 0.4s ease, box-shadow 0.3s ease;
        }}
        </style>
    """, unsafe_allow_html=True)
