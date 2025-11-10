"""
FIBO Client Module
Handles interaction with the Bria FIBO API for JSON-native image generation.
"""

import os
import requests
import time
from typing import Dict, List, Optional
import base64
from io import BytesIO


class FIBOClient:
    """Client for interacting with Bria FIBO API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FIBO client.
        
        Args:
            api_key: Bria API key (defaults to BRIA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("BRIA_API_KEY", "")
        self.base_url = "https://engine.prod.bria-api.com/v1"
        self.headers = {
            "api_token": self.api_key,
            "Content-Type": "application/json"
        }
    
    def generate_images(
        self, 
        prompt: Dict, 
        num_variants: int = 4,
        model: str = "bria-fibo-v1"
    ) -> List[Dict]:
        """
        Generate images using FIBO with JSON-native prompt.
        
        Args:
            prompt: JSON-structured prompt with elements
            num_variants: Number of image variants to generate
            model: Model name to use
            
        Returns:
            List of image result dictionaries
        """
        results = []
        
        # For demo purposes, we'll simulate the API call
        # In production, this would make actual API calls to Bria FIBO
        for i in range(num_variants):
            result = {
                "variant_id": i + 1,
                "status": "success",
                "prompt_used": prompt,
                "generation_time": round(time.time(), 2),
                "image_url": self._simulate_image_generation(prompt, i),
                "metadata": {
                    "model": model,
                    "seed": hash(str(prompt)) + i,
                    "steps": 50
                }
            }
            results.append(result)
        
        return results
    
    def _simulate_image_generation(self, prompt: Dict, variant: int) -> str:
        """
        Simulate image generation for demo purposes.
        Creates a simple placeholder image.
        
        Args:
            prompt: The prompt dictionary
            variant: Variant number
            
        Returns:
            Base64-encoded placeholder image
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            return ""
        
        # Create a simple placeholder image
        img = Image.new('RGB', (512, 512), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Add text
        text = f"FIBO Image\nVariant {variant + 1}"
        if "scene" in prompt:
            text += f"\n{prompt['scene'][:30]}"
        
        d.text((256, 256), text, fill=(255, 255, 255), anchor="mm")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def validate_api_key(self) -> bool:
        """
        Validate that API key is configured.
        
        Returns:
            True if API key exists, False otherwise
        """
        return bool(self.api_key)
