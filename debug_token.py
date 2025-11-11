#!/usr/bin/env python3
"""
Debug script to test FIBO token access in Streamlit Cloud environment
"""

import os
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

def main():
    st.title("🔍 FIBO Token Debug")
    
    # Load from .env file
    load_dotenv()
    env_token = os.getenv("HF_TOKEN")
    
    # Try to get from Streamlit secrets
    secrets_token = None
    try:
        if hasattr(st, 'secrets') and 'HF_TOKEN' in st.secrets:
            secrets_token = st.secrets["HF_TOKEN"]
    except Exception as e:
        st.error(f"Error accessing secrets: {e}")
    
    st.write("## Token Status")
    st.write(f"**Environment (.env) token:** {'✅ Found' if env_token else '❌ Not found'}")
    if env_token:
        st.write(f"Preview: `{env_token[:15]}...`")
    
    st.write(f"**Streamlit secrets token:** {'✅ Found' if secrets_token else '❌ Not found'}")
    if secrets_token:
        st.write(f"Preview: `{secrets_token[:15]}...`")
    
    # Use the available token
    token = secrets_token or env_token
    
    if not token:
        st.error("❌ No HF_TOKEN found in either .env file or Streamlit secrets")
        return
    
    st.write("## Testing FIBO Access")
    
    try:
        # Test client creation
        client = InferenceClient("briaai/FIBO", token=token)
        st.success("✅ InferenceClient created successfully")
        
        if st.button("🧪 Test Image Generation"):
            with st.spinner("Testing image generation..."):
                try:
                    result = client.text_to_image("A simple test image of a red apple")
                    st.success("✅ Image generation successful!")
                    st.image(result, caption="Test generation result")
                    st.write(f"**Result type:** `{type(result)}`")
                    if hasattr(result, 'size'):
                        st.write(f"**Image size:** {result.size}")
                except Exception as e:
                    st.error(f"❌ Image generation failed: {e}")
                    st.error(f"**Error type:** `{type(e).__name__}`")
                    
                    # Try to get more details
                    if hasattr(e, 'response'):
                        if hasattr(e.response, 'status_code'):
                            st.error(f"**HTTP Status:** {e.response.status_code}")
                        if hasattr(e.response, 'text'):
                            st.error(f"**Response:** {e.response.text}")
                    
    except Exception as e:
        st.error(f"❌ Failed to create InferenceClient: {e}")
        st.error(f"**Error type:** `{type(e).__name__}`")

if __name__ == "__main__":
    main()