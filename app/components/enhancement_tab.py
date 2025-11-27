import streamlit as st
import os
import time
from src.image_utils.enhancement import enhance_image_cv2
from app.components.status_bar import set_status


def render_enhancement_tab(upload, samples_dir):
    """Render the image enhancement section with frosted-glass cards, glow buttons, and smooth status sync."""

    if not upload or not upload.type.startswith("image/"):
        st.warning("⚠️ Please upload an image for enhancement.")
        return

    # --- File paths ---
    temp_path = os.path.join(samples_dir, f"temp_{upload.name.replace(' ', '_')}")
    output_path = os.path.join(samples_dir, "enhanced_result.jpg")

    try:
        # --- STATUS PROGRESSION ---
        set_status("🧠 Preparing image enhancement model...", progress=10, context="enhancement")

        time.sleep(0.4)
        set_status("⏳ Enhancing image quality...", progress=40)

        with st.spinner("✨ Enhancing image quality..."):
            enhance_image_cv2(temp_path, output_path)
        time.sleep(0.4)

        set_status("✨ Refining details...", progress=80)
        time.sleep(0.4)
        set_status("✅ Enhancement complete!", progress=100)

        # --- DISPLAY ENHANCEMENT RESULTS ---
        st.markdown("### 🖼 Image Enhancement Results")
        col1, col2 = st.columns(2)
        with col1:
            st.image(temp_path, caption="📷 Original Image", use_container_width=True)
        with col2:
            st.image(output_path, caption="✨ Enhanced Image", use_container_width=True)

        # --- THEMED COLORS ---
        dark = st.session_state.get("dark_mode", False)
        if dark:
            glass_bg = "rgba(30, 41, 59, 0.55)"
            border = "1px solid rgba(255,255,255,0.1)"
            text_color = "#f8fafc"
            glow = "0 0 14px rgba(96,165,250,0.3)"
            accent = "#60a5fa"
        else:
            glass_bg = "rgba(255, 255, 255, 0.65)"
            border = "1px solid rgba(0,0,0,0.05)"
            text_color = "#1e3a8a"
            glow = "0 0 12px rgba(37,99,235,0.25)"
            accent = "#2563eb"

        # --- Inject CSS for Frosted Sections ---
        st.markdown(f"""
            <style>
            .frosted-card {{
                background: {glass_bg};
                border: {border};
                border-radius: 16px;
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                box-shadow: {glow};
                padding: 20px 24px;
                margin-top: 20px;
                transition: all 0.4s ease;
            }}
            .frosted-card h3 {{
                color: {text_color};
                font-weight: 600;
                margin-bottom: 12px;
            }}
            .frosted-card .stProgress > div > div {{
                background-color: {accent} !important;
            }}
            .frosted-card .stSuccess > div {{
                background-color: rgba(34,197,94,0.15);
                color: {text_color};
                font-weight: 500;
            }}
            .download-panel {{
                text-align: center;
                background: {glass_bg};
                border: {border};
                border-radius: 16px;
                box-shadow: {glow};
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                padding: 18px 24px;
                margin-top: 25px;
                transition: all 0.4s ease;
            }}
            .download-panel h3 {{
                color: {text_color};
                margin-bottom: 12px;
                font-weight: 600;
            }}
            .download-panel .stDownloadButton>button {{
                border-radius: 10px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 0 8px rgba(0,0,0,0.15);
            }}
            .download-panel .stDownloadButton>button:hover {{
                transform: translateY(-2px) scale(1.03);
                box-shadow: {glow};
            }}
            </style>
        """, unsafe_allow_html=True)

        # --- QUALITY ENHANCEMENT SUMMARY (in frosted container) ---
        st.markdown('<div class="frosted-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Quality Enhancement Summary", unsafe_allow_html=True)
        st.progress(100)
        st.success("✅ Enhancement complete and saved!")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- DOWNLOAD OUTPUTS (Frosted Panel) ---
        st.markdown('<div class="download-panel">', unsafe_allow_html=True)
        st.markdown("### 💾 Download Outputs", unsafe_allow_html=True)
        cols = st.columns(2)
        files = [
            (output_path, "⬇ Download Enhanced Image"),
            (temp_path, "⬇ Download Original Image")
        ]
        for i, (path, label) in enumerate(files):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    cols[i].download_button(
                        label=label,
                        data=f,
                        file_name=os.path.basename(path),
                        mime="application/octet-stream",
                        use_container_width=True,
                    )
        st.markdown("</div>", unsafe_allow_html=True)

        # Delay before idle fade
        time.sleep(1)
        set_status("🧠 Models Loaded and Ready", progress=0)

    except Exception as e:
        st.error(f"❌ Enhancement failed: {e}")
        set_status(f"⚠️ Error: Enhancement failed ({e})", progress=0)
