import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import requests
import pandas as pd
import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AgroGard 🌱", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

if "history" not in st.session_state:
    st.session_state.history = []

# Premium UI Styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stButton>button {
        background-color: #2b3a42;
        color: #ffffff;
        border: 1px solid #3f51b5;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #3f51b5;
        border-color: #5c6bc0;
        transform: translateY(-2px);
    }
    
    .detect-btn .stButton>button {
        background: linear-gradient(135deg, #43a047, #2e7d32);
        border: None;
        font-size: 18px;
        padding: 10px 0;
        margin-top: 10px;
    }
    .detect-btn .stButton>button:hover {
        background: linear-gradient(135deg, #4caf50, #388e3c);
    }

    img {
        border-radius: 8px;
        max-height: 500px;
        object-fit: contain;
    }
    
    .history-title {
        font-size: 14px;
        text-align: center;
        background: rgba(0,0,0,0.6);
        color: white;
        padding: 4px;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    
    # ================= SIDEBAR MENU =================
    st.sidebar.markdown("<h2 style='text-align: center; color: #4caf50;'>🌿 AgroGard</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    # Using a Dropdown (selectbox) for navigation as requested
    menu_selection = st.sidebar.selectbox("Navigation Menu", ["Home", "History"])

    # ================= HOME PAGE =================
    if menu_selection == "Home":
        st.markdown("<h1 style='text-align: center; color: #2e7d32;'>AI Powered Weed Detection</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # User input handling
        tab_upload, tab_camera = st.tabs(["📁 Upload Image", "📸 Capture via Camera"])
        
        image_bytes = None
        
        with tab_upload:
            uploaded_file = st.file_uploader("Select an image to analyze", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
            if uploaded_file is not None:
                image_bytes = uploaded_file.getvalue()
                
        with tab_camera:
            captured_file = st.camera_input("Take a picture directly", label_visibility="collapsed")
            if captured_file is not None:
                image_bytes = captured_file.getvalue()

        if image_bytes is not None:
            # Place the Detect button centered above the columns so it doesn't push the right side downwards!
            st.markdown('<div class="detect-btn">', unsafe_allow_html=True)
            col_b1, col_btn, col_b3 = st.columns([1, 2, 1])
            with col_btn:
                detect_clicked = st.button("🔍 DETECT WEEDS", use_container_width=True)
            st.markdown('</div><br>', unsafe_allow_html=True)
                
            # Side by Side Layout for Preview vs strict Detection alignment
            col_preview, col_result = st.columns(2, gap="medium")
            
            with col_preview:
                st.markdown("<h3 style='text-align: center;'>Raw Input</h3>", unsafe_allow_html=True)
                st.image(image_bytes, use_container_width=True)
                
            with col_result:
                st.markdown("<h3 style='text-align: center;'>AI Analysis</h3>", unsafe_allow_html=True)
                
                if detect_clicked:
                    with st.spinner("Processing image via YOLOv11 Engine..."):
                        try:
                            files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
                            response = requests.post(f"{API_URL}/predict", files=files)
                            
                            if response.status_code == 200:
                                result = response.json()
                                prediction = result["prediction"]
                                confidence = result["confidence"]
                                image_base64 = result.get("image_b64")
                                
                                # Show Annotated Image completely aligned
                                if image_base64:
                                    import base64
                                    img_data = base64.b64decode(image_base64)
                                    st.image(img_data, use_container_width=True)
                                else:
                                    st.image(image_bytes, caption="Raw Image fallback", use_container_width=True)
                                    
                                m1, m2 = st.columns(2)
                                m1.metric("Top Result", prediction)
                                m2.metric("Confidence", f"{confidence * 100:.2f}%")

                                # Save to local history automatically
                                st.session_state.history.append({
                                    "Date & Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Prediction": prediction,
                                    "Confidence": f"{confidence * 100:.2f}%",
                                    "Image_b64": image_base64
                                })
                            else:
                                st.error(f"Error from backend: {response.text}")
                        except Exception as e:
                            st.error(f"Failed to connect to backend: {str(e)}")
                else:
                    st.info("👈 Press 'DETECT WEEDS' above to analyze this plant.")
        else:
            st.info("Please upload an image or use the camera to begin detection.")

    # ================= HISTORY PAGE =================
    elif menu_selection == "History":
        st.markdown("<h1 style='text-align: center; color: #2e7d32;'>Detection History Gallery</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if len(st.session_state.history) == 0:
            st.info("No detections yet. Go back to Home and scan a plant to start!")
        else:
            h1, h2 = st.columns([8, 2])
            with h2:
                # Setup Download buttons inline
                df = pd.DataFrame([{k:v for k,v in item.items() if k != 'Image_b64'} for item in st.session_state.history])
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download",
                    data=csv,
                    file_name='agrogard_history.csv',
                    mime='text/csv',
                    use_container_width=True
                )
                if st.button("🗑️ Delete", use_container_width=True):
                    st.session_state.history = []
                    st.rerun()

            # 3x3 Image Grid layout
            cols = st.columns(3)
            for idx, item in enumerate(st.session_state.history):
                col = cols[idx % 3]
                with col:
                    if item.get("Image_b64"):
                        import base64
                        img_data = base64.b64decode(item["Image_b64"])
                        st.image(img_data, use_container_width=True)
                    st.markdown(f"<div class='history-title'>{idx+1}.) {item['Prediction']} ({item['Confidence']})</div>", unsafe_allow_html=True)
                    st.write("")

if __name__ == "__main__":
    main()
