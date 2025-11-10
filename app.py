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
**Governed JSON-Native Image Generation with Bria FIBO**

This demo showcases JSON-native prompt control, brand policy enforcement, and comprehensive audit logging
for safe and compliant AI image generation.
""")

# Sidebar for brand policy information
with st.sidebar:
    st.header("📋 Brand Policies")
    
    policy_summary = components["policy_engine"].get_policy_summary()
    
    st.subheader(f"Brand: {policy_summary['brand_name']}")
    
    with st.expander("Allowed Themes", expanded=False):
        themes = policy_summary.get("policies", {}).get("allowed_themes", [])
        for theme in themes:
            st.write(f"✓ {theme}")
    
    with st.expander("Prohibited Content", expanded=False):
        prohibited = policy_summary.get("policies", {}).get("prohibited_content", [])
        for item in prohibited:
            st.write(f"✗ {item}")
    
    with st.expander("Color Preferences", expanded=False):
        colors = policy_summary.get("policies", {}).get("color_preferences", [])
        for color in colors:
            st.write(f"🎨 {color}")
    
    st.divider()
    
    # Audit Log Statistics
    st.header("📊 Audit Statistics")
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
    
    # Prompt creation form
    col1, col2 = st.columns([2, 1])
    
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
        
        num_variants = st.slider(
            "Number of Variants",
            min_value=1,
            max_value=4,
            value=4,
            help="Number of image variants to generate"
        )
    
    # Advanced options
    with st.expander("Advanced Options"):
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
    
    # Generate button
    if st.button("🎨 Generate Images", type="primary", use_container_width=True):
        if not scene:
            st.error("Please provide a scene description!")
        else:
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
            
            # Display JSON prompt
            st.subheader("📄 JSON Prompt")
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
            
            # Display validation results
            if is_valid:
                st.success("✅ Prompt passed all policy checks!")
            else:
                st.error("❌ Prompt violates brand policies!")
            
            if violations:
                st.error("**Violations:**")
                for violation in violations:
                    st.write(f"- {violation}")
            
            if warnings:
                st.warning("**Warnings:**")
                for warning in warnings:
                    st.write(f"- {warning}")
            
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
                    st.json(enhanced_prompt)
                    prompt = enhanced_prompt
            
            # Generate images
            st.subheader("🖼️ Generated Images")
            
            with st.spinner("Generating images..."):
                results = components["fibo_client"].generate_images(
                    prompt,
                    num_variants=num_variants
                )
                
                # Log results
                components["audit_log"].log_generation_result(entry_id, results)
                
                # Display images in a grid
                cols = st.columns(min(num_variants, 2))
                for idx, result in enumerate(results):
                    with cols[idx % 2]:
                        st.write(f"**Variant {result['variant_id']}**")
                        
                        # Display placeholder image
                        if result.get("image_url"):
                            # For demo, show metadata instead of actual image
                            st.info(f"Image variant {result['variant_id']} generated successfully!")
                            with st.expander("View Metadata"):
                                st.json(result["metadata"])
                        else:
                            st.warning(f"Image generation in progress...")

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
    
    ### Key Features
    
    - **JSON-Native Prompts**: Structured prompts using JSON for precise control
    - **Policy Enforcement**: Automatic validation against brand guidelines
    - **Audit Logging**: Complete audit trail of all generation requests
    - **Multi-Variant Generation**: Create multiple variations with a single request
    - **Brand Alignment**: Automatic enhancement to align with brand policies
    
    ### Architecture
    
    The application consists of several modules:
    
    - **vlm_agent**: Vision-Language Model agent for prompt construction
    - **policy_engine**: Brand policy enforcement engine
    - **fibo_client**: Client for Bria FIBO API integration
    - **audit_log**: Comprehensive audit logging system
    - **brand_profile.json**: Brand guidelines and policies
    
    ### Technologies Used
    
    - Streamlit for the web interface
    - Bria FIBO for image generation
    - Python for backend logic
    - JSON for structured data
    
    ### Getting Started
    
    1. Install dependencies: `pip install -r requirements.txt`
    2. Set your Bria API key: `export BRIA_API_KEY=your_key_here`
    3. Run the app: `streamlit run app.py`
    
    ### About Bria FIBO
    
    Bria FIBO is a next-generation image generation model that supports JSON-native prompts,
    providing fine-grained control over image generation with enterprise-grade compliance.
    """)
    
    st.divider()
    
    st.markdown("""
    ### Developer Information
    
    **Built for**: Bria FIBO Hackathon  
    **Version**: 1.0.0  
    **License**: MIT
    """)

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
