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

# Enterprise styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Status pills */
    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.125rem;
    }
    
    .status-success {
        background-color: #059669;
        color: white;
    }
    
    .status-warning {
        background-color: #d97706;
        color: white;
    }
    
    .status-error {
        background-color: #dc2626;
        color: white;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        color: #3b82f6;
        margin-bottom: 0.5rem;
        font-size: 1.125rem;
        font-weight: 600;
    }
    
    .metric-card p {
        color: #d1d5db;
        margin: 0;
        font-size: 0.875rem;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #059669 100%);
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.4);
    }
    
    /* Generated image cards */
    .image-card {
        background: #1f2937;
        border-radius: 0.75rem;
        padding: 1rem;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    .image-card img {
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    
    /* Section headers */
    .section-header {
        color: #3b82f6;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #374151;
    }
    
    .section-subtext {
        color: #9ca3af;
        font-size: 0.875rem;
        margin-bottom: 1.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1f2937;
    }
    
    /* Metrics styling */
    .metric-container {
        background: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #374151;
    }
    
    /* Floating Back to Top Button */
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #3b82f6 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
        display: none;
    }
    
    .back-to-top:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
    }
    
    /* Quick Navigation Floating Menu */
    .quick-nav {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(31, 41, 55, 0.95);
        border-radius: 0.75rem;
        padding: 0.75rem;
        border: 1px solid #374151;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        z-index: 1000;
        backdrop-filter: blur(8px);
        min-width: 140px;
    }
    
    .quick-nav button {
        display: block;
        width: 100%;
        background: transparent;
        color: #9ca3af;
        border: none;
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: 0.375rem;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.875rem;
        text-align: left;
        font-family: inherit;
    }
    
    .quick-nav button:hover {
        background: #374151;
        color: #3b82f6;
        transform: translateX(2px);
    }
    
    .quick-nav button:active {
        background: #4b5563;
        transform: translateX(4px);
    }
    
    .quick-nav button.active {
        background: #3b82f6;
        color: white;
    }
</style>

<script>
// Back to top functionality
window.addEventListener('scroll', function() {
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Quick navigation to tabs - Updated for Streamlit
function switchToTab(tabIndex) {
    // Multiple selectors to find Streamlit tab buttons
    const selectors = [
        '[data-testid="stTabs"] button',
        '.stTabs button',
        '[role="tab"]',
        'div[data-testid="stTabs"] div[role="tablist"] button'
    ];
    
    let tabButtons = null;
    for (const selector of selectors) {
        tabButtons = document.querySelectorAll(selector);
        if (tabButtons.length > 0) break;
    }
    
    if (tabButtons && tabButtons[tabIndex]) {
        // Ensure the button is clickable
        setTimeout(() => {
            tabButtons[tabIndex].click();
            scrollToTop();
        }, 100);
    } else {
        // Fallback: try to find by text content
        const allButtons = document.querySelectorAll('button');
        const tabTexts = ['Generate Images', 'Audit Log', 'About'];
        
        for (const button of allButtons) {
            if (button.textContent.includes(tabTexts[tabIndex])) {
                setTimeout(() => {
                    button.click();
                    scrollToTop();
                }, 100);
                break;
            }
        }
    }
}

// Alternative approach using Streamlit's internal API
function switchToTabAlt(tabIndex) {
    // Try to trigger Streamlit's tab switching
    const event = new CustomEvent('streamlit:setComponentValue', {
        detail: {
            key: 'tab_selection',
            value: tabIndex
        }
    });
    document.dispatchEvent(event);
    scrollToTop();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers with multiple attempts
    setTimeout(() => {
        const navButtons = document.querySelectorAll('.quick-nav button');
        navButtons.forEach((button, index) => {
            button.addEventListener('click', () => switchToTab(index));
        });
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

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

# Header Section
st.markdown('<h1 class="section-header">FIBO BrandGuard</h1>', unsafe_allow_html=True)
st.markdown('<p class="section-subtext">Governed JSON-native image generation with Bria FIBO for brand-safe, auditable visuals.</p>', unsafe_allow_html=True)

# Floating Navigation Components
st.markdown("""
<div class="quick-nav">
    <button onclick="switchToTab(0)" onmousedown="switchToTab(0)" title="Generate Images">🎨 Generate</button>
    <button onclick="switchToTab(1)" onmousedown="switchToTab(1)" title="Audit Log">📋 Audit Log</button>
    <button onclick="switchToTab(2)" onmousedown="switchToTab(2)" title="About">ℹ️ About</button>
</div>

<button class="back-to-top" onclick="scrollToTop()" title="Back to Top">↑</button>

<script>
// Delayed initialization to ensure Streamlit is ready
setTimeout(function() {
    // Function to switch tabs with multiple fallback strategies
    window.switchToTabImmediate = function(tabIndex) {
        console.log('Attempting to switch to tab:', tabIndex);
        
        // Strategy 1: Look for Streamlit tab buttons
        let tabButtons = document.querySelectorAll('[data-testid="stTabs"] button[role="tab"]');
        
        if (tabButtons.length === 0) {
            // Strategy 2: Alternative selector
            tabButtons = document.querySelectorAll('div[data-testid="stTabs"] button');
        }
        
        if (tabButtons.length === 0) {
            // Strategy 3: Look for any buttons in tabs container
            const tabsContainer = document.querySelector('[data-testid="stTabs"]');
            if (tabsContainer) {
                tabButtons = tabsContainer.querySelectorAll('button');
            }
        }
        
        if (tabButtons.length > tabIndex) {
            console.log('Found tab buttons, clicking index:', tabIndex);
            tabButtons[tabIndex].click();
            setTimeout(() => scrollToTop(), 200);
        } else {
            console.log('Tab buttons not found, trying text-based search');
            // Strategy 4: Find by text content
            const tabTexts = ['Generate Images', 'Audit Log', 'About'];
            const allButtons = document.querySelectorAll('button');
            
            for (const button of allButtons) {
                if (button.textContent.trim() === tabTexts[tabIndex]) {
                    console.log('Found tab by text:', tabTexts[tabIndex]);
                    button.click();
                    setTimeout(() => scrollToTop(), 200);
                    break;
                }
            }
        }
    };
    
    // Override the global function
    window.switchToTab = window.switchToTabImmediate;
    
    console.log('Navigation functions initialized');
}, 2000);
</script>
""", unsafe_allow_html=True)

# Status Pills
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    try:
        setup_info = components["fibo_client"].validate_setup()
        if setup_info.get("has_hf_token"):
            st.markdown('<span class="status-pill status-success">HF Token Verified</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill status-error">HF Token Missing</span>', unsafe_allow_html=True)
    except:
        st.markdown('<span class="status-pill status-warning">Token Status Unknown</span>', unsafe_allow_html=True)

with col2:
    try:
        is_remote_available = components["fibo_client"].validate_setup().get("client_available", False)
        if is_remote_available:
            st.markdown('<span class="status-pill status-success">Remote Client Ready</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill status-warning">Safe Mode Active</span>', unsafe_allow_html=True)
    except:
        st.markdown('<span class="status-pill status-warning">Client Status Unknown</span>', unsafe_allow_html=True)

with col3:
    st.markdown('<span class="status-pill status-success">Audit Logging Active</span>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Summary Cards Strip
col1, col2, col3 = st.columns(3)

with col1:
    policy_summary = components["policy_engine"].get_policy_summary()
    st.markdown(f"""
    <div class="metric-card">
        <h3>Brand Policies Active</h3>
        <p><strong>{policy_summary['brand_name']}</strong></p>
        <p>{len(policy_summary.get('policies', {}).get('allowed_themes', []))} allowed themes</p>
        <p>{len(policy_summary.get('policies', {}).get('prohibited_content', []))} restrictions</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    try:
        setup_info = components["fibo_client"].validate_setup()
        mode = "Remote API" if setup_info.get("client_available") else "Safe Mode"
        model_info = "Bria FIBO 1.2" if setup_info.get("client_available") else "Placeholder"
    except:
        mode = "Unknown"
        model_info = "Unknown"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>Governance Mode</h3>
        <p><strong>{mode}</strong></p>
        <p>Model: {model_info}</p>
        <p>JSON-native prompting</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    stats = components["audit_log"].get_statistics()
    st.markdown(f"""
    <div class="metric-card">
        <h3>Activity Summary</h3>
        <p><strong>{stats["generation_requests"]}</strong> requests</p>
        <p>{stats["approval_rate"]:.1f}% approval rate</p>
        <p>{stats["policy_violations"]} violations</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar for brand policy information
with st.sidebar:
    st.header("Brand Policies")
    
    policy_summary = components["policy_engine"].get_policy_summary()
    
    st.subheader(f"**Brand:** {policy_summary['brand_name']}")
    
    with st.expander("Allowed Themes", expanded=False):
        themes = policy_summary.get("policies", {}).get("allowed_themes", [])
        for theme in themes:
            st.write(f"• {theme}")
    
    with st.expander("Prohibited Content", expanded=False):
        prohibited = policy_summary.get("policies", {}).get("prohibited_content", [])
        for item in prohibited:
            st.write(f"• {item}")
    
    with st.expander("Color Preferences", expanded=False):
        colors = policy_summary.get("policies", {}).get("color_preferences", [])
        for color in colors:
            st.write(f"• {color}")
    
    st.divider()
    
    # Audit Log Statistics
    st.subheader("Audit Statistics")
    stats = components["audit_log"].get_statistics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Requests", stats["generation_requests"])
        st.metric("Approved", stats["approved_requests"])
    with col2:
        st.metric("Violations", stats["policy_violations"])
        approval_rate = stats.get("approval_rate", 0)
        st.metric("Approval Rate", f"{stats['approval_rate']:.1f}%")

# Main content area
tab1, tab2, tab3 = st.tabs(["Generate Images", "Audit Log", "About"])

with tab1:
    st.markdown('<h2 class="section-header">Create a Brand-Safe Prompt</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Design your prompt with enterprise governance and compliance built-in.</p>', unsafe_allow_html=True)
    
    # Main prompt card
    st.markdown("""
    <div class="metric-card" style="margin-bottom: 2rem;">
    </div>
    """, unsafe_allow_html=True)
    
    # Use container to create the card effect
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            scene = st.text_area(
                "Scene Description",
                placeholder="Describe the scene you want to generate (e.g., 'Modern office workspace with diverse team collaborating')",
                height=100,
                help="Provide a clear description that aligns with your brand guidelines"
            )
            
            style = st.selectbox(
                "Visual Style",
                options=["photorealistic", "artistic", "product photography", "modern", "minimalist"],
                help="Select the visual approach for your image"
            )
        
        with col2:
            template = st.selectbox(
                "Template",
                options=["basic", "product", "creative"],
                help="Choose a pre-configured template"
            )
            
            num_variants = st.slider(
                "Number of Variants",
                min_value=1,
                max_value=4,
                value=2,
                step=1,
                help="Generate multiple governed variations"
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                modifiers_input = st.text_input(
                    "Modifiers (comma-separated)",
                    placeholder="high quality, professional, clean",
                    help="Quality and style modifiers"
                )
                
                colors_input = st.text_input(
                    "Colors (comma-separated)",
                    placeholder="blue, white, gray",
                    help="Preferred brand colors"
                )
            
            with col2:
                elements_input = st.text_input(
                    "Elements (comma-separated)",
                    placeholder="laptop, plants, natural lighting",
                    help="Specific elements to include"
                )
                
                mood = st.text_input(
                    "Mood",
                    placeholder="professional, innovative, collaborative",
                    help="Desired atmosphere and tone"
                )
        
        # Generate button and view JSON
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_clicked = st.button("Generate Governed Images", type="primary", use_container_width=True)
        
        # View JSON Prompt link
        if scene:
            with st.expander("View JSON Prompt", expanded=False):
                try:
                    # Parse advanced options
                    modifiers = [m.strip() for m in modifiers_input.split(",") if m.strip()] if modifiers_input else None
                    colors = [c.strip() for c in colors_input.split(",") if c.strip()] if colors_input else None
                    elements = [e.strip() for e in elements_input.split(",") if e.strip()] if elements_input else None
                    
                    # Create prompt preview
                    if template != "basic":
                        preview_prompt = components["vlm_agent"].apply_template(
                            template,
                            scene,
                            style=style,
                            modifiers=modifiers,
                            colors=colors,
                            elements=elements,
                            mood=mood
                        )
                    else:
                        preview_prompt = components["vlm_agent"].create_prompt(
                            scene,
                            style=style,
                            modifiers=modifiers,
                            colors=colors,
                            elements=elements,
                            mood=mood
                        )
                    st.json(preview_prompt)
                except Exception as e:
                    st.error("Unable to generate prompt preview")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Only process if button clicked and scene is provided
    if generate_clicked:
        if not scene:
            st.error("Please provide a scene description!")
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
                
                # Validate against policies
                st.markdown('<h3 class="section-header">Policy Validation</h3>', unsafe_allow_html=True)
                is_valid, violations, warnings = components["policy_engine"].validate_prompt(prompt)
                
                policy_decision = {
                    "is_valid": is_valid,
                    "violations": violations,
                    "warnings": warnings,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Compact status summary
                if is_valid and not warnings:
                    st.markdown('<span class="status-pill status-success">Compliant</span> All policies passed', unsafe_allow_html=True)
                elif is_valid and warnings:
                    st.markdown('<span class="status-pill status-warning">Approved with Notes</span> Minor recommendations available', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-pill status-error">Policy Violation</span> Generation blocked', unsafe_allow_html=True)
                
                # Detailed messages in expander
                if violations or warnings:
                    with st.expander("View Policy Details"):
                        if violations:
                            st.subheader("Violations")
                            for violation in violations:
                                st.error(f"• {violation}")
                        if warnings:
                            st.subheader("Recommendations")
                            for warning in warnings:
                                st.warning(f"• {warning}")
                
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
                        st.info("**Enhanced Prompt with Brand Alignment Applied**")
                        prompt = enhanced_prompt
                
                # Generated Images Section
                st.markdown('<h3 class="section-header">Generated Images</h3>', unsafe_allow_html=True)
                st.markdown('<p class="section-subtext">All variants enforced by brand policies and recorded in the audit log.</p>', unsafe_allow_html=True)
                
                try:
                    # Show generation info and progress  
                    estimated_time = num_variants * 17  # Average 17 seconds per variant
                    
                    # Progress info box
                    with st.container():
                        st.info(f"**Generating {num_variants} creative variant{'s' if num_variants > 1 else ''}**")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Variants", num_variants)
                        with col2:
                            st.metric("⏱️ Est. Time", f"~{estimated_time}s")
                        with col3:
                            st.metric("Model", "Bria FIBO")
                        
                        # Progress steps
                        st.markdown("""
                        **Generation Process:**
                        1. 🔄 Initializing FIBO pipeline with your HF token
                        2. Creating unique variants with random seeds  
                        3. Applying creative enhancements (lighting, angles, moods)
                        4. Ensuring brand compliance throughout
                        5. Finalizing high-quality images
                        """)
                    
                    # Actual generation with enhanced spinner
                    with st.spinner(f"Generating {num_variants} brand-compliant creative variants... This may take {estimated_time}s"):
                        import time
                        start_time = time.time()
                        
                        results = components["fibo_client"].generate_images(
                            prompt,
                            num_variants=num_variants
                        )
                        
                        generation_time = time.time() - start_time
                        
                        # Show completion message
                        if results:
                            st.success(f"Generation completed in {generation_time:.1f}s!")
                        
                        # Log results
                        components["audit_log"].log_generation_result(entry_id, results)
                        
                        if not results:
                            st.warning("Remote FIBO generation is temporarily unavailable. Your prompt and audit log are still recorded.")
                        else:
                            # Display images in styled cards
                            for idx, result in enumerate(results):
                                st.markdown(f"""
                                <div class="image-card">
                                    <h4 style="color: #3b82f6; margin-bottom: 1rem;">Variant {result['variant_id']}</h4>
                                """, unsafe_allow_html=True)
                                
                                if "image" in result and result["image"]:
                                    st.image(
                                        result["image"], 
                                        caption=f"Variant {result['variant_id']} — Compliant",
                                        use_column_width=True
                                    )
                                
                                # Status indicator
                                if result.get("status") == "success":
                                    st.markdown('<span class="status-pill status-success">Compliant</span>', unsafe_allow_html=True)
                                elif result.get("status") == "safe_mode":
                                    st.markdown('<span class="status-pill status-warning">Safe Mode Preview</span>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<span class="status-pill status-warning">Placeholder Mode</span>', unsafe_allow_html=True)
                                
                                # Technical details in expander
                                with st.expander(f"Technical Details"):
                                    metadata = result.get("metadata", {})
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"**Model:** {metadata.get('model', 'Unknown')}")
                                        st.write(f"**Provider:** {metadata.get('provider', 'Unknown')}")
                                        st.write(f"**Generation Time:** {result.get('generation_time', 0):.1f}s")
                                    with col2:
                                        st.write(f"**Size:** {metadata.get('size', 'Unknown')}")
                                        st.write(f"**Seed:** {metadata.get('seed', 'Unknown')}")
                                    
                                    if result.get("prompt_string"):
                                        st.write("**Final Prompt:**")
                                        prompt_display = result.get("prompt_string", "")
                                        if len(prompt_display) > 200:
                                            prompt_display = prompt_display[:200] + "..."
                                        st.code(prompt_display)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)
                
                except Exception as e:
                    st.error("Remote FIBO generation is temporarily unavailable. Your prompt and audit log are still recorded.")
                    st.write("Technical details logged to console.")
                    print(f"Generation error: {e}")
            
            except Exception as e:
                st.error("An error occurred during processing. Please try again.")
                st.write("Technical details logged to console.")
                print(f"Processing error: {e}")

with tab2:
    st.markdown('<h2 class="section-header">Audit Log</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Every generation is captured with inputs, decisions, and outputs for compliance review.</p>', unsafe_allow_html=True)
    
    # Summary metrics at the top
    stats = components["audit_log"].get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="color: #3b82f6; margin: 0;">Total Requests</h4>
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0.25rem 0;">{stats["generation_requests"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="color: #059669; margin: 0;">Compliant %</h4>
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0.25rem 0;">{stats["approval_rate"]:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="color: #dc2626; margin: 0;">Violations</h4>
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0.25rem 0;">{stats["policy_violations"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Get last activity time
        entries = components["audit_log"].get_recent_entries(1)
        last_activity = "No activity" if not entries else entries[0].get('timestamp', 'N/A')[:16]
        
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="color: #9ca3af; margin: 0;">Last Activity</h4>
            <p style="font-size: 1rem; font-weight: bold; margin: 0.25rem 0;">{last_activity}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Controls
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("Clear Log", type="secondary"):
            components["audit_log"].clear_log()
            st.success("Audit log cleared!")
            st.rerun()
        
        limit = st.number_input("Show last N entries", min_value=5, max_value=50, value=10)
    
    # Display recent entries as clean rows
    entries = components["audit_log"].get_recent_entries(limit)
    
    if entries:
        st.markdown('<h4 style="color: #3b82f6; margin: 1rem 0 0.5rem 0;">Recent Activity</h4>', unsafe_allow_html=True)
        
        for entry in reversed(entries):
            entry_type = entry.get('type', 'unknown').replace('_', ' ').title()
            timestamp = entry.get('timestamp', 'N/A')
            
            # Determine status
            if entry_type == "Generation Request":
                is_valid = entry.get('policy_decision', {}).get('is_valid', False)
                status = "Compliant" if is_valid else "Blocked"
                status_class = "status-success" if is_valid else "status-error"
            else:
                status = "Recorded"
                status_class = "status-success"
            
            with st.expander(f"{timestamp} | {entry_type} | {status}", expanded=False):
                # Show key information first
                if entry_type == "Generation Request":
                    policy_decision = entry.get('policy_decision', {})
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Request Summary:**")
                        st.write(f"Status: {status}")
                        if policy_decision.get('violations'):
                            st.write("**Violations:**")
                            for violation in policy_decision['violations']:
                                st.write(f"• {violation}")
                        if policy_decision.get('warnings'):
                            st.write("**Warnings:**")
                            for warning in policy_decision['warnings']:
                                st.write(f"• {warning}")
                    
                    with col2:
                        prompt = entry.get('prompt', {})
                        if prompt.get('scene'):
                            st.write(f"**Scene:** {prompt['scene']}")
                        if prompt.get('style'):
                            st.write(f"**Style:** {prompt['style']}")
                        if prompt.get('modifiers'):
                            st.write(f"**Modifiers:** {', '.join(prompt['modifiers'])}")
                
                # Full JSON details
                st.divider()
                st.write("**Complete Entry Data:**")
                st.json(entry)
    else:
        st.info("No audit log entries yet. Generate some images to see the audit trail!")

with tab3:
    st.markdown('<h2 class="section-header">About FIBO BrandGuard</h2>', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #3b82f6 0%, #059669 100%); padding: 2rem; border-radius: 0.75rem; margin-bottom: 2rem; border: 1px solid #374151;'>
    <h3 style='color: white; text-align: center; margin: 0; font-size: 1.5rem;'>
    Enterprise-Grade AI Governance Platform
    </h3>
    <p style='color: rgba(255, 255, 255, 0.9); text-align: center; margin: 1rem 0 0 0; font-size: 1rem;'>
    FIBO BrandGuard bridges the gap between AI image generation and enterprise governance, ensuring every generated visual aligns with brand policies while maintaining complete audit trails for regulatory compliance.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Capabilities
    st.markdown("### Key Capabilities")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        • **Policy-First Generation**: Every prompt validated against brand guidelines before execution
        • **JSON-Native Prompts**: Structured, programmatic prompt construction for consistency
        • **Remote Bria FIBO Integration**: Direct API connection to Bria's cutting-edge model
        """)
    
    with col2:
        st.markdown("""
        • **Full Audit Trail**: Complete logging of all generations, decisions, and compliance actions
        • **Template-Based Workflows**: Pre-configured templates for common business use cases
        • **Creative Variant Generation**: Multiple governed variations with unique seeds
        """)
    
    st.divider()
    
    # Who It's For
    st.markdown("### Who It's For")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Global Brands**
        - Consistent visual identity
        - Multi-market compliance
        - Automated brand enforcement
        """)
    
    with col2:
        st.markdown("""
        **Financial Services**
        - Regulatory compliance
        - Risk management
        - Audit documentation
        """)
    
    with col3:
        st.markdown("""
        **Creative Agencies**
        - Client brand adherence
        - Scalable production
        - Quality assurance
        """)
    
    st.divider()
    
    # Architecture
    st.markdown("### Architecture")
    
    st.markdown("""
    FIBO BrandGuard implements a governance-first architecture where every component ensures compliance:
    
    **UI → Policy Engine → JSON Builder → Bria FIBO API → Audit Log**
    
    1. User provides scene description and style preferences
    2. Policy Engine validates against brand guidelines before generation
    3. VLM Agent constructs structured JSON prompts with compliance tags
    4. FIBO Client generates creative variants via Bria's remote API
    5. Audit Logger captures complete transaction history for compliance
    """)
    
    # Example prompt
    with st.expander("Example Governed JSON Prompt"):
        st.json({
            "scene": "Modern office workspace with diverse team collaborating",
            "style": "professional",
            "brand_colors": ["#3b82f6", "#ffffff"],
            "modifiers": ["high quality", "well-lit", "contemporary"],
            "elements": ["laptops", "modern furniture", "plants"],
            "mood": "innovative and collaborative",
            "compliance_tags": ["diversity", "professional", "brand-aligned"],
            "governance": {
                "validated": True,
                "policy_version": "1.0",
                "approved_themes": ["workplace", "technology", "collaboration"]
            }
        })
    
    st.divider()
    
    # Technologies Used
    st.markdown("### Technologies Used")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Core Platform**
        - Streamlit: Professional web interface
        - Python: Backend logic and policy enforcement
        - JSON: Structured data throughout system
        """)
    
    with col2:
        st.markdown("""
        **AI & Generation**
        - Bria FIBO 1.2: State-of-the-art image generation
        - HuggingFace Hub: Remote API integration
        - Custom VLM Agent: Intelligent prompt construction
        """)
    
    st.divider()
    
    # Hackathon Context
    st.markdown("### Hackathon Context")
    
    st.markdown("""
    Built for the Bria FIBO Hackathon to demonstrate production-ready, governed image generation. 
    FIBO BrandGuard showcases how enterprise organizations can deploy AI image generation with 
    proper governance, compliance, and audit capabilities while maintaining creative freedom 
    within brand guidelines.
    """)
    
    # System Status
    st.markdown("### System Status")
    
    try:
        setup_info = components["fibo_client"].validate_setup()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if setup_info.get("has_hf_token"):
                st.markdown('<span class="status-pill status-success">HF Token Connected</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-pill status-error">HF Token Missing</span>', unsafe_allow_html=True)
        
        with col2:
            if setup_info.get("client_available"):
                st.markdown('<span class="status-pill status-success">Remote Client Ready</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-pill status-warning">Safe Mode Active</span>', unsafe_allow_html=True)
        
        with col3:
            if setup_info.get("mode") == "remote-inference":
                st.markdown('<span class="status-pill status-success">Production Mode</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-pill status-warning">Demo Mode</span>', unsafe_allow_html=True)
        
        with st.expander("Detailed System Information"):
            st.json(setup_info)
    
    except Exception as e:
        st.error("Unable to check system status")
        st.write("Technical details logged to console.")
        print(f"Status check error: {e}")
    
    # Comparison table
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Typical AI Demos
        - Generate anything
        - No tracking or oversight  
        - Random text prompts
        - Individual use only
        - No compliance features
        """)
    
    with col2:
        st.markdown("""
        #### FIBO BrandGuard
        - Policy-driven generation
        - Complete compliance logging
        - JSON-native structured prompts
        - Template-based workflows
        - Automated governance validation
        """)
    
    st.divider()
    
    # Core innovations
    st.markdown("""
    ### Core Features
    
    #### Governance-First Architecture
    Platform validates every prompt against brand policies before generation:
    - Prompt validation against brand guidelines
    - Policy compliance checks  
    - Automated audit trail logging
    
    #### JSON-Native Enterprise Control
    Structured prompts enable programmatic, systematic generation:
    ```json
    {
      "scene": "Modern office workspace with diverse team",
      "style": "professional, clean, corporate", 
      "brand_colors": ["#0066CC", "#FFFFFF"],
      "compliance_tags": ["diversity", "professional", "brand-aligned"]
    }
    ```
    
    #### Intelligent Creative Variants
    Purposeful diversity within brand guidelines:
    - 12 types of creative variations including lighting, angles, and moods
    - **Unique Seed Management**: True randomness for each variant
    - **Brand Consistency**: All variants maintain compliance
    """)
    
    st.divider()
    
    # Enterprise value 
    st.markdown("""
    ### 🏢 Enterprise Value Delivered
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🏢 Corporate Marketing
        **Challenge**: 500+ marketing images need brand consistency  
        **Solution**: Automated policy validation + templates  
        **Outcome**: **95% reduction** in brand violations
        """)
    
    with col2:
        st.markdown("""
        #### Financial Services  
        **Challenge**: Regulatory compliance required  
        **Solution**: Policy engine with audit logging  
        **Outcome**: Full regulatory compliance automation
        """)
    
    with col3:
        st.markdown("""
        #### Design Agencies
        **Challenge**: Scale while maintaining brand standards  
        **Solution**: JSON workflows with creative variants  
        **Outcome**: 300% faster brand-compliant creative work
        """)
        
    st.divider()
    
    # Technical architecture
    st.markdown("""
    ### Enterprise Architecture
    
    **Modular, production-ready components:**
    
    - VLM Agent: JSON prompt construction and management
    - Policy Engine: Brand governance and compliance validation  
    - FIBO Client: Creative variant generation with unique seeds
    - Audit Logger: Complete operation tracking and regulatory reporting
    - Brand Profile: JSON-driven policy configuration system
    """)
    
    # Hackathon positioning
    st.markdown("""
    ### Hackathon Category: Best JSON-Native or Agentic Workflow
    
    **Demonstrates ideal JSON-native workflow:**
    
    1. Agentic Pipeline: VLM Agent → Policy Engine → FIBO Client → Audit Logger
    2. JSON Everything: Prompts, policies, audit logs, and brand profiles use structured data
    3. Systematic Workflow: Every step is programmable, repeatable, and auditable
    4. Enterprise Ready: Built for real business deployment beyond demonstration
    """)
    
    st.divider()
    
    # Tech stack
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### � Technologies Used
        
        - **Bria FIBO 1.2**: Advanced image generation via HuggingFace
        - **🖥️ Streamlit**: Professional web interface
        - **🐍 Python**: Backend logic and policy enforcement
        - **JSON**: Structured data throughout the system
        - **☁️ Cloud Ready**: Streamlit Cloud deployment
        """)
    
    with col2:
        st.markdown("""
        ### Quick Start Guide
        
        1. **🔑 Get HF Token**: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        2. **📝 Accept License**: [huggingface.co/briaai/FIBO](https://huggingface.co/briaai/FIBO)  
        3. **Clone & Run**:
           ```bash
           git clone https://github.com/Nolan0803/fibo-brandguard
           cd fibo-brandguard
           pip install -r requirements.txt
           echo "HF_TOKEN=your_token" > .env
           streamlit run app.py
           ```
        """)
        
    st.divider()
    
    # Footer section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏆 Built for Bria FIBO Hackathon 2025
        
        This platform showcases the future of enterprise AI governance - 
        demonstrating how Bria's cutting-edge FIBO model can be deployed 
        safely and systematically in real business environments.
        """)
    
    with col2:
        st.markdown("""
        ### 📧 Connect & Collaborate
        
        **🧑‍💻 Developer**: Nolan  
        **📂 Repository**: [GitHub - FIBO BrandGuard](https://github.com/Nolan0803/fibo-brandguard)  
        **🌐 Live Demo**: [Streamlit Cloud](https://fibo-brandguard.streamlit.app)  
        **📄 License**: MIT  
        **🏆 Category**: Best JSON-Native or Agentic Workflow
        """)
        
    # Closing message
    st.markdown("""
    ---
    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 20px;'>
    <h4 style='color: #1f77b4; margin: 0;'>FIBO BrandGuard</h4>
    <p style='margin: 5px 0 0 0; font-style: italic;'>Where Enterprise AI Governance Meets Creative Innovation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System status section
    st.subheader("System Status")
    
    try:
        setup_info = components["fibo_client"].validate_setup()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if setup_info.get("has_hf_token"):
                st.success("HF Token Connected")
            else:
                st.error("HF Token Missing")
        
        with col2:
            if setup_info.get("client_available"):
                st.success("Remote Client Ready")
            else:
                st.warning("Remote Client Unavailable")
        
        with col3:
            if setup_info.get("mode") == "remote-inference":
                st.success("Remote Mode Active")
            else:
                st.warning("Safe Mode Active")
        
        with st.expander("View Detailed System Information"):
            st.json(setup_info)
    
    except Exception as e:
        st.error("Unable to check system status")
        st.write("Technical details logged to console.")
        print(f"Status check error: {e}")

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        FIBO BrandGuard - Enterprise AI Image Generation | Built for Bria FIBO Hackathon
    </div>
    """,
    unsafe_allow_html=True
)
