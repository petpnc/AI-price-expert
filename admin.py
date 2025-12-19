"""
ValueAI - Admin Panel
Manage licenses, view payments, and monitor system usage
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Admin password (set in secrets)
ADMIN_PASSWORD = "admin123"  # Change this in production!

def check_admin_auth():
    """Check if user is authenticated as admin."""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    return st.session_state.admin_authenticated

def admin_login():
    """Display admin login page."""
    st.markdown("## 🔐 Admin Login")
    
    password = st.text_input("Admin Password", type="password")
    
    if st.button("Login"):
        # Get password from secrets or use default
        correct_password = st.secrets.get("ADMIN_PASSWORD", ADMIN_PASSWORD)
        
        if password == correct_password:
            st.session_state.admin_authenticated = True
            st.success("✅ Logged in as Admin")
            st.rerun()
        else:
            st.error("❌ Invalid password")

def load_credits():
    """Load credits from JSON or secrets."""
    try:
        if "credits" in st.secrets:
            return dict(st.secrets["credits"])
    except:
        pass
    
    credits_file = "credits.json"
    if os.path.exists(credits_file):
        with open(credits_file, 'r') as f:
            return json.load(f)
    return {}

def save_credits(credits):
    """Save credits to JSON file."""
    credits_file = "credits.json"
    try:
        with open(credits_file, 'w') as f:
            json.dump(credits, f, indent=2)
        return True
    except:
        return False

def load_payment_log():
    """Load payment log."""
    log_file = "payment_log.json"
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return json.load(f)
    return []

def show_license_management():
    """Display license key management interface."""
    st.markdown("### 🔑 License Key Management")
    
    credits = load_credits()
    
    # Display existing licenses
    if credits:
        st.markdown("#### Active License Keys")
        
        df = pd.DataFrame([
            {"License Key": key, "Credits": value}
            for key, value in credits.items()
        ])
        
        st.dataframe(df, use_container_width=True)
        
        # Total credits
        total_credits = sum(credits.values())
        total_licenses = len(credits)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Licenses", total_licenses)
        with col2:
            st.metric("Total Credits Available", total_credits)
    else:
        st.info("No license keys found.")
    
    st.markdown("---")
    
    # Add new license
    st.markdown("#### ➕ Create New License")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_key = st.text_input("License Key", placeholder="CUSTOM-KEY-2024")
    
    with col2:
        new_credits = st.number_input("Credits", min_value=1, value=10)
    
    if st.button("Create License", type="primary"):
        if new_key:
            credits[new_key.upper()] = new_credits
            if save_credits(credits):
                st.success(f"✅ Created license '{new_key.upper()}' with {new_credits} credits")
                st.rerun()
            else:
                st.error("❌ Failed to save license. Check file permissions.")
        else:
            st.warning("Please enter a license key.")
    
    st.markdown("---")
    
    # Modify existing license
    st.markdown("#### ✏️ Modify License")
    
    if credits:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_key = st.selectbox("Select License", list(credits.keys()))
        
        with col2:
            updated_credits = st.number_input("New Credits", min_value=0, value=credits.get(selected_key, 0))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Update Credits", use_container_width=True):
                credits[selected_key] = updated_credits
                if save_credits(credits):
                    st.success(f"✅ Updated '{selected_key}' to {updated_credits} credits")
                    st.rerun()
        
        with col2:
            if st.button("Delete License", use_container_width=True):
                if st.session_state.get('confirm_delete') == selected_key:
                    del credits[selected_key]
                    if save_credits(credits):
                        st.success(f"✅ Deleted '{selected_key}'")
                        st.session_state.confirm_delete = None
                        st.rerun()
                else:
                    st.session_state.confirm_delete = selected_key
                    st.warning("⚠️ Click again to confirm deletion")

def show_payment_history():
    """Display payment transaction history."""
    st.markdown("### 💰 Payment History")
    
    payments = load_payment_log()
    
    if payments:
        # Convert to DataFrame
        df = pd.DataFrame(payments)
        
        # Format timestamp
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Reorder columns
        columns_order = ['timestamp', 'license_key', 'email', 'amount_eur', 'credits', 'plan_id']
        df = df[[col for col in columns_order if col in df.columns]]
        
        st.dataframe(df, use_container_width=True)
        
        # Statistics
        st.markdown("#### 📊 Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Transactions", len(payments))
        
        with col2:
            total_revenue = sum([p.get('amount_eur', 0) for p in payments])
            st.metric("Total Revenue", f"€{total_revenue:.2f}")
        
        with col3:
            total_credits_sold = sum([p.get('credits', 0) for p in payments])
            st.metric("Credits Sold", total_credits_sold)
        
        # Export option
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"payments_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No payment history found.")

def show_system_info():
    """Display system information and settings."""
    st.markdown("### ⚙️ System Information")
    
    # Stripe status
    st.markdown("#### Payment Gateway Status")
    
    try:
        import stripe
        stripe_configured = "STRIPE_SECRET_KEY" in st.secrets
        
        if stripe_configured:
            st.success("✅ Stripe is configured and ready")
        else:
            st.warning("⚠️ Stripe not configured. Add STRIPE_SECRET_KEY to secrets.")
    except ImportError:
        st.error("❌ Stripe library not installed")
    
    # Google API status
    st.markdown("#### AI Service Status")
    
    try:
        import google.generativeai as genai
        google_configured = "GOOGLE_API_KEY" in st.secrets
        
        if google_configured:
            st.success("✅ Google Gemini API is configured")
        else:
            st.error("❌ Google API key not found")
    except ImportError:
        st.error("❌ Google Generative AI library not installed")
    
    # File status
    st.markdown("#### Data Files")
    
    files_status = {
        "credits.json": os.path.exists("credits.json"),
        "payment_log.json": os.path.exists("payment_log.json")
    }
    
    for file, exists in files_status.items():
        if exists:
            st.success(f"✅ {file}")
        else:
            st.info(f"ℹ️ {file} (will be created on first use)")

def main():
    """Main admin panel."""
    st.set_page_config(
        page_title="ValueAI Admin",
        page_icon="⚙️",
        layout="wide"
    )
    
    st.markdown("# ⚙️ ValueAI Admin Panel")
    
    # Check authentication
    if not check_admin_auth():
        admin_login()
        return
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    
    # Navigation
    st.sidebar.markdown("### 📋 Menu")
    page = st.sidebar.radio(
        "Select Page",
        ["License Management", "Payment History", "System Info"],
        label_visibility="collapsed"
    )
    
    # Display selected page
    if page == "License Management":
        show_license_management()
    elif page == "Payment History":
        show_payment_history()
    elif page == "System Info":
        show_system_info()

if __name__ == "__main__":
    main()
