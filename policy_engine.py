"""
Policy Engine Module
Enforces brand policies and guidelines on image generation prompts.
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime


class PolicyEngine:
    """Engine for enforcing brand policies on prompts."""
    
    def __init__(self, brand_profile_path: str = "brand_profile.json"):
        """
        Initialize policy engine with brand profile.
        
        Args:
            brand_profile_path: Path to brand profile JSON file
        """
        self.brand_profile = self._load_brand_profile(brand_profile_path)
        self.violations = []
        self.warnings = []
    
    def _load_brand_profile(self, path: str) -> Dict:
        """Load brand profile from JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "brand_name": "Default Brand",
                "policies": {
                    "prohibited_content": [],
                    "allowed_themes": [],
                    "color_preferences": []
                }
            }
    
    def validate_prompt(self, prompt: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate prompt against brand policies.
        
        Args:
            prompt: JSON prompt to validate
            
        Returns:
            Tuple of (is_valid, violations, warnings)
        """
        self.violations = []
        self.warnings = []
        
        # Check for prohibited content
        self._check_prohibited_content(prompt)
        
        # Check theme alignment
        self._check_theme_alignment(prompt)
        
        # Check color preferences
        self._check_color_preferences(prompt)
        
        # Check quality requirements
        self._check_quality_requirements(prompt)
        
        is_valid = len(self.violations) == 0
        
        return is_valid, self.violations, self.warnings
    
    def _check_prohibited_content(self, prompt: Dict):
        """Check for prohibited content in prompt."""
        prohibited = self.brand_profile.get("policies", {}).get("prohibited_content", [])
        
        # Convert prompt to string for checking
        prompt_str = json.dumps(prompt).lower()
        
        for term in prohibited:
            if term.lower() in prompt_str:
                self.violations.append(
                    f"Prohibited content detected: '{term}'"
                )
    
    def _check_theme_alignment(self, prompt: Dict):
        """Check if prompt aligns with allowed themes."""
        allowed_themes = self.brand_profile.get("policies", {}).get("allowed_themes", [])
        
        if not allowed_themes:
            return
        
        # Extract style or theme from prompt
        style = prompt.get("style", "").lower()
        scene = prompt.get("scene", "").lower()
        
        # Check if any allowed theme is mentioned
        has_allowed_theme = False
        for theme in allowed_themes:
            if theme.lower() in style or theme.lower() in scene:
                has_allowed_theme = True
                break
        
        if style and not has_allowed_theme:
            self.warnings.append(
                f"Prompt theme may not align with brand preferences. "
                f"Preferred themes: {', '.join(allowed_themes)}"
            )
    
    def _check_color_preferences(self, prompt: Dict):
        """Check color preferences."""
        color_prefs = self.brand_profile.get("policies", {}).get("color_preferences", [])
        
        if not color_prefs:
            return
        
        # Check if colors are mentioned in prompt
        colors = prompt.get("colors", [])
        if isinstance(colors, str):
            colors = [colors]
        
        if colors:
            non_preferred = [c for c in colors if c.lower() not in [p.lower() for p in color_prefs]]
            if non_preferred:
                self.warnings.append(
                    f"Non-preferred colors detected: {', '.join(non_preferred)}. "
                    f"Brand prefers: {', '.join(color_prefs)}"
                )
    
    def _check_quality_requirements(self, prompt: Dict):
        """Check quality requirements."""
        requirements = self.brand_profile.get("requirements", {})
        
        if requirements.get("minimum_quality") == "high":
            quality_keywords = ["high quality", "professional", "detailed", "sharp"]
            prompt_str = json.dumps(prompt).lower()
            
            has_quality = any(kw in prompt_str for kw in quality_keywords)
            if not has_quality:
                self.warnings.append(
                    "Consider adding quality modifiers (e.g., 'high quality', 'professional')"
                )
    
    def get_policy_summary(self) -> Dict:
        """
        Get summary of brand policies.
        
        Returns:
            Dictionary with policy information
        """
        return {
            "brand_name": self.brand_profile.get("brand_name", "Unknown"),
            "policies": self.brand_profile.get("policies", {}),
            "requirements": self.brand_profile.get("requirements", {})
        }
    
    def enhance_prompt(self, prompt: Dict) -> Dict:
        """
        Enhance prompt with brand-aligned modifiers.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Enhanced prompt
        """
        enhanced = prompt.copy()
        
        # Add quality modifiers if needed
        requirements = self.brand_profile.get("requirements", {})
        if requirements.get("minimum_quality") == "high":
            if "modifiers" not in enhanced:
                enhanced["modifiers"] = []
            if "high quality" not in enhanced["modifiers"]:
                enhanced["modifiers"].append("high quality")
            if "professional" not in enhanced["modifiers"]:
                enhanced["modifiers"].append("professional")
        
        # Add style guidelines
        style_guide = self.brand_profile.get("policies", {}).get("style_guidelines", {})
        tone = style_guide.get("tone", "")
        if tone and "style" in enhanced:
            enhanced["style"] = f"{enhanced['style']}, {tone}"
        
        return enhanced
