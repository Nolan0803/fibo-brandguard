# 🛡️ FIBO BrandGuard

**Governed, JSON-native Bria FIBO image generation demo for the Bria Hackathon**

FIBO BrandGuard is an enterprise-grade demonstration application that showcases how to implement governed AI image generation with Bria FIBO. It features JSON-native prompt control, automated brand policy enforcement, and comprehensive audit logging.

## ✨ Features

- **JSON-Native Prompts**: Structured prompts using JSON for precise, programmatic control
- **Policy Enforcement**: Automatic validation against brand guidelines and policies
- **Audit Logging**: Complete audit trail of all generation requests and policy decisions
- **Multi-Variant Generation**: Create up to 4 image variations with a single request
- **Brand Alignment**: Automatic prompt enhancement to align with brand policies
- **Interactive UI**: User-friendly Streamlit interface for easy interaction

## 🏗️ Architecture

The application consists of several modular components:

- **vlm_agent.py**: Vision-Language Model agent for constructing JSON-native prompts
- **policy_engine.py**: Brand policy enforcement engine that validates prompts
- **fibo_client.py**: Client for interacting with the Bria FIBO API
- **audit_log.py**: Comprehensive audit logging system
- **app.py**: Main Streamlit application
- **brand_profile.json**: Brand guidelines and policy configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Bria API key for production use

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Nolan0803/fibo-brandguard.git
cd fibo-brandguard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set your Bria API key:
```bash
export BRIA_API_KEY=your_api_key_here
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. Create a Prompt

- Enter a scene description (e.g., "A modern office workspace with natural lighting")
- Choose a visual style (photorealistic, artistic, product photography, etc.)
- Optionally use advanced options to add modifiers, colors, elements, and mood

### 2. Policy Validation

The system automatically validates your prompt against brand policies:
- ✅ **Approved**: Prompt aligns with all brand guidelines
- ⚠️ **Warnings**: Suggestions for better brand alignment
- ❌ **Rejected**: Prompt violates brand policies

### 3. Generate Images

- Click "Generate Images" to create up to 4 variants
- View the JSON prompt structure
- See policy validation results
- Review generated image metadata

### 4. Audit Log

- View all generation requests in the Audit Log tab
- See approval rates and policy violation statistics
- Track complete history of all operations

## 🔧 Configuration

### Brand Profile

Edit `brand_profile.json` to customize brand policies:

```json
{
  "brand_name": "Your Brand",
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

## 📦 Modules

### VLM Agent (`vlm_agent.py`)

Handles JSON prompt construction and template management:
- Create structured prompts
- Apply templates (basic, product, creative)
- Validate prompt structure
- Extract keywords for analysis

### Policy Engine (`policy_engine.py`)

Enforces brand policies on prompts:
- Validate against prohibited content
- Check theme alignment
- Verify color preferences
- Ensure quality requirements
- Enhance prompts for brand alignment

### FIBO Client (`fibo_client.py`)

Manages interaction with Bria FIBO API:
- Generate multiple image variants
- Handle API authentication
- Simulate image generation for demo purposes

### Audit Log (`audit_log.py`)

Tracks all operations:
- Log generation requests
- Record policy decisions
- Track violations
- Generate statistics
- Maintain complete audit trail

## 🎯 Use Cases

- **Brand Compliance**: Ensure all generated images align with brand guidelines
- **Content Governance**: Enforce policies on AI-generated content
- **Audit Trail**: Maintain complete records for compliance and review
- **Quality Control**: Automatically enhance prompts for better results
- **Multi-Variant Testing**: Generate multiple variations for A/B testing

## 🛠️ Development

### Project Structure

```
fibo-brandguard/
├── app.py                  # Main Streamlit application
├── vlm_agent.py           # VLM agent module
├── policy_engine.py       # Policy enforcement module
├── fibo_client.py         # FIBO API client
├── audit_log.py           # Audit logging module
├── brand_profile.json     # Brand policy configuration
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Running Tests

The application includes basic validation in each module. To test:

```bash
python -c "from vlm_agent import VLMAgent; print('VLM Agent OK')"
python -c "from policy_engine import PolicyEngine; print('Policy Engine OK')"
python -c "from fibo_client import FIBOClient; print('FIBO Client OK')"
python -c "from audit_log import AuditLog; print('Audit Log OK')"
```

## 📝 License

MIT License - See LICENSE file for details

## 🏆 Hackathon

Built for the **Bria FIBO Hackathon** to demonstrate enterprise-grade governance for AI image generation.

## 🤝 Contributing

This is a hackathon demo project. Feel free to fork and extend!

## 📧 Contact

For questions or feedback about this demo, please open an issue on GitHub.

---

**FIBO BrandGuard** - Governed AI Image Generation | Built with ❤️ for Bria FIBO Hackathon
