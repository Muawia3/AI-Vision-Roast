# 🔥 AI Vision Roast System

A beautiful, AI-powered web app that analyzes images and delivers hilarious roasts using Google's Gemini 2.5 Flash API.

## Features

✨ **Beautiful Modern UI** - Orange gradient theme with glassmorphism effects  
📱 **Fully Responsive** - Works perfectly on mobile, tablet, and desktop  
🎨 **Smooth Animations** - Hover effects and professional transitions  
🔥 **Three Roast Levels** - Mild, Medium, or Savage roasts  
⚡ **Real-time Processing** - Fast image analysis with progress indicators  
🚀 **Production Ready** - Deployed on Streamlit Cloud  

## Technologies

- **Streamlit** - Web framework
- **Google Gemini 2.5 Flash** - AI model for image analysis
- **Python** - Backend
- **PIL/Pillow** - Image processing
- **CSS3** - Modern styling with gradients and animations

## How to Use

1. Upload an image (JPG, PNG, or WebP)
2. Select roast intensity (Mild, Medium, or Savage)
3. Click "ROAST ME"
4. Get your hilarious AI-generated roast!

## Setup Local Development

```bash
# Clone repository
git clone https://github.com/Muawia3/AI-Vision-Roast.git
cd AI-Vision-Roast

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run app
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select this repository
4. Set main file to `app.py`
5. Add `GEMINI_API_KEY` in Secrets

## Requirements

- Python 3.8+
- streamlit>=1.39.0
- google-generativeai==0.8.6
- pillow==10.2.0
- python-dotenv==1.2.2

## API Key

Get your free Gemini API key from: https://ai.google.dev/

---

**Created with ❤️ using Streamlit & Google Gemini**
