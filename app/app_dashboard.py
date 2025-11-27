# app/app_dashboard.py — Adaptive Transitions + Dynamic Theme Integration

import sys, os, glob, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from PIL import Image

# --- Import Components ---
from app.components.navbar import render_navbar
from app.components.footer import render_footer
from app.components.status_bar import render_status_bar, set_status
from app.components.enhancement_tab import render_enhancement_tab
from app.components.recognition_tab import render_recognition_tab
from app.components.plate_tab import render_plate_tab
from app.components.deepfake_tab import render_deepfake_tab

# --- Import Theme ---
from app.styles import apply_theme
from app.components.theme_manager import apply_dynamic_theme

# --- Import Models ---
from src.ensemble.ensemble_core import DeepfakeEnsemble
from src.image_utils.recognition import ImageRecognition
from src.image_utils.number_plate_recognition import NumberPlateRecognizer


# --- Initialize Session Keys ---
for key, default in {
    "status": "🧠 Models Loaded and Ready",
    "progress": 0,
    "dark_mode": False,
    "last_update_time": 0,
    "visible": True,
    "history": [],
    "last_page": "enhancement"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Media Intelligence Suite",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="expanded"
)


# =========================================================
# SIDEBAR — THEME + UTILITIES
# =========================================================
st.sidebar.header("🧠 Control Panel")
theme_choice = st.sidebar.radio("🌓 Theme Mode", ["Light", "Dark"], index=0)
st.session_state.dark_mode = (theme_choice == "Dark")
apply_dynamic_theme(st.session_state.dark_mode)

st.sidebar.markdown("---")
st.sidebar.header("📁 Upload Media")
upload = st.sidebar.file_uploader("Select an image or video", type=["jpg", "jpeg", "png", "mp4"])
st.sidebar.info("💡 Upload a file to start analysis")

# st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Utility Actions")

if st.sidebar.button("🗑 Clear Session Cache"):
    st.cache_resource.clear()
    st.cache_data.clear()
    st.sidebar.success("✅ Cache cleared successfully. Refresh the page.")

SAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "samples"))
os.makedirs(SAMPLES_DIR, exist_ok=True)

# result_files = [
#     f for f in os.listdir(SAMPLES_DIR)
#     if f.startswith("enhanced_") or f.startswith("temp_")
# ]
# if result_files:
#     st.sidebar.write("⬇ Download Results:")
#     for file in result_files:
#         file_path = os.path.join(SAMPLES_DIR, file)
#         with open(file_path, "rb") as f:
#             st.sidebar.download_button(
#                 label=file,
#                 data=f,
#                 file_name=file,
#                 mime="application/octet-stream",
#                 key=f"sidebar_dl_{file}"
#             )


# =========================================================
# ADAPTIVE TRANSITION STYLING (based on theme)
# =========================================================
if st.session_state.dark_mode:
    bg_start = "rgba(15, 23, 42, 0.85)"   # deep navy glass
    bg_end = "rgba(30, 41, 59, 0.6)"
    glow = "#60a5fa"
else:
    bg_start = "rgba(255, 255, 255, 0.8)"  # light frosted white
    bg_end = "rgba(241, 245, 249, 0.5)"
    glow = "#2563eb"

st.markdown(f"""
    <style>
    /* --- Smooth theme-adaptive fade + slide transitions --- */
    .block-container {{
        animation: fadeSlideIn 0.7s ease-in-out;
        background: linear-gradient(120deg, {bg_start}, {bg_end});
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }}

    @keyframes fadeSlideIn {{
        from {{
            opacity: 0;
            transform: translateY(15px);
            filter: blur(3px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
            filter: blur(0);
        }}
    }}

    /* Directional animation (left/right) */
    @keyframes slideInLeft {{
        from {{ transform: translateX(40px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    @keyframes slideInRight {{
        from {{ transform: translateX(-40px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    /* Sidebar subtle fade */
    section[data-testid="stSidebar"] {{
        animation: sidebarFadeIn 0.8s ease;
    }}
    @keyframes sidebarFadeIn {{
        from {{ opacity: 0; transform: translateX(-15px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    /* Buttons hover glow */
    .stButton>button {{
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 10px {glow};
    }}
    </style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODELS
# =========================================================
@st.cache_resource
def load_models():
    ensemble = DeepfakeEnsemble(weights=(0.4, 0.6, 0.0))
    recognizer = ImageRecognition()
    plate_reader = NumberPlateRecognizer()
    return ensemble, recognizer, plate_reader

set_status("🧠 Initializing AI models...")
ensemble, recognizer, plate_reader = load_models()
set_status("✅ Models Loaded and Ready")


# =========================================================
# FILE HANDLING
# =========================================================
def cleanup_temp_files():
    for pattern in ["temp_*.jpg", "temp_*.png", "temp_*.mp4"]:
        for f in glob.glob(os.path.join(SAMPLES_DIR, pattern)):
            try:
                os.remove(f)
            except:
                pass

def save_uploaded(upload):
    cleanup_temp_files()
    temp_path = os.path.join(SAMPLES_DIR, f"temp_{upload.name.replace(' ', '_')}")
    with open(temp_path, "wb") as f:
        f.write(upload.read())
    return temp_path


# =========================================================
# HEADER + NAVIGATION
# =========================================================
st.title("🎬 AI Media Intelligence Suite")
st.markdown("##### Deepfake Detection • Image Enhancement • Recognition • Plate Reading")

current_page = render_navbar()
st.markdown("---")

# Determine direction of slide animation
page_order = ["enhancement", "recognition", "plate", "deepfake"]

if current_page not in page_order:
    current_page = "enhancement"

if st.session_state.last_page not in page_order:
    st.session_state.last_page = "enhancement"

if current_page != st.session_state.last_page:
    curr_idx = page_order.index(current_page)
    last_idx = page_order.index(st.session_state.last_page)
    direction = "Left" if curr_idx > last_idx else "Right"
    st.session_state.last_page = current_page
else:
    direction = "Fade"



st.markdown(f"""
    <style>
    .block-container {{
        animation: slideIn{direction} 0.7s ease-in-out;
    }}
    </style>
""", unsafe_allow_html=True)


# =========================================================
# TAB CONTENT
# =========================================================
if upload:
    temp_path = save_uploaded(upload)

    if current_page == "enhancement":
        render_enhancement_tab(upload, SAMPLES_DIR)
    elif current_page == "recognition":
        render_recognition_tab(upload, SAMPLES_DIR, recognizer)
    elif current_page == "plate":
        render_plate_tab(upload, SAMPLES_DIR, plate_reader)
    elif current_page == "deepfake":
        render_deepfake_tab(upload, SAMPLES_DIR, ensemble)
else:
    st.info("👆 Upload an image or video to begin analysis.")


# =========================================================
# FOOTER + FLOATING STATUS BAR
# =========================================================
render_footer(theme_dark=st.session_state.get("dark_mode", False))
render_status_bar(auto_hide_after=5.0)

st.markdown("""
<style>
html, body, [class*="main"] {
    overflow-x: hidden !important;
}
[data-testid="stDecoration"], footer, .reportview-container::after {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


