# app/components/footer.py
import streamlit as st
import datetime
import platform
import psutil
import GPUtil

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=0.4)
    mem = psutil.virtual_memory().percent
    gpu_info = "GPU: Not detected"
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_info = f"{gpu.name} ({gpu.load * 100:.1f}% load)"
    except Exception:
        pass
    return cpu, mem, gpu_info

def render_footer(theme_dark=False):
    """Frosted footer pinned to bottom — safe layout with glow pulse."""
    cpu, mem, gpu_info = get_system_metrics()
    year = datetime.datetime.now().year
    python_ver = platform.python_version()
    system_name = platform.system()

    if theme_dark:
        bg = "rgba(15,23,42,0.9)"
        text = "#f8fafc"
        accent = "#60a5fa"
    else:
        bg = "rgba(255,255,255,0.9)"
        text = "#1e3a8a"
        accent = "#2563eb"

    footer_html = f"""
    <style>
    .block-container {{
        padding-bottom: 110px !important;
        overflow-x: hidden !important;
    }}
    #frosted-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: {bg};
        color: {text};
        text-align: center;
        padding: 12px 10px;
        font-size: 13px;
        backdrop-filter: blur(14px);
        box-shadow: 0 -2px 18px rgba(0,0,0,0.25);
        border-top: 1px solid rgba(255,255,255,0.08);
        z-index: 9998;
        overflow: hidden;
    }}
    #frosted-footer a {{
        color: {accent};
        text-decoration: none;
    }}
    #frosted-footer a:hover {{
        opacity: 0.85;
    }}
    .metric-box {{
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 5px;
        font-size: 12.5px;
    }}
    html, body {{
        overflow-x: hidden !important;
    }}
    </style>
    <div id="frosted-footer">
        <p>🎬 <b>AI Media Intelligence Suite</b> | v1.1 | Built with ❤️ using 
        <a href="https://streamlit.io" target="_blank">Streamlit</a></p>
        <p>⚙️ {system_name} | Python {python_ver} | © {year}</p>
        <div class="metric-box">
            <span>🧮 CPU {cpu:.1f}%</span>
            <span>💾 Memory {mem:.1f}%</span>
            <span>🎮 {gpu_info}</span>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
