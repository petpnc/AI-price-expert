"""
ValueAI - Payment Integration Module
Handles Stripe payment processing and credit management
"""

import streamlit as st
import stripe
import json
import os
from datetime import datetime

# ============================================================================
# STRIPE CONFIGURATION
# ============================================================================

def init_stripe():
    """Initialize Stripe with API keys from secrets."""
    try:
        if "STRIPE_SECRET_KEY" in st.secrets:
            stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
            return True
        else:
            st.warning("⚠️ Stripe not configured. Payment features disabled.")
            return False
    except Exception as e:
        st.error(f"Error initializing Stripe: {e}")
        return False

# ============================================================================
# PRICING PLANS
# ============================================================================

PRICING_PLANS = {
    "starter": {
        "name": "Starter Pack",
        "credits": 10,
        "price_eur": 5.00,
        "price_cents": 500,
        "description": "Perfect for trying out ValueAI",
        "features": ["10 AI analyses", "Valid for 30 days", "Email support"]
    },
    "professional": {
        "name": "Professional",
        "credits": 50,
        "price_eur": 20.00,
        "price_cents": 2000,
        "description": "Best value for regular users",
        "features": ["50 AI analyses", "Valid for 60 days", "Priority support", "Save 20%"],
        "badge": "🔥 MOST POPULAR"
    },
    "business": {
        "name": "Business",
        "credits": 150,
        "price_eur": 50.00,
        "price_cents": 5000,
        "description": "For power users and businesses",
        "features": ["150 AI analyses", "Valid for 90 days", "Premium support", "Save 33%"],
        "badge": "💎 BEST VALUE"
    },
    "enterprise": {
        "name": "Enterprise",
        "credits": 500,
        "price_eur": 150.00,
        "price_cents": 15000,
        "description": "Unlimited power for your business",
        "features": ["500 AI analyses", "Valid for 12 months", "Dedicated support", "Custom integrations", "Save 40%"]
    }
}

# ============================================================================
# PAYMENT FUNCTIONS
# ============================================================================

def create_checkout_session(plan_id, user_email=None):
    """
    Create a Stripe Checkout session for a pricing plan.
    Returns the checkout URL or None if failed.
    """
    if not init_stripe():
        return None
    
    plan = PRICING_PLANS.get(plan_id)
    if not plan:
        st.error("Invalid pricing plan selected.")
        return None
    
    try:
        # Get success and cancel URLs
        success_url = st.secrets.get("STRIPE_SUCCESS_URL", "http://localhost:8501?payment=success")
        cancel_url = st.secrets.get("STRIPE_CANCEL_URL", "http://localhost:8501?payment=cancel")
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': plan['price_cents'],
                    'product_data': {
                        'name': plan['name'],
                        'description': f"{plan['credits']} AI Analysis Credits",
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url + f"&session_id={{CHECKOUT_SESSION_ID}}&plan={plan_id}",
            cancel_url=cancel_url,
            customer_email=user_email,
            metadata={
                'plan_id': plan_id,
                'credits': plan['credits']
            }
        )
        
        return session.url
    
    except Exception as e:
        st.error(f"Payment error: {e}")
        return None

def verify_payment_session(session_id):
    """
    Verify a payment session and return the payment details.
    """
    if not init_stripe():
        return None
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            return {
                'success': True,
                'email': session.customer_email,
                'amount': session.amount_total / 100,
                'plan_id': session.metadata.get('plan_id'),
                'credits': int(session.metadata.get('credits', 0))
            }
        else:
            return {
                'success': False,
                'status': session.payment_status
            }
    
    except Exception as e:
        st.error(f"Error verifying payment: {e}")
        return None

# ============================================================================
# LICENSE KEY GENERATION
# ============================================================================

def generate_license_key(prefix="VAI"):
    """Generate a unique license key."""
    import random
    import string
    
    timestamp = datetime.now().strftime("%y%m")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    return f"{prefix}-{timestamp}-{random_part}"

def create_license_from_payment(payment_data):
    """
    Create a new license key based on payment data.
    Returns the license key or None if failed.
    """
    if not payment_data or not payment_data.get('success'):
        return None
    
    license_key = generate_license_key()
    credits = payment_data.get('credits', 0)
    
    # Save to payment log
    log_payment(license_key, payment_data)
    
    return {
        'license_key': license_key,
        'credits': credits,
        'email': payment_data.get('email'),
        'plan_id': payment_data.get('plan_id')
    }

# ============================================================================
# PAYMENT LOGGING
# ============================================================================

def log_payment(license_key, payment_data):
    """Log successful payment to a file."""
    log_file = "payment_log.json"
    
    log_entry = {
        'license_key': license_key,
        'timestamp': datetime.now().isoformat(),
        'email': payment_data.get('email'),
        'amount_eur': payment_data.get('amount'),
        'credits': payment_data.get('credits'),
        'plan_id': payment_data.get('plan_id')
    }
    
    try:
        # Load existing log
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        # Append new entry
        log.append(log_entry)
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error logging payment: {e}")
        return False

# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_pricing_card(plan_id, plan_data, col):
    """Display a pricing plan card in Streamlit."""
    with col:
        # Badge if present
        if "badge" in plan_data:
            st.markdown(f"**{plan_data['badge']}**")
        
        st.markdown(f"### {plan_data['name']}")
        st.markdown(f"*{plan_data['description']}*")
        
        # Price
        st.markdown(f"## €{plan_data['price_eur']:.2f}")
        st.markdown(f"**{plan_data['credits']} credits**")
        
        # Features
        st.markdown("**Features:**")
        for feature in plan_data['features']:
            st.markdown(f"✅ {feature}")
        
        # Buy button
        if st.button(f"Buy {plan_data['name']}", key=f"buy_{plan_id}", use_container_width=True):
            checkout_url = create_checkout_session(plan_id)
            if checkout_url:
                st.markdown(f"[🛒 Complete Purchase]({checkout_url})")
                st.info("👆 Click the link above to complete your purchase securely with Stripe.")

def show_pricing_page():
    """Display the pricing page with all plans."""
    st.markdown("## 💳 Choose Your Plan")
    st.markdown("Select the perfect plan for your needs. All plans include full access to ValueAI features.")
    
    st.markdown("---")
    
    # Display plans in columns
    plans = list(PRICING_PLANS.items())
    
    # First row - 2 plans
    col1, col2 = st.columns(2)
    display_pricing_card(plans[0][0], plans[0][1], col1)
    display_pricing_card(plans[1][0], plans[1][1], col2)
    
    st.markdown("---")
    
    # Second row - 2 plans
    col3, col4 = st.columns(2)
    display_pricing_card(plans[2][0], plans[2][1], col3)
    display_pricing_card(plans[3][0], plans[3][1], col4)
    
    st.markdown("---")
    
    # FAQ Section
    with st.expander("❓ Frequently Asked Questions"):
        st.markdown("""
        **How do credits work?**
        Each AI analysis costs 1 credit. Purchase a plan that fits your usage.
        
        **Are credits refundable?**
        Yes! Contact us within 14 days for a full refund if you're not satisfied.
        
        **Do credits expire?**
        Credits expire based on the plan validity period shown above.
        
        **What payment methods do you accept?**
        We accept all major credit cards through Stripe (Visa, Mastercard, Amex).
        
        **Is payment secure?**
        Yes! We use Stripe, a PCI-compliant payment processor trusted by millions.
        
        **Can I upgrade my plan?**
        Yes! Contact support and we'll upgrade your account with additional credits.
        """)

def handle_payment_callback():
    """Handle payment success/failure callbacks."""
    # Check URL parameters
    query_params = st.query_params
    
    if "payment" in query_params:
        payment_status = query_params["payment"]
        
        if payment_status == "success" and "session_id" in query_params:
            session_id = query_params["session_id"]
            
            # Verify payment
            payment_data = verify_payment_session(session_id)
            
            if payment_data and payment_data.get('success'):
                # Create license
                license_info = create_license_from_payment(payment_data)
                
                if license_info:
                    st.success("🎉 Payment Successful!")
                    
                    st.markdown(f"""
                    ### Your License Key:
                    ```
                    {license_info['license_key']}
                    ```
                    
                    **Credits:** {license_info['credits']}
                    
                    ⚠️ **Important:** Save this license key! It has been sent to {license_info['email']}
                    
                    You can now use this key to log in and start analyzing items.
                    """)
                    
                    # Add credits to system
                    from app import save_credits, load_credits
                    credits = load_credits()
                    credits[license_info['license_key']] = license_info['credits']
                    save_credits(credits)
                    
                    st.balloons()
                    
                    if st.button("🚀 Start Using ValueAI"):
                        st.rerun()
            else:
                st.error("❌ Payment verification failed. Please contact support.")
        
        elif payment_status == "cancel":
            st.warning("⚠️ Payment was cancelled. No charges were made.")
