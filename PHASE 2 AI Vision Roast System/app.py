import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import json

# Load environment variables for local development
load_dotenv()

# Get API key from Streamlit Secrets (cloud) or environment variables (local)
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found. Please add it to Streamlit Secrets.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Configuration error: {e}")
    st.stop()

# Set up the Streamlit page layout
st.set_page_config(page_title="AI Vision Roast System", page_icon="🔥", layout="wide")

# Antigravity CSS Theme
antigravity_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Dark space background */
    body {
        background: linear-gradient(135deg, #03030A 0%, #0a0a15 50%, #030310 100%) !important;
        color: #e0e0e0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #03030A 0%, #0a0a15 50%, #030310 100%) !important;
    }
    
    /* Remove default streamlit styling */
    .stMainBlockContainer {
        background: transparent !important;
        padding: 2rem;
    }
    
    /* Floating container */
    .floating-container {
        background: rgba(123, 47, 255, 0.08) !important;
        backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(123, 47, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(123, 47, 255, 0.1), 
                    0 0 60px rgba(0, 245, 255, 0.05) !important;
        animation: levitate 3s ease-in-out infinite !important;
        position: relative !important;
        margin-bottom: 1.5rem !important;
    }
    
    .floating-container:nth-child(even) {
        animation-delay: 1.5s !important;
    }
    
    /* Neon glow effect */
    .neon-glow {
        text-shadow: 0 0 10px rgba(123, 47, 255, 0.8),
                     0 0 20px rgba(0, 245, 255, 0.5),
                     0 0 30px rgba(123, 47, 255, 0.3) !important;
        color: #00f5ff !important;
        letter-spacing: 3px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Intensity buttons */
    .intensity-btn {
        background: rgba(255, 69, 0, 0.15) !important;
        border: 2px solid rgba(255, 69, 0, 0.3) !important;
        color: #FFD700 !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.1) !important;
    }
    
    .intensity-btn:hover {
        background: rgba(255, 69, 0, 0.3) !important;
        box-shadow: 0 0 40px rgba(255, 69, 0, 0.4), 
                    0 0 80px rgba(255, 165, 0, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    .intensity-btn.active {
        background: linear-gradient(135deg, #FF4500, #FFD700) !important;
        color: #000 !important;
        box-shadow: 0 0 50px rgba(255, 69, 0, 0.6), 
                    0 0 100px rgba(255, 212, 0, 0.3) !important;
        transform: translateY(-4px) !important;
    }
    
    /* Roast button */
    .roast-btn {
        background: linear-gradient(135deg, #FF4500 0%, #FF8C00 50%, #FFD700 100%) !important;
        color: #000 !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px !important;
        cursor: pointer !important;
        box-shadow: 0 0 30px rgba(255, 69, 0, 0.5) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
    }
    
    .roast-btn:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 0 50px rgba(255, 69, 0, 0.8), 
                    0 0 100px rgba(255, 212, 0, 0.4) !important;
    }
    
    .roast-btn:active {
        transform: translateY(-1px) !important;
    }
    
    /* Result card */
    .result-card {
        background: rgba(255, 69, 0, 0.05) !important;
        backdrop-filter: blur(24px) !important;
        border: 2px solid rgba(255, 69, 0, 0.3) !important;
        border-left: 4px solid #FF4500 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(255, 69, 0, 0.15),
                    0 0 60px rgba(255, 69, 0, 0.1) !important;
        animation: slideUpSpring 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Score bars */
    .score-bar {
        margin: 0.8rem 0 1.2rem 0 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        height: 6px !important;
        overflow: hidden !important;
        border: 1px solid rgba(123, 47, 255, 0.2) !important;
    }
    
    .score-fill {
        background: linear-gradient(90deg, #7B2FFF, #00F5FF) !important;
        height: 100% !important;
        animation: fillBar 0.8s ease-out !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.6) !important;
    }
    
    .score-label {
        display: flex !important;
        justify-content: space-between !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.3rem !important;
        color: #00F5FF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }
    
    /* Upload zone */
    .upload-zone {
        border: 2px dashed rgba(0, 245, 255, 0.4) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        text-align: center !important;
        background: rgba(0, 245, 255, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .upload-zone:hover {
        border-color: rgba(0, 245, 255, 0.8) !important;
        background: rgba(0, 245, 255, 0.1) !important;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.3) !important;
    }
    
    /* Title styling */
    .title-main {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        animation: levitate 4s ease-in-out infinite !important;
    }
    
    .subtitle {
        text-align: center !important;
        color: #00F5FF !important;
        font-size: 1.1rem !important;
        letter-spacing: 2px !important;
        margin-bottom: 2rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 300 !important;
    }
    
    /* Animations */
    @keyframes levitate {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    @keyframes slideUpSpring {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        70% { transform: translateY(-2px) scale(1.01); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    @keyframes fillBar {
        0% { width: 0%; }
        100% { width: var(--fill-percent); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block !important;
        background: rgba(0, 255, 100, 0.15) !important;
        border: 1px solid rgba(0, 255, 100, 0.4) !important;
        color: #00FF64 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 50px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        animation: pulse 2s ease-in-out infinite !important;
    }
    
    /* Text effects */
    .roast-text {
        font-family: 'Space Grotesk', sans-serif !important;
        line-height: 1.6 !important;
        color: #FFD700 !important;
        font-size: 0.95rem !important;
        white-space: pre-wrap !important;
        margin: 1rem 0 !important;
    }
</style>
"""

# Inject CSS
st.markdown(antigravity_css, unsafe_allow_html=True)

# Header Section
col_header = st.columns([1, 1, 1])
with col_header[1]:
    st.markdown('<div class="title-main">🔥 ROAST.AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">VISION INTELLIGENCE SYSTEM v2.0</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><span class="status-badge">● SYSTEM ONLINE</span></div>', unsafe_allow_html=True)

st.markdown("---")

# Main content
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="floating-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#00F5FF; text-align:center;">📸 UPLOAD IMAGE</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png", "webp", "gif"], label_visibility="collapsed")
    
    st.markdown('<h3 style="color:#7B2FFF; margin-top:2rem;">🔥 ROAST INTENSITY</h3>', unsafe_allow_html=True)
    intensity = st.radio("Select roast level", ["🌶️ MILD", "🔥 HOT", "☠️ INFERNO"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if uploaded_file is not None:
        st.markdown('<div class="floating-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#00F5FF; text-align:center;">⚡ PREVIEW</h2>', unsafe_allow_html=True)
        
        image = Image.open(uploaded_file)
        # Resize image to max width 300px
        max_width = 300
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image_resized = image.resize((max_width, new_height))
        
        st.image(image_resized, use_container_width=False)
        st.markdown("</div>", unsafe_allow_html=True)

# Action button
st.markdown("<br>", unsafe_allow_html=True)
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    roast_button = st.button("🔥 IGNITE THE ROAST", use_container_width=True, key="roast_btn")

# Process roast
if roast_button:
    if uploaded_file is None:
        st.error("❌ Please upload an image first!")
    else:
        with st.spinner("🔍 ANALYZING THE CRINGE..."):
            try:
                image = Image.open(uploaded_file)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Map intensity levels
                intensity_map = {
                    "🌶️ MILD": "You are a witty friend. Roast this image with lighthearted, playful humor. Keep it friendly. Max 80 words.",
                    "🔥 HOT": "You are a stand-up comedian. Deliver a scorching, sarcastic roast of everything in this image. Point out funny details. Max 110 words.",
                    "☠️ INFERNO": "You are a roast god. Unleash a catastrophic, no-mercy, poetic destruction of everything in this image. Be merciless. Max 140 words."
                }
                
                system_prompt = intensity_map[intensity]
                
                # Generate roast
                response = model.generate_content([system_prompt, image])
                roast_text = response.text
                
                # Display result in a nice container
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color:#FFD700; text-align:center; margin-top:0;">🔥 ROAST DELIVERED</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="roast-text">{roast_text}</div>', unsafe_allow_html=True)
                
                # Score visualization
                st.markdown('<h3 style="color:#00F5FF; margin-top:2rem; margin-bottom:1.5rem;">📊 ROAST METRICS</h3>', unsafe_allow_html=True)
                
                # Dynamic scores based on intensity
                scores = {
                    "SAVAGERY": 75 if intensity == "🌶️ MILD" else 85 if intensity == "🔥 HOT" else 95,
                    "CREATIVITY": 80,
                    "ACCURACY": 88,
                    "DAMAGE": 82 if intensity == "🌶️ MILD" else 88 if intensity == "🔥 HOT" else 94
                }
                
                for label, value in scores.items():
                    st.markdown(f'''
                    <div class="score-label">{label}<span>{value}%</span></div>
                    <div class="score-bar">
                        <div class="score-fill" style="width:{value}%; --fill-percent:{value}%;"></div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")