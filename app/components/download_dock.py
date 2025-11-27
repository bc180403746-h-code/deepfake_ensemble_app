# app/components/download_dock.py
import streamlit as st
import os
import time


def render_download_dock(file_paths: list, theme_dark: bool = False, auto_hide_after: float = 5.0):
    """
    Floating frosted-glass download dock — unified design with status bar theme.
    Automatically hides after inactivity.
    """

    # --- Adaptive Theme Colors ---
    if theme_dark:
        bg = "rgba(30, 41, 59, 0.7)"      # frosted navy
        border = "1px solid rgba(255,255,255,0.12)"
        shadow = "0 4px 20px rgba(0,0,0,0.45)"
        btn_bg = "linear-gradient(135deg, #60a5fa, #1e3a8a)"
        btn_color = "#f8fafc"
        pulse_color = "#60a5fa"
    else:
        bg = "rgba(255, 255, 255, 0.75)"   # frosted light white
        border = "1px solid rgba(0,0,0,0.08)"
        shadow = "0 4px 18px rgba(0,0,0,0.12)"
        btn_bg = "linear-gradient(135deg, #2563eb, #60a5fa)"
        btn_color = "white"
        pulse_color = "#2563eb"

    # --- CSS Styling and HTML Block (safe, single block) ---
    dock_html = f"""
    <style>
    .download-dock {{
        position: fixed;
        bottom: 110px;
        right: 25px;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 10px;
        background: {bg};
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: {border};
        border-radius: 16px;
        box-shadow: {shadow};
        padding: 14px 16px;
        z-index: 9997;
        transition: all 0.5s ease;
        animation: slideUp 0.6s ease forwards;
        overflow: hidden;
    }}

    @keyframes slideUp {{
        from {{ transform: translateY(30px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    .download-dock.hide {{
        opacity: 0;
        transform: translateY(25px);
    }}

    .download-dock .stDownloadButton>button {{
        background: {btn_bg};
        color: {btn_color};
        border-radius: 12px !important;
        border: none !important;
        width: 220px !important;
        font-weight: 500;
        box-shadow: {shadow};
        transition: all 0.3s ease;
    }}

    .download-dock .stDownloadButton>button:hover {{
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 0 14px {pulse_color};
    }}

    /* Pulse indicator like the status bar */
    .dock-pulse {{
        position: absolute;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: {pulse_color};
        top: -6px;
        right: -6px;
        animation: dockPulse 2s ease-in-out infinite;
        box-shadow: 0 0 8px {pulse_color};
    }}

    @keyframes dockPulse {{
        0% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.4); opacity: 0.6; }}
        100% {{ transform: scale(1); opacity: 0.9; }}
    }}

    html, body {{
        overflow-x: hidden !important;
    }}
    </style>

    <div class="download-dock" id="download-dock">
        <div class="dock-pulse"></div>
    """

    # --- Render download buttons inside dock ---
    st.markdown(dock_html, unsafe_allow_html=True)

    for file_path, label in file_paths:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label=label,
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream",
                    key=f"dl_{os.path.basename(file_path)}",
                )

    # --- Close the dock safely ---
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Auto-hide with JS ---
    st.markdown(f"""
        <script>
        setTimeout(() => {{
            const dock = document.getElementById('download-dock');
            if (dock) {{
                dock.classList.add('hide');
            }}
        }}, {int(auto_hide_after * 1000)});
        </script>
    """, unsafe_allow_html=True)
