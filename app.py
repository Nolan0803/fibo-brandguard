"""
FIBO BrandGuard - Streamlit Application
A governed, JSON-native Bria FIBO image generation demo for the Bria Hackathon.
"""

import streamlit as st
import json
from datetime import datetime
from vlm_agent import VLMAgent
from policy_engine import PolicyEngine
from fibo_client import FIBOClient
from audit_log import AuditLog


# Page configuration
st.set_page_config(
    page_title="FIBO BrandGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all application components."""
    return {
        "vlm_agent": VLMAgent(),
        "policy_engine": PolicyEngine("brand_profile.json"),
        "fibo_client": FIBOClient(),
        "audit_log": AuditLog("audit_log.json")
    }

components = initialize_components()

# App header
st.title("🛡️ FIBO BrandGuard")
st.markdown("""
**Governed JSON-native image generation with Bria FIBO for brand-safe, auditable visuals.**
""")

# Check remote FIBO availability
try:
    from fibo_client import is_pipeline_loaded
    is_remote_available = is_pipeline_loaded()
except Exception as e:
    st.error("⚠️ Error checking FIBO client status")
    is_remote_available = False

# Status banner
if is_remote_available:
    st.success("🌐 Remote FIBO generation active: governed images generated via official API.")
else:
    st.warning("🛡️ FIBO Safe Mode: remote generation unavailable, using placeholder preview only.")

# Sidebar for brand policy information
with st.sidebar:
    st.header("📋 Brand Policies")
    
    policy_summary = components["policy_engine"].get_policy_summary()
    
    st.subheader(f"**Brand:** {policy_summary['brand_name']}")
    
    with st.expander("✅ Allowed Themes", expanded=False):
        themes = policy_summary.get("policies", {}).get("allowed_themes", [])
        for theme in themes:
            st.write(f"• {theme}")
    
    with st.expander("❌ Prohibited Content", expanded=False):
        prohibited = policy_summary.get("policies", {}).get("prohibited_content", [])
        for item in prohibited:
            st.write(f"• {item}")
    
    with st.expander("🎨 Color Preferences", expanded=False):
        colors = policy_summary.get("policies", {}).get("color_preferences", [])
        for color in colors:
            st.write(f"• {color}")
    
    st.divider()
    
    # Audit Log Statistics
    st.subheader("📊 Audit Statistics")
    stats = components["audit_log"].get_statistics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Requests", stats["generation_requests"])
        st.metric("Approved", stats["approved_requests"])
    with col2:
        st.metric("Violations", stats["policy_violations"])
        approval_rate = stats.get("approval_rate", 0)
        st.metric("Approval Rate", f"{approval_rate:.1f}%")

# Main content area
tab1, tab2, tab3 = st.tabs(["🎨 Generate Images", "📜 Audit Log", "ℹ️ About"])

with tab1:
    st.header("Create Your Prompt")
    
    # Create prompt form in a card-like container
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            scene = st.text_area(
                "Scene Description",
                placeholder="e.g., A modern office workspace with natural lighting",
                height=100,
                help="Describe the scene you want to generate"
            )
            
            style = st.selectbox(
                "Visual Style",
                options=["photorealistic", "artistic", "product photography", "modern", "minimalist"],
                help="Choose the visual style for the image"
            )
        
        with col2:
            template = st.selectbox(
                "Template",
                options=["basic", "product", "creative"],
                help="Use a pre-defined template"
            )
            
            # Fixed slider with proper range
            num_variants = st.slider(
                "Number of Variants",
                min_value=1,
                max_value=4,
                value=2,
                step=1,
                help="Number of image variants to generate"
            )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                modifiers_input = st.text_input(
                    "Modifiers (comma-separated)",
                    placeholder="e.g., high quality, professional",
                    help="Add quality and style modifiers"
                )
                
                colors_input = st.text_input(
                    "Colors (comma-separated)",
                    placeholder="e.g., blue, white",
                    help="Specify preferred colors"
                )
            
            with col2:
                elements_input = st.text_input(
                    "Elements (comma-separated)",
                    placeholder="e.g., laptop, plants",
                    help="Specific elements to include"
                )
                
                mood = st.text_input(
                    "Mood",
                    placeholder="e.g., professional, calm",
                    help="Desired mood or atmosphere"
                )
        
        # Generate button - centered and prominent
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_clicked = st.button("🎨 Generate Images", type="primary", use_container_width=True)
    
    # Only process if button clicked and scene is provided
    if generate_clicked:
        if not scene:
            st.error("❌ Please provide a scene description!")
        else:
            try:
                # Parse advanced options
                modifiers = [m.strip() for m in modifiers_input.split(",") if m.strip()] if modifiers_input else None
                colors = [c.strip() for c in colors_input.split(",") if c.strip()] if colors_input else None
                elements = [e.strip() for e in elements_input.split(",") if e.strip()] if elements_input else None
                
                # Create prompt
                if template != "basic":
                    prompt = components["vlm_agent"].apply_template(
                        template,
                        scene,
                        style=style,
                        modifiers=modifiers,
                        colors=colors,
                        elements=elements,
                        mood=mood
                    )
                else:
                    prompt = components["vlm_agent"].create_prompt(
                        scene,
                        style=style,
                        modifiers=modifiers,
                        colors=colors,
                        elements=elements,
                        mood=mood
                    )
                
                # Display JSON prompt in collapsible section
                with st.expander("📄 View JSON Prompt", expanded=False):
                    st.json(prompt)
                
                # Validate against policies
                st.subheader("🔍 Policy Validation")
                is_valid, violations, warnings = components["policy_engine"].validate_prompt(prompt)
                
                policy_decision = {
                    "is_valid": is_valid,
                    "violations": violations,
                    "warnings": warnings,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Display validation results with proper styling
                if is_valid and not warnings:
                    st.success("✅ Prompt passed all policy checks!")
                elif is_valid and warnings:
                    st.warning("⚠️ Prompt approved with recommendations")
                    for warning in warnings:
                        st.write(f"• {warning}")
                else:
                    st.error("❌ Prompt violates brand policies!")
                    for violation in violations:
                        st.write(f"• {violation}")
                
                # Log the request
                entry_id = components["audit_log"].log_generation_request(
                    prompt,
                    policy_decision,
                    user="streamlit_user"
                )
                
                if not is_valid:
                    components["audit_log"].log_policy_violation(
                        prompt,
                        violations,
                        user="streamlit_user"
                    )
                    st.stop()
                
                # Enhance prompt if needed
                if warnings:
                    enhanced_prompt = components["policy_engine"].enhance_prompt(prompt)
                    if enhanced_prompt != prompt:
                        st.info("**Enhanced Prompt with Brand Alignment:**")
                        with st.expander("View Enhanced Prompt", expanded=False):
                            st.json(enhanced_prompt)
                        prompt = enhanced_prompt
                
                # Generate images with error handling
                st.subheader("🖼️ Generated Images")
                
                try:
                    with st.spinner("Generating images..."):
                        results = components["fibo_client"].generate_images(
                            prompt,
                            num_variants=num_variants
                        )
                        
                        # Log results
                        components["audit_log"].log_generation_result(entry_id, results)
                        
                        if not results:
                            st.warning("⚠️ Remote FIBO generation is temporarily unavailable. Your prompt and audit log are still recorded.")
                        else:
                            # Display images in grid format
                            cols = st.columns(min(len(results), 2))  # Max 2 columns
                            for idx, result in enumerate(results):
                                with cols[idx % 2]:
                                    st.write(f"**Variant {result['variant_id']}**")
                                    
                                    # Display image
                                    if "image" in result and result["image"]:
                                        st.image(
                                            result["image"], 
                                            caption=f"Variant {result['variant_id']}"
                                        )
                                    
                                    # Status indicator
                                    if result.get("status") == "success":
                                        st.success(f"✅ Generated successfully")
                                    elif result.get("status") == "safe_mode":
                                        st.info("🛡️ Safe mode preview")
                                    else:
                                        st.warning("⚠️ Placeholder mode")
                                    
                                    # Show metadata in expander
                                    with st.expander(f"📊 View Details - Variant {result['variant_id']}"):
                                        metadata = result.get("metadata", {})
                                        details = {
                                            "Model": metadata.get("model", "Unknown"),
                                            "Provider": metadata.get("provider", "Unknown"),
                                            "Generation Time": f"{result.get('generation_time', 0):.1f}s",
                                            "Size": metadata.get("size", "Unknown"),
                                            "Seed": metadata.get("seed", "Unknown"),
                                            "Final Prompt": result.get("prompt_string", "")[:200] + "..." if len(result.get("prompt_string", "")) > 200 else result.get("prompt_string", "")
                                        }
                                        for key, value in details.items():
                                            st.write(f"**{key}:** {value}")
                
                except Exception as e:
                    st.error("⚠️ Remote FIBO generation is temporarily unavailable. Your prompt and audit log are still recorded.")
                    st.write("Technical details logged to console.")
                    print(f"Generation error: {e}")
            
            except Exception as e:
                st.error("⚠️ An error occurred during processing. Please try again.")
                st.write("Technical details logged to console.")
                print(f"Processing error: {e}")

with tab2:
    st.header("📜 Audit Log")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🗑️ Clear Log", type="secondary"):
            components["audit_log"].clear_log()
            st.success("Audit log cleared!")
            st.rerun()
        
        limit = st.number_input("Show last N entries", min_value=5, max_value=50, value=10)
    
    # Display recent entries
    entries = components["audit_log"].get_recent_entries(limit)
    
    if entries:
        for entry in reversed(entries):
            with st.expander(
                f"{entry.get('type', 'unknown').replace('_', ' ').title()} - {entry.get('timestamp', 'N/A')}"
            ):
                st.json(entry)
    else:
        st.info("No audit log entries yet. Generate some images to see the audit trail!")

with tab3:
    st.header("ℹ️ About FIBO BrandGuard")
    
    st.markdown("""
    ### What is FIBO BrandGuard?
    
    FIBO BrandGuard is a demonstration application built for the **Bria FIBO Hackathon** that showcases
    enterprise-grade governance for AI image generation.
    
    ### 🔑 Key Innovation Points
    
    • **Uses Bria FIBO JSON-native prompting** for precise, reproducible control over image generation
    • **Enforces configurable brand and safety policies** before generation to ensure compliance
    • **Logs every request** with input JSON, policy verdicts, and generation metadata for complete auditability
    • **Supports remote FIBO inference** so it runs reliably even without local GPU hardware
    
    ### ⭐ What Makes This Different
    
    Unlike generic image generators, FIBO BrandGuard provides:
    
    - **Governance First**: Every prompt is validated against brand policies before generation
    - **JSON-Native Control**: Structured prompts enable programmatic, consistent control
    - **Complete Audit Trail**: Every decision and generation is logged for compliance
    - **Enterprise Ready**: Designed for regulated environments requiring oversight
    
    ### 🏗️ Architecture
    
    The application consists of modular components:
    
    - **vlm_agent**: Vision-Language Model agent for prompt construction
    - **policy_engine**: Brand policy enforcement engine
    - **fibo_client**: Remote client for Bria FIBO API integration
    - **audit_log**: Comprehensive audit logging system
    - **brand_profile.json**: Brand guidelines and policies
    
    ### 🔧 Technologies Used
    
    - **Frontend**: Streamlit for the web interface
    - **Image Generation**: Bria FIBO via HuggingFace Inference API
    - **Backend Logic**: Python for policy enforcement and audit logging
    - **Data Format**: JSON for structured, governable prompts
    
    ### 🚀 Getting Started
    
    1. Set your HuggingFace token in `.env`:
       ```
       HF_TOKEN=your_token_here
       ```
    2. Install dependencies: `pip install -r requirements.txt`
    3. Run the app: `streamlit run app.py`
    4. Accept Bria FIBO license at [huggingface.co/briaai/FIBO](https://huggingface.co/briaai/FIBO)
    
    ### 🎯 Use Cases
    
    - **Brand Compliance**: Ensure generated content aligns with brand guidelines
    - **Content Governance**: Enforce policies on AI-generated visuals
    - **Audit Requirements**: Maintain complete records for regulatory compliance
    - **Quality Control**: Automatically enhance prompts for brand alignment
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏆 Built for Bria FIBO Hackathon
        
        This demo showcases how to build production-ready,
        governed AI image generation systems using Bria's
        cutting-edge FIBO model.
        """)
    
    with col2:
        st.markdown("""
        ### 📧 Developer Information
        
        **Version**: 2.0.0  
        **License**: MIT  
        **Repository**: [GitHub](https://github.com/Nolan0803/fibo-brandguard)
        """)
    
    # System status section
    st.subheader("🔧 System Status")
    
    try:
        setup_info = components["fibo_client"].validate_setup()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if setup_info.get("has_hf_token"):
                st.success("✅ HF Token")
            else:
                st.error("❌ HF Token")
        
        with col2:
            if setup_info.get("client_available"):
                st.success("✅ Remote Client")
            else:
                st.warning("⚠️ Remote Client")
        
        with col3:
            if setup_info.get("mode") == "remote-inference":
                st.success("✅ Remote Mode")
            else:
                st.warning("⚠️ Safe Mode")
        
        with st.expander("View Detailed System Information"):
            st.json(setup_info)
    
    except Exception as e:
        st.error("⚠️ Unable to check system status")
        st.write("Technical details logged to console.")
        print(f"Status check error: {e}")

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        FIBO BrandGuard - Governed AI Image Generation | Built with ❤️ for Bria FIBO Hackathon
    </div>
    """,
    unsafe_allow_html=True
)
