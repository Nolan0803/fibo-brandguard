"""
VLM Agent Module
Handles Vision-Language Model operations and JSON prompt construction.
"""

import json
from typing import Dict, List, Optional


class VLMAgent:
    """Agent for constructing and managing JSON-native prompts for FIBO."""
    
    def __init__(self):
        """Initialize VLM Agent."""
        self.prompt_templates = {
            "basic": {
                "scene": "",
                "style": "photorealistic",
                "modifiers": []
            },
            "product": {
                "scene": "",
                "style": "product photography",
                "modifiers": ["high quality", "professional lighting"],
                "elements": []
            },
            "creative": {
                "scene": "",
                "style": "artistic",
                "modifiers": ["creative", "unique"],
                "mood": "inspiring"
            }
        }
    
    def create_prompt(
        self,
        scene_description: str,
        style: str = "photorealistic",
        modifiers: Optional[List[str]] = None,
        colors: Optional[List[str]] = None,
        elements: Optional[List[str]] = None,
        mood: Optional[str] = None
    ) -> Dict:
        """
        Create a JSON-native prompt for FIBO.
        
        Args:
            scene_description: Main scene description
            style: Visual style
            modifiers: List of modifiers (quality, lighting, etc.)
            colors: Preferred colors
            elements: Specific elements to include
            mood: Desired mood
            
        Returns:
            JSON-structured prompt
        """
        prompt = {
            "scene": scene_description,
            "style": style
        }
        
        if modifiers:
            prompt["modifiers"] = modifiers
        
        if colors:
            prompt["colors"] = colors
        
        if elements:
            prompt["elements"] = elements
        
        if mood:
            prompt["mood"] = mood
        
        # Add metadata
        prompt["metadata"] = {
            "version": "1.0",
            "prompt_type": "json_native"
        }
        
        return prompt
    
    def get_template(self, template_name: str) -> Dict:
        """
        Get a prompt template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template dictionary
        """
        return self.prompt_templates.get(template_name, self.prompt_templates["basic"]).copy()
    
    def apply_template(
        self,
        template_name: str,
        scene: str,
        **kwargs
    ) -> Dict:
        """
        Apply a template with custom values.
        
        Args:
            template_name: Name of the template to use
            scene: Scene description
            **kwargs: Additional fields to override
            
        Returns:
            Customized prompt
        """
        template = self.get_template(template_name)
        template["scene"] = scene
        
        # Update with any additional kwargs
        for key, value in kwargs.items():
            if value is not None:
                template[key] = value
        
        # Add metadata
        if "metadata" not in template:
            template["metadata"] = {}
        template["metadata"]["template"] = template_name
        template["metadata"]["version"] = "1.0"
        
        return template
    
    def validate_prompt_structure(self, prompt: Dict) -> bool:
        """
        Validate that prompt has required structure.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check for required fields
        if "scene" not in prompt:
            return False
        
        # Check that scene is not empty
        if not prompt["scene"].strip():
            return False
        
        return True
    
    def format_prompt_display(self, prompt: Dict) -> str:
        """
        Format prompt for display.
        
        Args:
            prompt: Prompt dictionary
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(prompt, indent=2)
    
    def extract_keywords(self, prompt: Dict) -> List[str]:
        """
        Extract key elements from prompt for analysis.
        
        Args:
            prompt: Prompt dictionary
            
        Returns:
            List of keywords
        """
        keywords = []
        
        # Extract from scene
        if "scene" in prompt:
            keywords.extend(prompt["scene"].split())
        
        # Extract from style
        if "style" in prompt:
            keywords.append(prompt["style"])
        
        # Extract from elements
        if "elements" in prompt:
            keywords.extend(prompt["elements"])
        
        # Extract from modifiers
        if "modifiers" in prompt:
            keywords.extend(prompt["modifiers"])
        
        return keywords
