import streamlit as st
import os
import time
from src.image_utils.recognition import ImageRecognition
from app.components.status_bar import set_status
from app.components.download_dock import render_download_dock


def render_recognition_tab(upload, samples_dir, recognizer: ImageRecognition):
    """Render the Image Recognition tab with consistent theme, status bar, and download dock."""
    if not upload or not upload.type.startswith("image/"):
        st.warning("⚠️ Please upload a valid image for recognition.")
        return

    # --- File handling ---
    temp_path = os.path.join(samples_dir, f"temp_{upload.name.replace(' ', '_')}")

    try:
        # --- Smart status updates ---
        set_status("🧠 Initializing recognition model...", progress=15, context="recognition")
        time.sleep(0.4)

        set_status("🔍 Analyzing uploaded image...", progress=50)
        with st.spinner("🧠 Identifying image content..."):
            label, prob = recognizer.predict(temp_path)
        time.sleep(0.3)

        set_status("✅ Image recognition complete!", progress=100)

        # --- Display results ---
        st.markdown("### 🖼 Image Recognition Results")
        col1, col2 = st.columns([3, 2])

        with col1:
            st.image(temp_path, caption="📸 Uploaded Image", use_container_width=True)

        with col2:
            st.metric("Predicted Label", label)
            st.metric("Confidence", f"{prob:.2%}")
            st.success("✅ Recognition complete!")

        # --- Floating Download Dock (aligned bottom-right) ---
        render_download_dock(
            file_paths=[(temp_path, "⬇ Download Analyzed Image")],
            theme_dark=st.session_state.get("dark_mode", False),
            auto_hide_after=6.0
        )

        # Keep status bar visible briefly before fading
        time.sleep(1)
        set_status("🧠 Models Loaded and Ready", progress=0)

    except Exception as e:
        st.error(f"❌ Recognition failed: {e}")
        set_status(f"⚠️ Recognition failed: {e}", progress=0)
