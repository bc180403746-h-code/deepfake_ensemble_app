# app/app.py — Modular, Theme-Ready Dashboard

import sys, os, time, glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from PIL import Image

# --- Import your project modules ---
from src.ensemble.ensemble_core import DeepfakeEnsemble
from src.image_utils.enhancement import enhance_image_cv2
from src.image_utils.recognition import ImageRecognition
from src.image_utils.number_plate_recognition import NumberPlateRecognizer


# ====================== APP SETUP ======================
st.set_page_config(
    page_title="AI Media Intelligence Suite",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="expanded",
)

# --- Custom CSS (Light/Dark Theme Aware) ---
st.markdown("""
    <style>
        .main { background-color: var(--background-color); }
        h1, h2, h3 { text-align:center; color: var(--text-color); }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b, #0f172a);
            color: white;
        }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
        }
        .stTabs [role="tablist"] > div { justify-content: center; }
        .metric-label { font-weight: 600; color: #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("""
    <div style='text-align:center'>
        <h1>🎬 AI Media Intelligence Dashboard</h1>
        <h4 style='color:gray'>Deepfake Detection • Image Enhancement • Recognition • Plate Reading</h4>
        <hr style='margin-top:10px;margin-bottom:20px'>
    </div>
""", unsafe_allow_html=True)


# ====================== MODEL LOADING ======================
@st.cache_resource
def load_models():
    with st.spinner("Loading AI models (first run may take a minute)..."):
        ensemble = DeepfakeEnsemble(weights=(0.4, 0.6, 0.0))
        recognizer = ImageRecognition()
        plate_reader = NumberPlateRecognizer()
    return ensemble, recognizer, plate_reader


ensemble, recognizer, plate_reader = load_models()


# ====================== HELPER FUNCTIONS ======================
BASE_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "samples"))
os.makedirs(SAMPLES_DIR, exist_ok=True)


def cleanup_old_temp_files():
    for pattern in ["temp_*.jpg", "temp_*.png", "temp_*.mp4"]:
        for f in glob.glob(os.path.join(SAMPLES_DIR, pattern)):
            try:
                os.remove(f)
            except:
                pass


def save_uploaded_file(upload):
    cleanup_old_temp_files()
    safe_name = upload.name.replace(" ", "_")
    temp_path = os.path.join(SAMPLES_DIR, f"temp_{safe_name}")
    with open(temp_path, "wb") as f:
        f.write(upload.read())
    return temp_path


# ====================== SIDEBAR OPTIONS ======================
st.sidebar.title("⚙️ Control Panel")
theme_choice = st.sidebar.radio("Theme Mode", ["Light", "Dark"], index=0)

# Apply dynamic colors
if theme_choice == "Dark":
    st.markdown("<style>:root { --background-color:#0f172a; --text-color:#f8fafc; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>:root { --background-color:#f8fafc; --text-color:#1e293b; }</style>", unsafe_allow_html=True)

st.sidebar.write("---")
upload = st.sidebar.file_uploader("📂 Upload Image or Video", type=["jpg", "jpeg", "png", "mp4"])


# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "🪄 Image Enhancement",
    "🧠 Image Recognition",
    "🚗 Number Plate Recognition",
    "🎭 Deepfake Detection"
])

if upload is None:
    st.info("👆 Upload an image or video from the sidebar to begin.")
    st.stop()


# ====================== PROCESS ======================
temp_path = save_uploaded_file(upload)

# ---------------- TAB 1: ENHANCEMENT ----------------
with tab1:
    if upload.type.startswith("image/"):
        with st.spinner("Enhancing image quality..."):
            output_path = os.path.join(SAMPLES_DIR, "enhanced_preview.jpg")
            enhance_image_cv2(temp_path, output_path)
        col1, col2 = st.columns(2)
        with col1:
            st.image(temp_path, caption="Original", use_container_width=True)
        with col2:
            st.image(output_path, caption="Enhanced", use_container_width=True)
        st.success("✅ Enhancement Complete!")
    else:
        st.warning("⚠️ Please upload an image file for enhancement.")


# ---------------- TAB 2: IMAGE RECOGNITION ----------------
with tab2:
    if upload.type.startswith("image/"):
        with st.spinner("Analyzing image contents..."):
            label, prob = recognizer.predict(temp_path)
        st.image(temp_path, caption="Uploaded Image", use_container_width=True)
        st.metric("Predicted Label", label)
        st.metric("Confidence", f"{prob:.2%}")
        st.success("✅ Recognition Complete!")
    else:
        st.warning("⚠️ Please upload an image for recognition.")


# ---------------- TAB 3: PLATE DETECTION ----------------
with tab3:
    if upload.type.startswith("image/"):
        with st.spinner("Detecting and reading number plate..."):
            plate_text = plate_reader.read_plate_text(temp_path)
        st.image(temp_path, caption="Car Image", use_container_width=True)
        if plate_text not in ["No plate detected", "Text not detected"]:
            st.success(f"✅ Detected Plate: **{plate_text}**")
        else:
            st.warning("⚠️ No clear plate text found.")
    else:
        st.warning("⚠️ Please upload a car image.")


# ---------------- TAB 4: DEEPFAKE DETECTION ----------------
with tab4:
    with st.spinner("Running deepfake detection..."):
        if upload.type.startswith("image/"):
            label, probs = ensemble.predict(image_path=temp_path, video_path=None)
            st.image(temp_path, caption="Uploaded Image", use_container_width=True)
        else:
            label, probs = ensemble.predict(image_path=None, video_path=temp_path)
            st.video(temp_path)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Prediction", label)
    with col2:
        st.metric("Fake Probability", f"{probs[1]:.4f}")
    st.success("✅ Deepfake Analysis Complete!")
