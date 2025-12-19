import streamlit as st
import google.generativeai as genai
import json
import os
from PIL import Image
import io
from datetime import datetime

# Import payment module
try:
    from payments import show_pricing_page, handle_payment_callback, init_stripe
    PAYMENTS_ENABLED = True
except ImportError:
    PAYMENTS_ENABLED = False

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="ValueAI - Smart Item Valuation",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Google API Key from Streamlit secrets
# In production: Add your API key to .streamlit/secrets.toml as:
# GOOGLE_API_KEY = "your-api-key-here"
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("⚠️ Google API Key not found in secrets. Please configure it in .streamlit/secrets.toml")
    st.stop()

# ============================================================================
# CREDITS MANAGEMENT SYSTEM
# ============================================================================

CREDITS_FILE = "credits.json"

def load_credits():
    """Load credits from Streamlit secrets (cloud) or JSON file (local)."""
    # Try to load from Streamlit secrets first (for cloud deployment)
    try:
        if "credits" in st.secrets:
            return dict(st.secrets["credits"])
    except:
        pass
    
    # Fallback to local JSON file (for local development)
    if not os.path.exists(CREDITS_FILE):
        # Initialize with demo data
        default_credits = {
            "DEMO-KEY": 3,
            "CLIENT-100": 50,
            "PREMIUM-2024": 100,
            "TEST-KEY": 10
        }
        save_credits(default_credits)
        return default_credits
    
    try:
        with open(CREDITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading credits: {e}")
        return {}

def save_credits(credits_data):
    """Save credits to JSON file. Fails silently on cloud (uses secrets instead)."""
    try:
        with open(CREDITS_FILE, 'w', encoding='utf-8') as f:
            json.dump(credits_data, f, indent=2)
        return True
    except Exception as e:
        # On cloud, file system is read-only for app directory
        # Credits should be managed via Streamlit secrets
        return False

def validate_license_key(key):
    """Check if license key is valid and has credits."""
    credits = load_credits()
    if key in credits and credits[key] > 0:
        return True, credits[key]
    return False, 0

def deduct_credit(key):
    """Deduct one credit from the license key."""
    credits = load_credits()
    if key in credits and credits[key] > 0:
        credits[key] -= 1
        save_credits(credits)
        return True
    return False

# HOW TO ADD MORE LICENSE KEYS:
# 1. Open credits.json file
# 2. Add a new line with format: "YOUR-KEY-NAME": number_of_credits
# 3. Save the file
# Example:
# {
#   "DEMO-KEY": 3,
#   "NEW-CLIENT": 25,  <-- Add this line
#   "PREMIUM-2024": 100
# }

# ============================================================================
# AI ANALYSIS FUNCTION
# ============================================================================

def analyze_item_with_gemini(image):
    """
    Analyze uploaded image using Google Gemini API.
    Returns structured JSON with item valuation.
    """
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Craft the expert appraiser prompt
        prompt = """You are an expert appraiser and valuation specialist with decades of experience across antiques, collectibles, electronics, furniture, and everyday items.

Analyze the item in this image and provide a detailed valuation report in STRICT JSON format.

Your response must be ONLY valid JSON (no markdown, no explanations outside JSON) with these exact fields:

{
  "item_name": "Clear identification of the item",
  "condition": "Excellent/Good/Fair/Poor - with brief explanation",
  "price_new": "Estimated retail price if brand new (numeric value in EUR)",
  "price_used_fast": "Quick sale price for bazaar/Facebook Marketplace (numeric value in EUR)",
  "price_collector": "High-end collector/auction price if rare/vintage (numeric value in EUR)",
  "description": "A compelling 2-3 sentence sales description suitable for a classified ad, highlighting key features and value proposition"
}

Important guidelines:
- Be realistic and conservative with valuations
- Consider visible condition, brand, age, and market demand
- All prices in EUR (€)
- For common items, collector price may equal or be slightly above used_fast price
- For rare/vintage items, collector price can be significantly higher
- Description should be persuasive but honest

Analyze the image now and respond with ONLY the JSON object."""

        # Generate response
        response = model.generate_content([prompt, image])
        
        # Parse JSON from response
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        result = json.loads(response_text.strip())
        
        return {
            "success": True,
            "data": result
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse AI response. The AI didn't return valid JSON. Try again or use a clearer image."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"AI Analysis Error: {str(e)}"
        }

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    # Handle payment callbacks first
    if PAYMENTS_ENABLED:
        handle_payment_callback()
    
    # Custom CSS for better mobile responsiveness and styling
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
        }
        .copy-button {
            background: #28a745 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💎 ValueAI</h1>
        <p>Smart AI-Powered Item Valuation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # AUTHENTICATION
    # ========================================================================
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.license_key = None
        st.session_state.credits = 0
    
    if not st.session_state.authenticated:
        st.markdown("### 🔐 Enter Your License Key")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            license_input = st.text_input(
                "License Key",
                placeholder="Enter your license key (e.g., DEMO-KEY)",
                label_visibility="collapsed"
            )
        
        with col2:
            login_button = st.button("🚀 Login", use_container_width=True)
        
        if login_button:
            if license_input:
                is_valid, credits = validate_license_key(license_input.strip().upper())
                
                if is_valid:
                    st.session_state.authenticated = True
                    st.session_state.license_key = license_input.strip().upper()
                    st.session_state.credits = credits
                    st.success(f"✅ Welcome! You have {credits} credits available.")
                    st.rerun()
                else:
                    st.error("❌ Invalid license key or no credits remaining.")
            else:
                st.warning("⚠️ Please enter a license key.")
        
        # Demo info
        with st.expander("ℹ️ Demo Keys Available"):
            st.info("Try these demo keys:\n- **DEMO-KEY** (3 credits)\n- **TEST-KEY** (10 credits)")
        
        # Buy credits option
        if PAYMENTS_ENABLED:
            st.markdown("---")
            st.markdown("### 💳 Don't have a license key?")
            if st.button("Buy Credits Now", use_container_width=True, type="primary"):
                st.session_state.show_pricing_guest = True
                st.rerun()
        
        st.stop()
    
    # Handle guest pricing page
    if 'show_pricing_guest' in st.session_state and st.session_state.show_pricing_guest:
        if PAYMENTS_ENABLED:
            show_pricing_page()
            
            if st.button("⬅️ Back to Login"):
                st.session_state.show_pricing_guest = False
                st.rerun()
        
        st.stop()
    
    # ========================================================================
    # SIDEBAR - Credits & Info
    # ========================================================================
    
    with st.sidebar:
        st.markdown("### 👤 Account Info")
        st.markdown(f"**License:** `{st.session_state.license_key}`")
        
        # Refresh credits from file
        _, current_credits = validate_license_key(st.session_state.license_key)
        st.session_state.credits = current_credits
        
        st.metric("💳 Credits Remaining", st.session_state.credits)
        
        if st.session_state.credits == 0:
            st.error("⚠️ No credits remaining!")
        
        # Buy more credits button
        if PAYMENTS_ENABLED:
            st.markdown("---")
            if st.button("💳 Buy More Credits", use_container_width=True, type="primary"):
                st.session_state.show_pricing = True
                st.rerun()
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.license_key = None
            st.session_state.credits = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 How It Works")
        st.markdown("""
        1. Upload or take a photo
        2. AI analyzes the item
        3. Get instant valuation
        4. Copy sales description
        
        **Cost:** 1 credit per analysis
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use clear, well-lit photos
        - Show the full item
        - Include any brands/labels
        - Avoid blurry images
        """)
    
    # ========================================================================
    # MAIN CONTENT
    # ========================================================================
    
    # Check if user wants to see pricing
    if 'show_pricing' not in st.session_state:
        st.session_state.show_pricing = False
    
    # Show pricing page if requested
    if st.session_state.show_pricing and PAYMENTS_ENABLED:
        show_pricing_page()
        
        if st.button("⬅️ Back to App"):
            st.session_state.show_pricing = False
            st.rerun()
        
        st.stop()
    
    if st.session_state.credits == 0:
        st.error("❌ You have no credits remaining. Please contact support to purchase more credits.")
        st.stop()
    
    st.markdown("### 📸 Upload or Capture Item Photo")
    
    # Image input options
    tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Take Photo"])
    
    uploaded_file = None
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
    
    with tab2:
        camera_photo = st.camera_input("Take a picture", label_visibility="collapsed")
        if camera_photo is not None:
            uploaded_file = camera_photo
    
    # Process image if uploaded
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Item to Analyze", use_container_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Item & Get Valuation", use_container_width=True, type="primary"):
            
            with st.spinner("🤖 AI is analyzing your item... This may take a few seconds..."):
                # Call Gemini API
                result = analyze_item_with_gemini(image)
                
                if result["success"]:
                    # Deduct credit
                    if deduct_credit(st.session_state.license_key):
                        st.session_state.credits -= 1
                        
                        data = result["data"]
                        
                        # Display results
                        st.success("✅ Analysis Complete!")
                        
                        st.markdown("---")
                        st.markdown("### 📊 Valuation Report")
                        
                        # Item Info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Item:** {data.get('item_name', 'Unknown')}")
                        with col2:
                            st.markdown(f"**Condition:** {data.get('condition', 'Not specified')}")
                        
                        st.markdown("---")
                        
                        # Price metrics
                        st.markdown("### 💰 Estimated Values (EUR)")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "🆕 New Price",
                                f"€{data.get('price_new', 0)}",
                                help="Estimated retail price if brand new"
                            )
                        
                        with col2:
                            st.metric(
                                "⚡ Quick Sale",
                                f"€{data.get('price_used_fast', 0)}",
                                help="Fast sale price (Bazaar/Facebook)"
                            )
                        
                        with col3:
                            st.metric(
                                "🏆 Collector Price",
                                f"€{data.get('price_collector', 0)}",
                                help="High-end collector/auction price"
                            )
                        
                        st.markdown("---")
                        
                        # Sales Description
                        st.markdown("### 📝 Ready-to-Use Sales Description")
                        
                        description = data.get('description', 'No description available')
                        
                        st.text_area(
                            "Copy this description for your ad:",
                            value=description,
                            height=120,
                            label_visibility="collapsed"
                        )
                        
                        st.info("💡 **Tip:** Copy the text above and paste it directly into your Bazaar or Facebook Marketplace listing!")
                        
                        # Timestamp
                        st.caption(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        
                    else:
                        st.error("Failed to deduct credit. Please try again.")
                
                else:
                    st.error(f"❌ {result.get('error', 'Unknown error occurred')}")
                    st.info("💡 Try uploading a clearer image or a different angle of the item.")

if __name__ == "__main__":
    main()
