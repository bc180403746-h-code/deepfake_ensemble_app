import streamlit as st
import os
import time
from app.components.status_bar import set_status
from app.components.download_dock import render_download_dock


def render_deepfake_tab(upload, samples_dir, ensemble):
    """Render deepfake detection tab (image or video)."""
    temp_path = os.path.join(samples_dir, f"temp_{upload.name.replace(' ', '_')}")

    try:
        if upload.type.startswith("image/"):
            set_status("🧠 Analyzing image for deepfakes...", progress=20, context="deepfake")
            label, probs = ensemble.predict(image_path=temp_path, video_path=None)
            st.image(temp_path, caption="🧩 Uploaded Image", use_container_width=True)
        else:
            set_status("🎬 Analyzing video for deepfakes...", progress=20)
            label, probs = ensemble.predict(image_path=None, video_path=temp_path)
            st.video(temp_path)

        set_status("✅ Deepfake detection complete!", progress=100)
        st.success(f"**Prediction:** {label} (Real={probs[0]:.4f}, Fake={probs[1]:.4f})")

        render_download_dock(
            file_paths=[(temp_path, "⬇ Download Media File")],
            theme_dark=st.session_state.get("dark_mode", False),
            auto_hide_after=6.0
        )

    except Exception as e:
        st.error(f"❌ Deepfake detection failed: {e}")
        set_status(f"⚠️ Deepfake detection failed ({e})", progress=0)
