import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Get API key from Streamlit Secrets (cloud) or environment variables (local)
try:
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("âŒ GEMINI_API_KEY not found. Please add it to Streamlit Secrets.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"âŒ Configuration error: {e}")
    st.stop()

# Set up the Streamlit page layout with beautiful theme
st.set_page_config(
    page_title="AI Vision Roast System",
    page_icon="ðŸ”¥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
        * {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        html, body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        
        .stApp, [data-testid="stApp"] {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%) !important;
        }
        
        /* Main header styling */
        .main-header {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%) !important;
            padding: 40px 20px !important;
            border-radius: 15px !important;
            text-align: center !important;
            margin-bottom: 30px !important;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3) !important;
        }
        
        .main-header h1 {
            font-size: 3em !important;
            font-weight: 800 !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
            margin: 0 !important;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1.1em !important;
            margin-top: 10px !important;
        }
        
        /* Card styling */
        .card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
            border-color: rgba(255, 107, 53, 0.5);
            box-shadow: 0 15px 40px rgba(255, 107, 53, 0.2);
        }
        
        .card-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #ff6b35;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Intensity selector styling */
        .intensity-container {
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .intensity-btn {
            flex: 1;
            min-width: 100px;
            padding: 12px 20px;
            border-radius: 10px;
            border: 2px solid rgba(255, 107, 53, 0.3);
            background: rgba(255, 107, 53, 0.1);
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 1em;
        }
        
        .intensity-btn:hover {
            border-color: #ff6b35;
            background: rgba(255, 107, 53, 0.2);
            transform: translateY(-2px);
        }
        
        /* Upload area styling */
        .upload-area {
            border: 2px dashed rgba(255, 107, 53, 0.5);
            border-radius: 10px;
            padding: 40px 20px;
            text-align: center;
            background: rgba(255, 107, 53, 0.05);
            transition: all 0.3s ease;
        }
        
        /* Roast button styling */
        .roast-button {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.1em !important;
            padding: 15px 30px !important;
            border-radius: 10px !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4) !important;
            margin-top: 20px !important;
        }
        
        .roast-button:hover {
            box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Result styling */
        .result-container {
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(247, 147, 30, 0.05) 100%);
            border-left: 4px solid #ff6b35;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .result-text {
            color: #ffffff;
            font-size: 1.05em;
            line-height: 1.8;
            font-family: 'Georgia', serif;
        }
        
        /* Image styling */
        .image-container {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.2);
            border: 2px solid rgba(255, 107, 53, 0.3);
        }
        
        /* Status messages */
        .status-success {
            background: rgba(76, 175, 80, 0.2);
            border-left: 4px solid #4CAF50;
            color: #A5D6A7;
        }
        
        .status-error {
            background: rgba(244, 67, 54, 0.2);
            border-left: 4px solid #f44336;
            color: #EF9A9A;
        }
        
        /* Responsive text */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2em;
            }
            
            .card {
                padding: 20px;
            }
            
            .card-title {
                font-size: 1.2em;
            }
        }
        
        /* Spinner animation */
        .spinner {
            color: #ff6b35;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>ðŸ”¥ AI Vision Roast System</h1>
        <p>Powered by Gemini 2.5 Flash - Upload an image and get roasted!</p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
        <div class="card">
            <div class="card-title">ðŸ“¸ Step 1: Upload Image</div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag and drop your image here or click to browse",
        type=["jpg", "png", "webp"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
            <hr style="border: none; border-top: 1px solid rgba(255, 107, 53, 0.2); margin: 20px 0;">
            <div style="font-size: 1em; font-weight: 600; color: #ff6b35; margin-bottom: 15px;">
                ðŸŽ¯ Choose Roast Intensity
            </div>
    """, unsafe_allow_html=True)
    
    intensity = st.segmented_control(
        "Intensity Level",
        ["Mild", "Medium", "Savage"],
        default="Medium",
        label_visibility="collapsed"
    )
    
    intensity_descriptions = {
        "Mild": "ðŸ‘¶ Lighthearted and friendly",
        "Medium": "ðŸŽ­ Witty and sarcastic",
        "Savage": "ðŸ”¥ Mercilessly funny"
    }
    
    st.markdown(f"""
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em; margin: 10px 0;">
            {intensity_descriptions[intensity]}
        </p>
    """, unsafe_allow_html=True)
    
    roast_button = st.button(
        "ðŸ”¥ ROAST ME ðŸ”¥",
        use_container_width=True,
        key="roast_btn"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card">
            <div class="card-title">âœ¨ Step 2: View Result</div>
    """, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process roast when button clicked
        if roast_button:
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with progress_placeholder.container():
                st.markdown("""
                    <div style="text-align: center; padding: 20px;">
                        <p style="color: #ff6b35; font-size: 1.1em; font-weight: 600;">
                            ðŸ”¥ Analyzing the cringe...
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                progress_bar = st.progress(0)
            
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Prompts based on intensity
                prompts = {
                    "Mild": "You are a witty friend. Look at this image and give a lighthearted, playful tease about it. Keep it friendly and fun. Make it 2-3 sentences.",
                    "Medium": "You are a stand-up comedian. Roast this image with witty, sarcastic jokes. Point out funny or questionable details. Make it entertaining! 3-4 sentences.",
                    "Savage": "You are a savage roaster. Be mercilessly and hilariously funny about every awkward detail in this image. Don't hold back! (But stay within safety guidelines). 3-5 sentences of pure comedy."
                }
                
                progress_bar.progress(50)
                response = model.generate_content([prompts[intensity], image])
                progress_bar.progress(100)
                
                # Display result
                progress_placeholder.empty()
                
                st.markdown("""
                    <div class="result-container">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                            <span style="font-size: 1.5em;">âš¡</span>
                            <span style="color: #ff6b35; font-weight: 700; font-size: 1.1em;">
                                AI Generated Roast
                            </span>
                        </div>
                        <div class="result-text">
                """, unsafe_allow_html=True)
                
                st.markdown(response.text)
                
                st.markdown("""
                        </div>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 107, 53, 0.3);">
                            <small style="color: rgba(255, 255, 255, 0.6);">
                                Powered by Google Gemini 2.5 Flash
                            </small>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                progress_placeholder.empty()
                st.markdown(f"""
                    <div class="result-container status-error">
                        <strong>âŒ Error:</strong> {str(e)}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 60px 20px; color: rgba(255, 255, 255, 0.5);">
                <p style="font-size: 3em; margin-bottom: 15px;">ðŸ“¸</p>
                <p style="font-size: 1.1em;">Upload an image to get started!</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    JPG, PNG, or WebP formats supported
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="
        text-align: center;
        padding: 30px 20px;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 107, 53, 0.2);
        color: rgba(255, 255, 255, 0.6);
    ">
        <p style="margin: 0; font-size: 0.9em;">
            Built with â¤ï¸ using Streamlit & Google Gemini API
        </p>
    </div>
""", unsafe_allow_html=True)
