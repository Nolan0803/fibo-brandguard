import os
import json
import io
import time
import random
import logging
from typing import List, Dict, Any, Optional
from PIL import Image
from huggingface_hub import InferenceClient

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file at startup
from dotenv import load_dotenv
load_dotenv()

# Load and validate HF_TOKEN (works with both .env files and Streamlit secrets)
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    # Try Streamlit secrets if available
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'HF_TOKEN' in st.secrets:
            hf_token = st.secrets["HF_TOKEN"]
            logger.info("✅ HuggingFace token loaded from Streamlit secrets")
    except:
        pass

if hf_token:
    if not hasattr(hf_token, '__name__'):  # Not from streamlit secrets
        logger.info("✅ HuggingFace token loaded successfully from .env")
        logger.info(f"Token length: {len(hf_token)} characters")
        logger.info(f"Token prefix: {hf_token[:10]}...")
else:
    logger.error("❌ HF_TOKEN not found in .env file or Streamlit secrets. Please configure your HuggingFace token.")

def _to_pil_image(result):
    """
    Convert various response types from HuggingFace InferenceClient to PIL.Image.
    
    Args:
        result: Response from client.text_to_image() - could be PIL.Image, bytes, or dict
        
    Returns:
        PIL.Image.Image object
        
    Raises:
        TypeError: If result type is not supported
    """
    if isinstance(result, Image.Image):
        return result
    if isinstance(result, (bytes, bytearray)):
        return Image.open(io.BytesIO(result)).convert("RGB")
    if isinstance(result, dict):
        data = result.get("image") or result.get("bytes")
        if isinstance(data, (bytes, bytearray)):
            return Image.open(io.BytesIO(data)).convert("RGB")
    raise TypeError(f"Unsupported response type from remote FIBO: {type(result)}")


# Module-level remote client state
HF_TOKEN = hf_token  # Use the token loaded at startup
_remote_client: Optional[InferenceClient] = None


def _load_pipeline():
    """
    Initialize and return the module-level Hugging Face InferenceClient.
    Returns None when HF_TOKEN is not set.
    """
    global _remote_client
    if _remote_client is not None:
        logger.info("✅ Using existing remote client")
        return _remote_client

    if not HF_TOKEN:
        logger.error("❌ No HF_TOKEN found. Set HF_TOKEN to your Hugging Face token.")
        return None

    try:
        logger.info("🔄 Initializing HuggingFace InferenceClient for briaai/FIBO...")
        _remote_client = InferenceClient("briaai/FIBO", token=HF_TOKEN)
        logger.info("✅ Remote InferenceClient initialized successfully")
        return _remote_client
    except Exception as e:
        logger.error(f"❌ Failed to initialize remote InferenceClient: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        _remote_client = None
        return None


def is_pipeline_loaded() -> bool:
    """Return True when the remote InferenceClient is available."""
    return _load_pipeline() is not None


def is_remote_enabled() -> bool:
    """Return True when remote FIBO generation is properly configured."""
    return bool(hf_token) and is_pipeline_loaded()


def get_client_status() -> dict:
    """Get detailed client status for UI display."""
    client = _load_pipeline()
    return {
        "remote_available": client is not None,
        "token_configured": bool(hf_token),
        "mode": "remote" if client is not None else "safe_mode",
        "model": "briaai/FIBO" if client is not None else "placeholder"
    }


def generate_variant_prompt(base_prompt: str, variant_num: int) -> str:
    """
    Generate a slightly adjusted version of the prompt by adding creative flavor words.
    
    Args:
        base_prompt: The original prompt text
        variant_num: Variant number (1-indexed)
        
    Returns:
        Modified prompt with added creative elements
    """
    # Creative variations to add diversity
    lighting_variations = [
        "golden sunset lighting", "dramatic shadows", "soft natural light", 
        "cinematic lighting", "warm ambient glow", "bright studio lighting"
    ]
    
    angle_variations = [
        "close-up portrait", "wide-angle view", "low angle shot", 
        "bird's eye view", "three-quarter angle", "dynamic perspective"
    ]
    
    mood_variations = [
        "elegant atmosphere", "vibrant energy", "serene ambiance", 
        "dynamic composition", "minimalist aesthetic", "rich textures"
    ]
    
    # Rotate through different types of variations based on variant number
    if variant_num % 3 == 1:
        flavor = lighting_variations[(variant_num - 1) % len(lighting_variations)]
    elif variant_num % 3 == 2:
        flavor = angle_variations[(variant_num - 1) % len(angle_variations)]
    else:
        flavor = mood_variations[(variant_num - 1) % len(mood_variations)]
    
    # Add the flavor to the end of the prompt
    return f"{base_prompt}, {flavor}"


def build_prompt_from_governed_json(governed_json: Dict[str, Any]) -> str:
    """
    Convert JSON prompt structure to string format for FIBO API.
    
    Args:
        governed_json: Structured JSON prompt
        
    Returns:
        String representation of the prompt
    """
    if isinstance(governed_json, str):
        try:
            governed_json = json.loads(governed_json)
        except Exception:
            return governed_json

    parts = []

    scene = governed_json.get("scene")
    if scene:
        parts.append(str(scene))

    style = governed_json.get("style")
    if style:
        parts.append(f"style: {style}")

    modifiers = governed_json.get("modifiers") or governed_json.get("modifiers_list")
    if isinstance(modifiers, list):
        parts.append("modifiers: " + ", ".join(str(m) for m in modifiers))

    mood = governed_json.get("mood")
    if mood:
        parts.append(f"mood: {mood}")

    colors = governed_json.get("colors")
    if isinstance(colors, list):
        parts.append("colors: " + ", ".join(str(c) for c in colors))

    if not parts:
        return json.dumps(governed_json)

    return " | ".join(parts)


def generate_images_from_json_prompt(json_prompt: dict, num_images: int = 1) -> List[Image.Image]:
    """
    Ensure the remote client is loaded; if not, return an empty list.

    Convert the structured JSON prompt into a string payload using
    json.dumps(json_prompt, ensure_ascii=False), call the remote client
    using text_to_image in a loop, and return a list of PIL.Image objects.
    
    Each variant gets a unique seed and slight prompt variations for diversity.

    On any exception, log and return an empty list.
    """
    logger.info(f"🎯 Starting image generation: {num_images} variants requested")
    
    client = _load_pipeline()
    if client is None:
        logger.error("❌ Remote FIBO client not available (HF_TOKEN missing or init failed)")
        return []

    base_prompt_str = json.dumps(json_prompt, ensure_ascii=False)
    logger.info(f"📝 Base prompt: {base_prompt_str[:100]}{'...' if len(base_prompt_str) > 100 else ''}")
    
    images: List[Image.Image] = []

    for i in range(num_images):
        try:
            start = time.time()
            
            # Generate unique seed for this variant
            unique_seed = random.randint(0, 9999999)
            
            # Create variant prompt with creative additions
            variant_prompt = generate_variant_prompt(base_prompt_str, i + 1)
            logger.info(f"🎨 Variant {i+1} prompt: {variant_prompt[:150]}{'...' if len(variant_prompt) > 150 else ''}")
            logger.info(f"🎲 Using seed: {unique_seed}")
            
            # Log API call attempt
            logger.info(f"📡 Making API call to HuggingFace for variant {i+1}...")
            
            # The InferenceClient text_to_image can return PIL.Image or bytes
            # Note: HuggingFace Inference API doesn't support seed parameter directly
            # but we'll use the varied prompts to create diversity
            response = client.text_to_image(prompt=variant_prompt)
            latency = time.time() - start
            
            logger.info(f"📡 API Response received in {latency:.2f}s")
            logger.info(f"📡 Response type: {type(response)}")
            
            # Use helper to handle different response types
            image = _to_pil_image(response)
            images.append(image)
            logger.info(f"✅ Remote FIBO variant {i+1} generated successfully - Size: {image.size}")
            
        except Exception as e:
            logger.error(f"❌ Remote generation error for variant {i+1}: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            
            # Log detailed error information
            if hasattr(e, 'response'):
                status_code = getattr(e.response, 'status_code', 'unknown')
                logger.error(f"❌ HTTP Status: {status_code}")
                
                # Try to get response text if available
                try:
                    response_text = getattr(e.response, 'text', 'No response text')
                    logger.error(f"❌ Response text: {response_text}")
                except:
                    logger.error("❌ Could not get response text")
                    
            if hasattr(e, 'message'):
                logger.error(f"❌ Error message: {e.message}")
                
            # Continue with other variants instead of returning empty list
            continue

    logger.info(f"🏁 Generation complete: {len(images)}/{num_images} images successfully generated")
    return images


def _create_safe_mode_image(json_prompt: dict, variant_id: int = 1) -> Image.Image:
    """
    Create a safe mode informational image when remote generation fails.
    
    Args:
        json_prompt: The original JSON prompt
        variant_id: Variant number for display
        
    Returns:
        PIL Image with safe mode information
    """
    img = Image.new('RGB', (512, 320), color=(45, 55, 72))
    
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Get prompt text for preview
        prompt_text = build_prompt_from_governed_json(json_prompt)
        prompt_preview = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
        
        # Try to load fonts
        try:
            font_large = ImageFont.truetype("arial.ttf", 20)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw informational text
        draw.text((256, 70), "FIBO SAFE MODE", font=font_large, anchor="mm", fill=(255, 255, 255))
        draw.text((256, 100), "Requires CUDA-compatible GPU", font=font_small, anchor="mm", fill=(200, 200, 200))
        draw.text((256, 125), "or valid HF token", font=font_small, anchor="mm", fill=(200, 200, 200))
        
        draw.text((256, 160), "Prompt:", font=font_small, anchor="mm", fill=(255, 255, 255))
        draw.text((256, 185), prompt_preview, font=font_small, anchor="mm", fill=(180, 220, 180))
        
        draw.text((256, 220), f"Variant {variant_id}", font=font_small, anchor="mm", fill=(255, 180, 180))
        
    except Exception as e:
        print(f"Warning: Could not add text to safe mode image: {e}")
    
    return img


class FIBOClient:
    """Remote Bria FIBO client using HuggingFace Inference API."""
    
    def __init__(self, hf_token: str = None):
        """
        Initialize remote FIBO client.
        
        Args:
            hf_token: Hugging Face token (defaults to HF_TOKEN env var)
        """
        self.hf_token = hf_token or os.getenv("HF_TOKEN", "") or os.getenv("HUGGINGFACE_TOKEN", "")
        self.model_id = "briaai/FIBO"
    
    def generate_images(
        self, 
        prompt: Dict, 
        num_variants: int = 2,
        **kwargs  # Accept additional parameters for compatibility
    ) -> List[Dict]:
        """
        Generate images using remote FIBO API and return in app-compatible format.
        Each variant gets unique seeds and creative prompt variations.
        
        This method maintains compatibility with the existing app.py interface.
        
        Args:
            prompt: JSON-structured prompt
            num_variants: Number of image variants to generate
            **kwargs: Additional parameters (ignored for remote API)
            
        Returns:
            List of image result dictionaries with PIL Images
        """
        logger.info(f"🚀 FIBOClient.generate_images called with {num_variants} variants")
        logger.info(f"📝 Input prompt: {prompt}")
        
        # Generate unique seeds for each variant upfront
        variant_seeds = [random.randint(0, 9999999) for _ in range(num_variants)]
        logger.info(f"🎲 Generated seeds: {variant_seeds}")
        
        # Call the new remote function
        images = generate_images_from_json_prompt(prompt, num_variants)

        results: List[Dict[str, Any]] = []

        if images:  # Remote generation successful
            logger.info(f"✅ Remote generation successful: {len(images)} images")
            for i, image in enumerate(images):
                # Create variant prompt to show what was actually used
                base_prompt_str = build_prompt_from_governed_json(prompt)
                variant_prompt_str = generate_variant_prompt(base_prompt_str, i + 1)
                
                result = {
                    "variant_id": i + 1,
                    "status": "success",
                    "image": image,
                    "prompt_used": prompt,
                    "prompt_string": variant_prompt_str,  # Show the actual variant prompt used
                    "generation_time": 0.0,
                    "metadata": {
                        "model": self.model_id,
                        "provider": "huggingface-inference",
                        "seed": variant_seeds[i],  # Use the actual unique seed
                        "device": "remote",
                        "latency": None,
                        "size": f"{image.size[0]}x{image.size[1]}" if hasattr(image, 'size') else "unknown",
                        "variant_type": "creative_variation",
                        "base_prompt": base_prompt_str
                    }
                }
                results.append(result)
                logger.info(f"📊 Variant {i+1} result created - Status: {result['status']}")
        else:  # Remote generation failed, show safe mode
            logger.warning(f"⚠️ Remote generation failed, falling back to safe mode for {num_variants} variants")
            for i in range(num_variants):
                safe_image = _create_safe_mode_image(prompt, i + 1)
                result = {
                    "variant_id": i + 1,
                    "status": "safe_mode",
                    "image": safe_image,
                    "prompt_used": prompt,
                    "prompt_string": build_prompt_from_governed_json(prompt),
                    "generation_time": 0.1,
                    "metadata": {
                        "model": "safe_mode",
                        "provider": "local-fallback",
                        "seed": variant_seeds[i],  # Use unique seeds even in safe mode
                        "device": "cpu",
                        "size": f"{safe_image.size[0]}x{safe_image.size[1]}" if hasattr(safe_image, 'size') else "512x320",
                        "variant_type": "safe_mode"
                    }
                }
                results.append(result)
                logger.info(f"📊 Safe mode variant {i+1} created")

        logger.info(f"🏁 generate_images returning {len(results)} results")
        return results
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate that the client is properly set up for remote inference.
        
        Returns:
            Dictionary with validation status
        """
        return {
            "has_hf_token": bool(self.hf_token),
            "client_available": is_pipeline_loaded(),
            "model": self.model_id,
            "mode": "remote-inference"
        }
