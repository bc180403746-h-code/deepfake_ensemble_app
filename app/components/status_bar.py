import streamlit as st
import streamlit.components.v1 as components
import time


# ---------- Initialize ----------
def init_status_bar():
    """Ensure session keys exist for status tracking."""
    for key, default in {
        "status": "🧠 Models Loaded and Ready",
        "progress": 0,
        "dark_mode": False,
        "last_update_time": time.time(),
        "visible": True,
        "history": [],
        "ripple_trigger": 0.0,  # tracks last pulse trigger
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ---------- Update ----------
def set_status(message: str, progress: int = 0, context: str = "default"):
    """
    Update status message, progress, and trigger footer pulse with context color.
    context: 'enhancement', 'recognition', 'plate', 'deepfake'
    """
    st.session_state.status = message
    st.session_state.progress = progress
    st.session_state.last_update_time = time.time()
    st.session_state.visible = True
    st.session_state.history.append(f"{time.strftime('%H:%M:%S')} — {message}")

    # Trigger footer pulse + color
    st.session_state.footer_pulse_time = time.time()
    st.session_state.footer_context = context


# ---------- Render ----------
def render_status_bar(auto_hide_after: float = 6.0):
    """Render floating status bar with frosted-glass and ripple pulse (safe, no white div)."""
    init_status_bar()

    now = time.time()
    idle_time = now - st.session_state.last_update_time
    ripple_age = now - st.session_state.ripple_trigger

    st.session_state.visible = idle_time <= auto_hide_after
    show_ripple = ripple_age < 1.0

    msg = st.session_state.status
    progress = st.session_state.progress
    dark = st.session_state.dark_mode
    visible = st.session_state.visible

    # --- Theme Colors ---
    if dark:
        bg = "rgba(30,58,138,0.92)"
        text = "#f8fafc"
        fill = "#38bdf8"
        track = "rgba(255,255,255,0.25)"
        pulse_color = "#60a5fa"
        shadow = "rgba(0,0,0,0.4)"
    else:
        bg = "rgba(219,234,254,0.95)"
        text = "#1e3a8a"
        fill = "#2563eb"
        track = "rgba(0,0,0,0.1)"
        pulse_color = "#2563eb"
        shadow = "rgba(0,0,0,0.15)"

    translate = "0,0" if visible else "150%,0"
    opacity = "1" if visible else "0"

    # --- HTML + CSS ---
    html_code = f"""
    <style>
    .status-bar {{
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
        padding: 12px 18px 14px;
        border-radius: 14px;
        background: {bg};
        color: {text};
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 10px {shadow};
        backdrop-filter: blur(10px);
        width: 280px;
        transform: translate({translate});
        opacity: {opacity};
        transition: transform 0.6s ease, opacity 0.6s ease;
    }}
    .ai-pulse-wrapper {{
        position: relative;
        width: 18px;
        height: 18px;
    }}
    .ai-pulse {{
        position: absolute;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: {pulse_color};
        box-shadow: 0 0 10px {pulse_color};
        animation: pulseGlow 2s ease-in-out infinite;
    }}
    .ripple {{
        position: absolute;
        border-radius: 50%;
        background: {pulse_color};
        opacity: 0.35;
        animation: rippleWave 1.5s ease-out forwards;
    }}
    @keyframes pulseGlow {{
        0% {{ transform: scale(1); box-shadow: 0 0 6px {pulse_color}; }}
        50% {{ transform: scale(1.25); box-shadow: 0 0 18px {pulse_color}; }}
        100% {{ transform: scale(1); box-shadow: 0 0 6px {pulse_color}; }}
    }}
    @keyframes rippleWave {{
        0% {{ transform: scale(0.6); opacity: 0.4; }}
        70% {{ transform: scale(2.4); opacity: 0; }}
        100% {{ opacity: 0; }}
    }}
    .progress-container {{
        height: 6px;
        background: {track};
        border-radius: 4px;
        margin-top: 6px;
        overflow: hidden;
    }}
    .progress-bar {{
        height: 6px;
        width: {progress}%;
        background: {fill};
        transition: width 0.3s ease-in-out;
    }}
    </style>

    <div class="status-bar">
        <div class="ai-pulse-wrapper">
            <div class="ai-pulse"></div>
            {'<div class="ripple"></div>' if show_ripple else ''}
        </div>
        <div>
            <div>{msg}</div>
            <div class="progress-container"><div class="progress-bar"></div></div>
        </div>
    </div>
    """

    # --- Safe render (no white div ghost) ---
    components.html(html_code, height=0, width=0)
