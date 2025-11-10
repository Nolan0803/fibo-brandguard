# FIBO BrandGuard Usage Guide

This guide walks you through using FIBO BrandGuard for governed AI image generation.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Nolan0803/fibo-brandguard.git
cd fibo-brandguard

# Install dependencies
pip install -r requirements.txt
```

Or use the quick start script:
```bash
./quickstart.sh
```

### 2. Configuration (Optional)

For production use with real Bria FIBO API:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Bria API key
# BRIA_API_KEY=your_actual_api_key
```

### 3. Run the Demo

```bash
python3 demo.py
```

This demonstrates:
- JSON prompt construction
- Policy validation
- Image generation (simulated)
- Audit logging

### 4. Launch the Web App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Using the Web Interface

### Creating Prompts

1. **Navigate to the "Generate Images" tab**

2. **Enter Scene Description**
   - Describe what you want to generate
   - Example: "A modern office workspace with natural lighting"

3. **Select Visual Style**
   - Choose from: photorealistic, artistic, product photography, modern, minimalist

4. **Configure Advanced Options** (optional)
   - **Modifiers**: Add quality descriptors like "high quality", "professional"
   - **Colors**: Specify preferred colors matching brand guidelines
   - **Elements**: List specific objects to include
   - **Mood**: Set the desired atmosphere

5. **Choose Number of Variants**
   - Generate 1-4 different variations

### Policy Validation

The system automatically validates your prompt:

- ✅ **Passed**: Prompt aligns with brand policies
- ⚠️ **Warnings**: Suggestions for improvement
- ❌ **Failed**: Prompt violates policies (won't generate)

### Viewing Results

After validation:
1. Review the structured JSON prompt
2. See policy decisions
3. View generated image metadata
4. Check the audit log

### Audit Log

The "Audit Log" tab shows:
- All generation requests
- Policy decisions
- Violations and warnings
- Approval statistics

## Customizing Brand Policies

Edit `brand_profile.json`:

```json
{
  "brand_name": "Your Brand Name",
  "policies": {
    "allowed_themes": ["professional", "modern"],
    "prohibited_content": ["violence", "inappropriate"],
    "color_preferences": ["blue", "white"],
    "style_guidelines": {
      "tone": "professional and trustworthy"
    }
  },
  "requirements": {
    "minimum_quality": "high",
    "brand_consistency": true,
    "safety_first": true
  }
}
```

## API Integration

### Using the Modules Programmatically

```python
from vlm_agent import VLMAgent
from policy_engine import PolicyEngine
from fibo_client import FIBOClient
from audit_log import AuditLog

# Initialize
vlm = VLMAgent()
policy = PolicyEngine("brand_profile.json")
fibo = FIBOClient()
audit = AuditLog()

# Create prompt
prompt = vlm.create_prompt(
    scene_description="A professional photo",
    style="photorealistic",
    modifiers=["high quality"]
)

# Validate
is_valid, violations, warnings = policy.validate_prompt(prompt)

if is_valid:
    # Generate
    results = fibo.generate_images(prompt, num_variants=4)
    
    # Log
    entry_id = audit.log_generation_request(
        prompt, 
        {"is_valid": is_valid, "violations": violations, "warnings": warnings}
    )
```

## Examples

### Example 1: Product Photography

```python
prompt = vlm.create_prompt(
    scene_description="A sleek laptop on a minimalist desk",
    style="product photography",
    modifiers=["high quality", "professional lighting", "clean background"],
    colors=["silver", "white"],
    elements=["laptop", "desk", "minimal accessories"]
)
```

### Example 2: Office Environment

```python
prompt = vlm.apply_template(
    "product",
    scene="Modern office workspace",
    modifiers=["natural lighting", "professional"],
    colors=["blue", "white", "green"],
    elements=["desk", "chair", "plants", "laptop"]
)
```

### Example 3: Custom Template

```python
from vlm_agent import VLMAgent

vlm = VLMAgent()
prompt = vlm.create_prompt(
    scene_description="Your scene here",
    style="your style",
    modifiers=["modifier1", "modifier2"],
    mood="desired mood"
)
```

## Troubleshooting

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Streamlit Won't Start

```bash
# Check Streamlit installation
streamlit --version

# Try running with explicit path
python3 -m streamlit run app.py
```

### Policy Violations

Check `brand_profile.json` to understand what content is prohibited and what themes are allowed.

### Audit Log Issues

The audit log is stored in `audit_log.json`. If corrupted:
```bash
rm audit_log.json
# The app will create a new one automatically
```

## Best Practices

1. **Start with Templates**: Use built-in templates for consistency
2. **Include Quality Modifiers**: Add "high quality", "professional" for better results
3. **Follow Brand Colors**: Use colors from your brand preferences
4. **Review Warnings**: Address warnings for better brand alignment
5. **Check Audit Log**: Regularly review for compliance tracking

## Advanced Usage

### Batch Processing

```python
prompts = [
    vlm.create_prompt("scene 1", "photorealistic"),
    vlm.create_prompt("scene 2", "artistic"),
    vlm.create_prompt("scene 3", "modern")
]

for prompt in prompts:
    is_valid, _, _ = policy.validate_prompt(prompt)
    if is_valid:
        results = fibo.generate_images(prompt)
```

### Custom Validation

```python
# Add custom validation logic
is_valid, violations, warnings = policy.validate_prompt(prompt)

# Add your own checks
if "custom_requirement" not in prompt.get("modifiers", []):
    warnings.append("Custom requirement missing")
```

## Support

- **Documentation**: See README.md
- **Contributing**: See CONTRIBUTING.md
- **Issues**: Open a GitHub issue
- **Demo**: Run `python3 demo.py`

## Next Steps

- Customize `brand_profile.json` for your brand
- Integrate with real Bria FIBO API
- Build automation workflows
- Export audit logs for compliance
