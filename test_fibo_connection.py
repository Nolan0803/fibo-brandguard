#!/usr/bin/env python3
"""
Test script to debug FIBO connection and credits
Run this locally to see detailed logs without Streamlit
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_env_setup():
    """Test environment variable setup"""
    logger.info("=== Testing Environment Setup ===")
    
    # Load environment
    load_dotenv()
    
    # Check HF token
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        logger.info(f"✅ HF_TOKEN found - Length: {len(hf_token)} characters")
        logger.info(f"✅ Token prefix: {hf_token[:10]}...")
        
        # Check if it looks like a valid HF token
        if hf_token.startswith('hf_'):
            logger.info("✅ Token has correct HuggingFace prefix")
        else:
            logger.warning("⚠️ Token doesn't start with 'hf_' - might be invalid")
            
    else:
        logger.error("❌ HF_TOKEN not found in environment")
        return False
        
    return True

def test_fibo_client():
    """Test FIBO client initialization and simple generation"""
    logger.info("=== Testing FIBO Client ===")
    
    try:
        from fibo_client import FIBOClient
        
        # Initialize client
        client = FIBOClient()
        logger.info("✅ FIBOClient initialized")
        
        # Test validation
        validation = client.validate_setup()
        logger.info(f"📊 Client validation: {validation}")
        
        # Simple test prompt
        test_prompt = {
            "scene": "a simple red apple on a white background",
            "style": "clean, minimal, product photography",
            "mood": "professional"
        }
        
        logger.info(f"🧪 Testing with simple prompt: {test_prompt}")
        
        # Try to generate 1 image
        results = client.generate_images(test_prompt, num_variants=1)
        
        if results:
            result = results[0]
            logger.info(f"✅ Generation successful!")
            logger.info(f"📊 Status: {result.get('status')}")
            logger.info(f"🖼️ Has image: {bool(result.get('image'))}")
            logger.info(f"📝 Metadata: {result.get('metadata', {})}")
            
            if result.get('status') == 'success':
                logger.info("🎉 SUCCESS: Real image generation working!")
                return True
            else:
                logger.warning(f"⚠️ Generation in safe mode: {result.get('status')}")
                return False
        else:
            logger.error("❌ No results returned")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing FIBO client: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        return False

def test_huggingface_api():
    """Test direct HuggingFace API connection"""
    logger.info("=== Testing Direct HuggingFace API ===")
    
    try:
        from huggingface_hub import InferenceClient
        
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            logger.error("❌ No HF_TOKEN for API test")
            return False
            
        # Test client initialization
        client = InferenceClient("briaai/FIBO", token=hf_token)
        logger.info("✅ InferenceClient initialized")
        
        # Test simple text-to-image call
        logger.info("🧪 Testing direct API call...")
        
        try:
            result = client.text_to_image("a simple red apple")
            logger.info(f"✅ API call successful! Response type: {type(result)}")
            
            # Try to process the result
            if hasattr(result, 'size'):
                logger.info(f"🖼️ Image size: {result.size}")
            
            return True
            
        except Exception as api_error:
            logger.error(f"❌ API call failed: {api_error}")
            logger.error(f"Error type: {type(api_error).__name__}")
            
            # Check for specific error patterns
            error_str = str(api_error).lower()
            if 'quota' in error_str or 'credits' in error_str:
                logger.error("💰 LIKELY CAUSE: Out of HuggingFace credits/quota")
            elif 'unauthorized' in error_str or 'token' in error_str:
                logger.error("🔑 LIKELY CAUSE: Invalid or expired token")
            elif 'rate limit' in error_str:
                logger.error("🚦 LIKELY CAUSE: Rate limited - try again later")
            
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in API test: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 FIBO BrandGuard Connection Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: Environment setup
    if not test_env_setup():
        all_passed = False
        print("\n❌ Environment setup failed - check your .env file")
        return
    
    print()
    
    # Test 2: FIBO client
    if not test_fibo_client():
        all_passed = False
    
    print()
    
    # Test 3: Direct API
    if not test_huggingface_api():
        all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED - Image generation should work!")
    else:
        print("❌ SOME TESTS FAILED - Check logs above for issues")
        print("\n💡 Common solutions:")
        print("   - Check HuggingFace token is valid and not expired")
        print("   - Verify you have credits/quota remaining")
        print("   - Try again later if rate limited")
        print("   - Make sure .env file is in the correct location")

if __name__ == "__main__":
    main()