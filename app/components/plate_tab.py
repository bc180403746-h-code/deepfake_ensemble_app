import streamlit as st
import os
import time
from app.components.status_bar import set_status
from app.components.download_dock import render_download_dock


def render_plate_tab(upload, samples_dir, plate_reader):
    """Render number plate recognition tab with feedback and downloads."""
    if not upload or not upload.type.startswith("image/"):
        st.warning("⚠️ Please upload a vehicle image for number plate recognition.")
        return

    temp_path = os.path.join(samples_dir, f"temp_{upload.name.replace(' ', '_')}")

    try:
        set_status("🚗 Detecting license plate...", progress=20, context="plate")
        time.sleep(0.4)
        with st.spinner("🔍 Reading plate text..."):
            plate_text = plate_reader.read_plate_text(temp_path)
        set_status("✅ Plate recognition complete!", progress=100)

        st.image(temp_path, caption="🚙 Vehicle Image", use_container_width=True)
        st.success(f"**Detected Plate:** {plate_text}")

        render_download_dock(
            file_paths=[(temp_path, "⬇ Download Vehicle Image")],
            theme_dark=st.session_state.get("dark_mode", False),
            auto_hide_after=6.0
        )

    except Exception as e:
        st.error(f"❌ Plate recognition failed: {e}")
        set_status(f"⚠️ Plate recognition failed ({e})", progress=0)
