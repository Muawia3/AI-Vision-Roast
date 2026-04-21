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
        st.error("❌ GEMINI_API_KEY not found. Please add it to Streamlit Secrets.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Configuration error: {e}")
    st.stop()

# Set up the Streamlit page layout
st.set_page_config(page_title="AI Vision Roast System", page_icon="🔥", layout="wide")

st.title("🔥 AI Vision Roast System")
st.markdown("**Powered by Gemini 2.5 Flash**")

# Create the two-panel layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("STEP 1 — UPLOAD")
    # File Uploader supporting the formats you specified
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png", "webp"])
    
    # Roast Intensity Selector
    intensity = st.radio("Roast intensity", ["Mild", "Medium", "Savage"], horizontal=True)
    
    # Action Button
    roast_button = st.button("Roast Me ↗", use_container_width=True)

with col2:
    st.subheader("STEP 2 — RESULT")
    
    if uploaded_file is not None:
        # Display the uploaded image preview
        image = Image.open(uploaded_file)
        st.image(image, caption="Image preview", use_container_width=True)
        
        # Trigger the roast when the button is clicked
        if roast_button:
            with st.spinner("Analyzing the cringe..."):
                try:
                    # Initialize the model
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Dynamic Prompting based on user intensity selection
                    if intensity == "Mild":
                        system_prompt = "You are a witty friend. Look at this image and give a lighthearted, playful tease. Keep it friendly."
                    elif intensity == "Medium":
                        system_prompt = "You are a stand-up comedian. Roast this image with some good, sarcastic jokes. Point out funny details."
                    else:
                        system_prompt = "You are a savage roaster. Be mercilessly funny, highlight every awkward detail and questionable choice in this image, but do not violate safety guidelines."
                    
                    # Generate the response
                    response = model.generate_content([system_prompt, image])
                    
                    # Display the result
                    st.success("AI Generated | Gemini 2.5 Flash")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")