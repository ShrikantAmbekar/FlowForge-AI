import streamlit as st
import google.generativeai as genai
from typing import Optional
import time

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
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #a0aec0;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        color: #a78bfa;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.2rem;
    }
    
    .card-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .card-title {
        font-size: 1.1rem;
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
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Features grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #94a3b8;
        font-size: 0.85rem;
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
        margin: 2rem 0;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

def generate_eraser_code(brd_content: str, additional_info: str, api_key: str) -> Optional[str]:
    """Generate Eraser.io flowchart code using Google Gemini API"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""You are an expert at creating Eraser.io diagram code. Based on the following Business Requirements Document (BRD) content and additional information, generate a comprehensive flowchart using Eraser.io syntax.

## BRD Document Content:
{brd_content}

## Additional Information/Context:
{additional_info if additional_info else "No additional information provided."}

## Instructions:
1. Analyze the BRD content carefully to understand the business process flow
2. Identify all key steps, decision points, and process flows
3. Generate clean, well-structured Eraser.io flowchart code
4. Use appropriate shapes: rectangles for processes, diamonds for decisions, rounded rectangles for start/end
5. Include clear labels and connections
6. Organize the flow logically from top to bottom or left to right

## Output Requirements:
- Generate ONLY the Eraser.io diagram code
- Do not include any explanations or markdown formatting
- Use proper Eraser.io syntax for flowcharts
- Ensure all connections are properly defined
- Use meaningful node names and labels

Generate the Eraser.io flowchart code now:"""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

# Header Section
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
st.markdown('<span class="hero-badge">⚡ AI-Powered Diagram Generation</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">FlowForge AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Transform your Business Requirements into beautiful Eraser.io flowcharts instantly</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
with st.expander("🔑 Configure API Key", expanded=not st.session_state.api_key):
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="Enter your Google Gemini API key...",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("✓ API key configured")

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
        height=300,
        placeholder="Paste your Business Requirements Document content here...\n\nExample:\n- Project Overview\n- Business Objectives\n- Process Flow\n- User Stories\n- Requirements",
        help="Paste the full content of your Business Requirements Document"
    )
    
    additional_info = st.text_input(
        "Additional Context (Optional)",
        placeholder="Any specific instructions or context for the flowchart...",
        help="Add any extra information to guide the flowchart generation"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
                result = generate_eraser_code(
                    brd_content, 
                    additional_info, 
                    st.session_state.api_key
                )
                st.session_state.generated_code = result
    
    if st.session_state.generated_code:
        if st.session_state.generated_code.startswith("Error:"):
            st.error(st.session_state.generated_code)
        else:
            st.code(st.session_state.generated_code, language="plaintext")
            
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
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; color: #64748b; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">🎨</div>
            <p style="font-size: 1rem; margin: 0;">Your generated Eraser.io code will appear here</p>
            <p style="font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.7;">Enter your BRD content and click Generate</p>
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

