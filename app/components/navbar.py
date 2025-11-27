import streamlit as st
import time

def render_navbar():
    """Render adaptive frosted navbar with shimmer and active glow highlight."""
    dark = st.session_state.get("dark_mode", False)

    # --- THEME COLORS ---
    if dark:
        bg_gradient = "linear-gradient(120deg, rgba(30,41,59,0.65), rgba(17,24,39,0.75), rgba(30,41,59,0.65))"
        border = "1px solid rgba(255,255,255,0.08)"
        text_color = "#f8fafc"
        hover = "rgba(255,255,255,0.08)"
        glow_gradient = "linear-gradient(90deg, #60a5fa, #38bdf8, #a78bfa, #60a5fa)"
    else:
        bg_gradient = "linear-gradient(120deg, rgba(255,255,255,0.65), rgba(241,245,249,0.85), rgba(255,255,255,0.65))"
        border = "1px solid rgba(0,0,0,0.05)"
        text_color = "#1e3a8a"
        hover = "rgba(0,0,0,0.05)"
        glow_gradient = "linear-gradient(90deg, #2563eb, #3b82f6, #8b5cf6, #2563eb)"

    # --- Persistent page in session state ---
    if "current_page" not in st.session_state:
        st.session_state.current_page = "enhancement"

    # --- Animation Speed Logic ---
    if "nav_anim_speed" not in st.session_state:
        st.session_state.nav_anim_speed = "normal"
    if "nav_anim_time" not in st.session_state:
        st.session_state.nav_anim_time = time.time()

    # Speed up for 2 seconds after page switch
    if time.time() - st.session_state.nav_anim_time < 2 and st.session_state.nav_anim_speed == "fast":
        speed = "4s"
    else:
        st.session_state.nav_anim_speed = "normal"
        speed = "10s"

    # --- CSS ---
    st.markdown(f"""
        <style>
        .navbar {{
            display: flex;
            justify-content: center;
            gap: 30px;
            background: {bg_gradient};
            border: {border};
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 10px 18px;
            margin-bottom: 25px;
            box-shadow: 0 0 20px rgba(0,0,0,0.15);
            background-size: 200% 200%;
            animation: shimmerFlow {speed} ease-in-out infinite, navbarFadeSlide 0.8s ease;
        }}

        @keyframes shimmerFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes navbarFadeSlide {{
            from {{ opacity: 0; transform: translateY(-12px); filter: blur(3px); }}
            to {{ opacity: 1; transform: translateY(0); filter: blur(0); }}
        }}

        .navbar button {{
            background: transparent;
            border: none;
            color: {text_color};
            font-weight: 500;
            font-size: 15px;
            cursor: pointer;
            padding: 8px 16px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        .navbar button:hover {{
            background: {hover};
            transform: translateY(-1px);
        }}
        .navbar button.active {{
            font-weight: 600;
            color: #60a5fa;
            position: relative;
        }}

        .navbar button.active::after {{
            content: '';
            position: absolute;
            left: 10%;
            bottom: 0;
            width: 80%;
            height: 3px;
            border-radius: 4px;
            background: {glow_gradient};
            background-size: 300% 100%;
            animation: gradientFlow 5s linear infinite, glowPulse 1.6s ease-in-out infinite alternate;
        }}

        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes glowPulse {{
            0% {{ box-shadow: 0 0 5px rgba(96,165,250,0.6); }}
            50% {{ box-shadow: 0 0 18px rgba(168,85,247,0.8); }}
            100% {{ box-shadow: 0 0 5px rgba(96,165,250,0.6); }}
        }}
        </style>
    """, unsafe_allow_html=True)

    # --- NAV BUTTONS ---
    pages = {
        "enhancement": "🪄 Enhancement",
        "recognition": "🧠 Recognition",
        "plate": "🚗 Plate Reader",
        "deepfake": "🎭 Deepfake"
    }

    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    cols = st.columns(len(pages))
    for i, (key, label) in enumerate(pages.items()):
        with cols[i]:
            is_active = st.session_state.current_page == key
            if st.button(label, key=f"nav_{key}"):
                st.session_state.current_page = key
                st.session_state.nav_anim_speed = "fast"
                st.session_state.nav_anim_time = time.time()
            st.markdown(
                f"<style>div[data-testid='stButton'][key='nav_{key}'] button{{ {'color:#60a5fa;font-weight:600;' if is_active else ''} }}</style>",
                unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

    return st.session_state.current_page
