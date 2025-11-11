# FIBO BrandGuard 🛡️✨

**A professional AI-powered tool that detects, refines, and regenerates brand-consistent imagery using Bria FIBO's JSON-native controllability.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://localhost:8501)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Bria FIBO](https://img.shields.io/badge/Bria-FIBO%201.2-blue.svg)](https://huggingface.co/briaai/FIBO)

## 🚀 Overview

FIBO BrandGuard helps marketers, designers, and enterprises maintain consistent visual identity by automatically analyzing uploaded content, flagging deviations from brand tone, and regenerating compliant versions using Bria's FIBO API.

### 🎯 Problem Solved
- **Brand Inconsistency**: Marketing teams struggle with off-brand visual content
- **Manual Review Overhead**: Time-consuming manual brand compliance checks  
- **Regeneration Complexity**: Difficult to specify exact brand requirements for AI models
- **Scale Challenges**: Maintaining consistency across hundreds of images

### 💡 Solution
FIBO BrandGuard leverages **JSON-native structured prompts** to automatically generate brand-compliant imagery with precise control over style, composition, and visual elements.

## ✨ Features

- 🎨 **Image Refinement**: Detects brand inconsistencies and regenerates visuals with creative variants
- ⚙️ **JSON-Native Workflow**: Uses FIBO structured prompts for automated controllability
- 🧠 **AI Compliance Check**: Evaluates imagery against predefined color palettes, lighting, and tone
- 🔄 **Creative Variants**: Automatically generates diverse interpretations with unique seeds and lighting variations
- 📊 **Complete Audit Trail**: Every decision and generation logged for compliance
- 💼 **Enterprise-Ready Interface**: Built with Streamlit for ease of integration
- 🌐 **Remote Inference**: Uses HuggingFace API - no local GPU required

## 🧰 Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Bria FIBO + Hugging Face API  
- **AI Model:** Bria FIBO 1.2 (via HF API)
- **Image Processing:** PIL, base64 encoding
- **Environment:** python-dotenv for secure configuration
- **Deployment:** Local/Cloud (Streamlit)

## 🏆 Hackathon Category

**Best JSON-Native or Agentic Workflow**  
(Shows how structured JSON controllability enables consistent, scalable brand generation)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- HuggingFace Account with API access
- Bria FIBO API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nolan0803/fibo-brandguard.git
   cd fibo-brandguard
   ```

2. **Create virtual environment** 
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:  
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   Create a `.env` file in the project root:
   ```env
   HF_TOKEN=your_huggingface_token_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

**Important**: 
- Get your token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Accept the Bria FIBO license at [huggingface.co/briaai/FIBO](https://huggingface.co/briaai/FIBO)
- Never commit your token to version control

## � Usage

### Basic Workflow

1. **Define Scene**: Enter your creative brief or scene description
2. **Configure Generation**: Set number of variants (1-4) and creativity level
3. **Brand Governance**: System automatically applies JSON-structured prompts
4. **Generate Images**: Creates unique variants with different seeds and creative prompts
5. **Review Results**: View generated images with metadata and audit trails

### Advanced Features

#### Creative Variants
The system automatically generates diverse variants through:
- **Unique Seeds**: Each variant uses random seeds (e.g., 1003702, 4043772) 
- **Lighting Variations**: Golden hour, dramatic, soft natural, cinematic
- **Angle Diversity**: Wide-angle, close-up, bird's eye view, macro
- **Mood Modifiers**: Vibrant, serene, dynamic, ethereal

#### JSON Prompt Structure
```json
{
  "scene": "A modern office environment",
  "style": "professional, clean, minimalist",
  "lighting": "natural daylight, soft shadows",
  "color_palette": "blue, white, gray tones", 
  "composition": "wide angle, balanced framing",
  "mood": "confident, innovative, trustworthy"
}
```

### Example Generations
- **Marketing Campaign**: "Modern tech workspace" → Multiple variants with different lighting and angles
- **Product Photography**: "Premium laptop setup" → Consistent brand style with creative diversity
- **Corporate Imagery**: "Team collaboration" → Professional variants maintaining brand guidelines

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  Policy Engine  │    │  FIBO Client    │
│                 │────│                 │────│                 │
│ • Input Forms   │    │ • Brand Rules   │    │ • HF API Calls  │
│ • Image Display │    │ • JSON Schema   │    │ • Variant Gen   │
│ • Audit Logs    │    │ • Compliance    │    │ • Error Handle  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Audit System  │
                    │                 │
                    │ • Event Logging │
                    │ • Metadata      │
                    │ • Compliance    │
                    └─────────────────┘
```

### Project Structure
```
fibo-brandguard/
├── app.py              # Main Streamlit application
├── fibo_client.py      # Remote FIBO API client with variant generation
├── policy_engine.py    # Brand governance and compliance
├── vlm_agent.py        # Vision-Language Model agent  
├── audit_log.py        # Audit logging system
├── brand_profile.json  # Brand policy configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md         # This file
└── demos/            # Demo scripts and examples
```

### Core Components

- **VLM Agent**: Constructs structured JSON prompts from user input
- **Policy Engine**: Validates prompts against configurable brand policies
- **FIBO Client**: Manages remote Bria FIBO API calls with creative variant generation
- **Audit Log**: Maintains complete audit trail for compliance

## ⚙️ Configuration

### Brand Policies (`brand_profile.json`)

Customize brand enforcement:

```json
{
  "brand_name": "Your Brand",
  "policies": {
    "allowed_themes": ["professional", "modern", "clean"],
    "prohibited_content": ["violence", "inappropriate"],
    "color_preferences": ["blue", "white", "gray"],
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

### Environment Variables

```bash
# Required
HF_TOKEN=your_huggingface_token_here

# Optional
STREAMLIT_THEME_BASE=dark
STREAMLIT_THEME_PRIMARY_COLOR=#1E88E5
```

## 📽️ Demo Video

[🎥 Watch on YouTube](<your-public-video-link>)

*Showcasing JSON-native workflow, brand governance, creative variant generation, and enterprise-ready features*

## 🎯 Use Cases

- **Enterprise Compliance**: Ensure all generated visuals meet brand guidelines
- **Marketing Campaign Generation**: Create consistent brand visuals with creative diversity
- **Content Governance**: Enforce policies on AI-generated marketing materials  
- **Quality Assurance**: Automatically enhance prompts for brand alignment
- **Multi-variant Testing**: Generate consistent variations for A/B testing
- **Creative Exploration**: Discover new visual directions while maintaining brand consistency

## 🏆 Hackathon Highlights

Built specifically for the **Bria FIBO Hackathon**, this demo showcases:

1. **Innovation**: JSON-native governance for enterprise AI image generation
2. **Technical Excellence**: Clean, modular architecture with comprehensive error handling
3. **User Experience**: Intuitive interface with clear policy feedback and audit trails  
4. **Enterprise Ready**: Production-quality governance, logging, and compliance features
5. **Bria FIBO Integration**: Full utilization of FIBO's JSON-native capabilities

## � Technical Details

### Dependencies
- `streamlit` - Web interface framework
- `huggingface_hub` - Remote FIBO API access
- `python-dotenv` - Environment variable management
- `pillow` - Image processing and display

### Performance
- **Remote Generation**: 2-5 seconds per image
- **Safe Mode Fallback**: Instant placeholder generation
- **Memory Usage**: ~200MB (no local model weights)
- **Network**: Requires stable internet for remote inference

## 📝 Development

### Running Tests
```bash
# Basic validation
python -c "import fibo_client; print('FIBO Client OK')"
python -c "import policy_engine; print('Policy Engine OK')"
python -c "import audit_log; print('Audit Log OK')"
```

### Code Quality
- Type hints throughout
- Comprehensive error handling
- Modular, testable architecture
- Clear separation of concerns

## 🤝 Contributing

This is a hackathon demonstration project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## � License

MIT License - See LICENSE file for details

## 🏆 Acknowledgments

Built for the **Bria FIBO Hackathon** to demonstrate the future of governed AI image generation.

## 📞 Contact

- **Developer**: Nolan  
- **Project**: FIBO BrandGuard
- **Hackathon**: Bria FIBO Hackathon 2025
- **Repository**: [GitHub](https://github.com/Nolan0803/fibo-brandguard)

---

*Built with ❤️ for the Bria FIBO Hackathon - Demonstrating the power of JSON-native AI workflows for enterprise brand governance*
