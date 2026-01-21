import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from typing import Optional
import time
import re

# Page configuration
st.set_page_config(
    page_title="FlowForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Remove default Streamlit top spacing */
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .stApp > header {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
    }
    
    /* Header styling */
    .hero-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.25rem;
        margin-top: 0;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a0aec0;
        margin-bottom: 0.5rem;
        margin-top: 0;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.75rem;
        color: #a78bfa;
        font-weight: 500;
        white-space: nowrap;
    }
    
    /* Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.5rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0;
    }
    
    .card-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }
    
    .card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 0;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: rgba(15, 15, 26, 0.8) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #64748b !important;
    }
    
    .stTextInput input {
        background: rgba(15, 15, 26, 0.8) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Output code styling */
    .output-container {
        background: rgba(15, 15, 26, 0.9);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .stCode {
        background: rgba(15, 15, 26, 0.9) !important;
        border-radius: 12px !important;
    }
    
    pre {
        background: rgba(15, 15, 26, 0.9) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
    
    code {
        color: #a78bfa !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Labels */
    .stTextArea label, .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Compact expander */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
    }
    
    .streamlit-expanderContent {
        padding: 0.5rem 1rem !important;
    }
    
    /* Features grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 0.5rem 0 1rem 0;
    }
    
    .feature-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .feature-icon {
        font-size: 1rem;
        margin-bottom: 0;
    }
    
    .feature-text {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    /* Copy button styling */
    .copy-btn {
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #a78bfa;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        margin: 0.75rem 0;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .features-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Focus on title */
    .hero-title:focus {
        outline: 2px solid rgba(102, 126, 234, 0.5);
        outline-offset: 4px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'char_info' not in st.session_state:
    st.session_state.char_info = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'models/gemini-2.0-flash'

def parse_retry_time(error_message: str) -> Optional[float]:
    """Extract retry time in seconds from error message"""
    match = re.search(r'Please retry in ([\d.]+)s', error_message)
    if match:
        return float(match.group(1))
    return None

def format_retry_time(seconds: float) -> str:
    """Format retry time in human-readable format"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    else:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} {secs} second{'s' if secs > 1 else ''}"

def generate_eraser_code(brd_content: str, additional_info: str, api_key: str, model_name: str = 'models/gemini-2.0-flash') -> tuple:
    """Generate Eraser.io flowchart code using Google Gemini API"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
You are an expert in generating flowchart diagrams using ONLY Eraser.io native flowchart syntax.
You MUST follow the exact syntax defined here:
https://docs.eraser.io/docs/syntax-3

## INPUT DOCUMENT (BRD):
{brd_content}

## ADDITIONAL CONTEXT:
{additional_info if additional_info else "No additional context provided."}

## CRITICAL RULES (MANDATORY):
- DO NOT output YAML, JSON, Mermaid, Markdown, or any structured schema
- DO NOT use keys like nodes:, edges:, type:, style:
- Output ONLY plain-text Eraser.io flowchart DSL
- Each node must be defined on its own line
- Connections must use `->`
- Decisions must use `shape: diamond`
- Start/End must use `shape: oval`
- Use labels inside brackets only
- Output must be directly pasteable into https://app.eraser.io

## EXPECTED FORMAT (EXAMPLE):
title Sample Flow
direction right

Start [shape: oval]
ProcessA [label: "Some process"]
DecisionA [shape: diamond, label: "Decision?"]
End [shape: oval]

Start -> ProcessA
ProcessA -> DecisionA
DecisionA -> End : Yes

## TASK:
1. Analyze the BRD thoroughly
2. Identify all steps, decisions, and loops
3. Generate a clean, professional flowchart
4. Ensure logical flow and readable node names

## OUTPUT RULE:
- Output ONLY Eraser.io flowchart code
- No explanations
- No markdown
- No extra text

Generate the Eraser.io flowchart code now:
"""


        # Generate response (only 1 API call)
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        
        # Calculate character counts (no API calls)
        char_info = {
            'input_chars': len(prompt),
            'output_chars': len(output_text),
            'total_chars': len(prompt) + len(output_text)
        }
        
        return output_text, char_info
    
    except Exception as e:
        return f"Error: {str(e)}", None

# Header Section
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">FlowForge AI</h1>
    <span class="hero-badge">⚡ AI-Powered Diagram Generation</span>
</div>
<p class="hero-subtitle">Transform your Business Requirements into beautiful Eraser.io flowcharts instantly</p>
""", unsafe_allow_html=True)

# Focus on title on page load
components.html("""
<script>
    (function() {
        function focusTitle() {
            const title = document.querySelector('.hero-title');
            if (title) {
                title.setAttribute('tabindex', '-1');
                title.focus();
                return true;
            }
            return false;
        }
        
        // Try immediately
        if (!focusTitle()) {
            // If not found, wait for DOM
            setTimeout(function() {
                focusTitle();
            }, 100);
        }
    })();
</script>
""", height=0)

# Features section
st.markdown("""
<div class="features-grid">
    <div class="feature-item">
        <div class="feature-icon">📄</div>
        <div class="feature-text">BRD to Flowchart</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🤖</div>
        <div class="feature-text">Gemini AI Powered</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">⚡</div>
        <div class="feature-text">Instant Generation</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# API Key Section
with st.expander("🔑 Configure API Key", expanded=False):
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="Enter your Google Gemini API key...",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    model_options = {
        "Gemini 2.0 Flash": "models/gemini-2.0-flash",
        "Gemini Flash Latest": "models/gemini-flash-latest",
        "Gemini Pro Latest": "models/gemini-pro-latest",
        "Gemini 2.5 Flash": "models/gemini-2.5-flash",
        "Gemini 2.5 Pro": "models/gemini-2.5-pro"
    }
    
    selected_model_display = st.selectbox(
        "Select Model",
        options=list(model_options.keys()),
        index=list(model_options.values()).index(st.session_state.selected_model) if st.session_state.selected_model in model_options.values() else 0,
        help="Try different models if you get quota errors. Some models have better free tier support."
    )
    st.session_state.selected_model = model_options[selected_model_display]
    
    if api_key:
        st.session_state.api_key = api_key
        st.success(f"✓ API key configured | Model: {selected_model_display}")

# Main content columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <div class="card-icon">📋</div>
            <h3 class="card-title">Input Documents</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    brd_content = st.text_area(
        "BRD Document Content",
        height=200,
        placeholder="Paste your Business Requirements Document content here...\n\nExample:\n- Project Overview\n- Business Objectives\n- Process Flow\n- User Stories\n- Requirements",
        help="Paste the full content of your Business Requirements Document"
    )
    
    additional_info = st.text_input(
        "Additional Context (Optional)",
        placeholder="Any specific instructions or context for the flowchart...",
        help="Add any extra information to guide the flowchart generation"
    )
    
    # Character count (doesn't use API quota)
    if brd_content:
        char_count = len(brd_content) + len(additional_info or "")
        st.markdown(f"""
        <div style="padding: 0.6rem 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2); margin-bottom: 1rem;">
            <p style="color: #a78bfa; margin: 0; font-size: 0.85rem;">
                📝 <strong>Characters:</strong> {char_count:,}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    generate_clicked = st.button("⚡ Generate Flowchart Code", use_container_width=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <div class="card-icon">✨</div>
            <h3 class="card-title">Generated Eraser.io Code</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    output_placeholder = st.empty()
    
    if generate_clicked:
        if not st.session_state.api_key:
            st.error("⚠️ Please configure your Google Gemini API key first")
        elif not brd_content.strip():
            st.error("⚠️ Please enter BRD document content")
        else:
            with st.spinner("🔮 Generating flowchart code..."):
                result, char_info = generate_eraser_code(
                    brd_content, 
                    additional_info, 
                    st.session_state.api_key,
                    st.session_state.selected_model
                )
                st.session_state.generated_code = result
                st.session_state.char_info = char_info
    
    if st.session_state.generated_code:
        if st.session_state.generated_code.startswith("Error:"):
            error_msg = st.session_state.generated_code
            
            # Check if limit is 0 (no quota allocated)
            if "limit: 0" in error_msg:
                st.error(f"""
                🚨 **No Quota Allocated - Free Tier Not Enabled**
                
                Your API key shows `limit: 0`, which means **no free tier quota is allocated** to your account.
                This is different from exceeding a quota - your account doesn't have free tier access enabled.
                
                **🔧 How to Fix:**
                
                1. **Check Google AI Studio**: Go to https://aistudio.google.com/
                2. **Enable Free Tier**: Make sure free tier is enabled for your account
                3. **Verify API Key**: Ensure your API key is from a project with free tier enabled
                4. **Check Billing**: Some accounts require billing to be enabled (even with $0 spend limit)
                5. **Try Different Model**: The model `gemini-2.0-flash` might not be available in free tier
                
                **💡 Alternative Solutions:**
                - **Try a different model** using the dropdown above (e.g., `gemini-flash-latest` or `gemini-pro-latest`)
                - Create a new API key from Google AI Studio
                - Check your Google Cloud Console for API enablement
                - Enable billing with $0 spend limit (sometimes required for free tier)
                
                **📚 Helpful Links:**
                - Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits
                - Usage Dashboard: https://ai.dev/rate-limit
                - API Key Setup: https://makersuite.google.com/app/apikey
                """)
            else:
                retry_time = parse_retry_time(error_msg)
                
                if retry_time:
                    formatted_time = format_retry_time(retry_time)
                    st.error(f"""
                    ⚠️ **Quota Exceeded (Rate Limit)**
                    
                    {error_msg.split('Please retry')[0].strip()}
                    
                    ⏱️ **Please retry in: {formatted_time}**
                    
                    💡 *Tip: Free tier allows ~15 requests per minute. Wait a bit and try again.*
                    """)
                else:
                    st.error(error_msg)
        else:
            st.code(st.session_state.generated_code, language="plaintext")
            
            # Character count display
            if st.session_state.char_info:
                ci = st.session_state.char_info
                st.markdown(f"""
                <div style="margin-top: 1rem; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3);">
                    <p style="color: #10b981; margin: 0 0 0.5rem 0; font-size: 0.9rem; font-weight: 600;">📊 Character Count</p>
                    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                        <div style="color: #a0aec0; font-size: 0.85rem;">
                            <span style="color: #667eea;">Input:</span> {ci['input_chars']:,} chars
                        </div>
                        <div style="color: #a0aec0; font-size: 0.85rem;">
                            <span style="color: #a78bfa;">Output:</span> {ci['output_chars']:,} chars
                        </div>
                        <div style="color: #a0aec0; font-size: 0.85rem;">
                            <span style="color: #10b981;">Total:</span> {ci['total_chars']:,} chars
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Copy instruction
            st.markdown("""
            <div style="margin-top: 1rem; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
                <p style="color: #a78bfa; margin: 0; font-size: 0.9rem;">
                    💡 <strong>Tip:</strong> Copy the code above and paste it into <a href="https://app.eraser.io" target="_blank" style="color: #667eea;">Eraser.io</a> to view your flowchart
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 180px; color: #64748b; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;">🎨</div>
            <p style="font-size: 0.9rem; margin: 0;">Your generated Eraser.io code will appear here</p>
            <p style="font-size: 0.8rem; margin-top: 0.25rem; opacity: 0.7;">Enter your BRD content and click Generate</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
        Built with ❤️ using Streamlit & Google Gemini AI
    </p>
    <p style="color: #475569; font-size: 0.75rem; margin-top: 0.5rem;">
        FlowForge AI © 2026 | Transform documents into diagrams
    </p>
</div>
""", unsafe_allow_html=True)

