import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
import numpy as np
import google.generativeai as genai
import ast

# Configuration
st.set_page_config(page_title="Enhanced Loan Marketplace", page_icon="💰", layout="wide")
GOOGLE_API_KEY = "AIzaSyAKZv8PdQEy72iqoeonV8EHQWK0mK3_dNE"  # Hardcoded API key
genai.configure(api_key=GOOGLE_API_KEY)

# Enhanced CSS
st.markdown("""
<style>
    .loan-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .review-card {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .upgrade-card {
        background-color: #e7f5ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .improvement-tip {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

def get_loan_types_from_gemini():
    """Get additional loan types using Gemini AI with robust error handling"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = """Generate a Python dictionary containing additional business loan types with this exact structure:
        {
            'additional_loans': [
                {
                    'name': 'Equipment Financing Loan',
                    'provider': 'Tech Finance Ltd',
                    'type': 'Equipment Loan',
                    'interest_rate': 11.5,
                    'min_amount': 100000,
                    'max_amount': 1000000,
                    'tenure_range': (12, 48),
                    'processing_time': '3-5 days',
                    'processing_fee': 1.0,
                    'suitable_for': ['Manufacturing', 'Tech Companies'],
                    'required_documents': ['Business Registration', 'Equipment Quotation'],
                    'features': ['Quick Processing', 'Flexible Terms'],
                    'upgrade_criteria': {
                        'min_credit_score': 70,
                        'min_repayment_history': 6,
                        'interest_reduction': 1.5
                    }
                }
            ]
        }
        
        Generate 5 more loan types following exactly this structure. Return only the Python dictionary."""

        response = model.generate_content(prompt)
        
        # Validate and clean the response
        if not response or not response.text:
            st.warning("Empty response from Gemini API")
            return {'additional_loans': []}

        # Clean the response text
        cleaned_response = response.text.strip()
        
        # Remove code block markers if present
        if cleaned_response.startswith('```') and cleaned_response.endswith('```'):
            cleaned_response = cleaned_response.strip('`').strip()
        if cleaned_response.startswith('python'):
            cleaned_response = cleaned_response[6:].strip()

        try:
            # Use ast.literal_eval for safer parsing
            loan_types = ast.literal_eval(cleaned_response)
            
            # Validate the structure
            if not isinstance(loan_types, dict) or 'additional_loans' not in loan_types:
                st.warning("Invalid response format from Gemini API")
                return {'additional_loans': []}
            
            return loan_types
        
        except (SyntaxError, ValueError) as se:
            st.error(f"Error parsing Gemini response: {se}")
            st.error(f"Problematic response text: {cleaned_response}")
            return {'additional_loans': []}
            
    except Exception as e:
        st.error(f"Unexpected error fetching additional loan types: {str(e)}")
        return {'additional_loans': []}

def load_loan_database():
    """Load comprehensive loan database with contextual information"""
    base_loans = {
        'premium_loans': [
            {
                'name': 'Business Growth Plus',
                'provider': 'Premium Finance',
                'type': 'Premium Business Loan',
                'interest_rate': 8.5,
                'min_amount': 500000,
                'max_amount': 2000000,
                'tenure_range': (12, 60),
                'processing_time': '3-5 days',
                'processing_fee': 0.5,
                'suitable_for': ['Established Businesses', 'High Growth Startups'],
                'required_documents': ['2 Years Tax Returns', 'Business Plan', 'Financial Statements'],
                'features': ['Lower Interest Rates', 'Higher Limits', 'Flexible Repayment'],
                'upgrade_criteria': {
                    'min_credit_score': 80,
                    'min_repayment_history': 6,
                    'interest_reduction': 2.0
                }
            }
        ],
        'government_schemes': [
            {
                'name': 'PM Street Vendor AtmaNirbhar Nidhi',
                'provider': 'Government of India',
                'type': 'Micro Enterprise Loan',
                'interest_rate': 7.0,
                'min_amount': 10000,
                'max_amount': 50000,
                'tenure_range': (6, 24),
                'processing_time': '5-7 days',
                'processing_fee': 0,
                'suitable_for': ['Street Vendors', 'Small Shop Owners'],
                'required_documents': ['Aadhaar Card', 'Vendor Certificate'],
                'features': ['No Collateral Required', 'Zero Processing Fee'],
                'upgrade_criteria': {
                    'min_credit_score': 65,
                    'min_repayment_history': 3,
                    'interest_reduction': 1.0
                }
            }
        ],
        'startup_loans': [
            {
                'name': 'Digital Startup Boost',
                'provider': 'StartupFin',
                'type': 'Startup Loan',
                'interest_rate': 10.5,
                'min_amount': 200000,
                'max_amount': 1000000,
                'tenure_range': (12, 36),
                'processing_time': '4-6 days',
                'processing_fee': 1.0,
                'suitable_for': ['Tech Startups', 'Digital Services'],
                'required_documents': ['Startup Registration', 'Business Plan', 'Founder KYC'],
                'features': ['Mentorship Support', 'Network Access', 'Flexible Repayment'],
                'upgrade_criteria': {
                    'min_credit_score': 75,
                    'min_repayment_history': 4,
                    'interest_reduction': 1.5
                }
            }
        ]
    }
    
    # Add AI-generated loan types
    ai_loans = get_loan_types_from_gemini()
    if ai_loans and 'additional_loans' in ai_loans:
        base_loans['additional_loans'] = ai_loans['additional_loans']
    
    return base_loans

def calculate_credit_score(transactions_df):
    """Enhanced credit score calculation with detailed metrics"""
    credit_sum = transactions_df['credit'].sum()
    debit_sum = transactions_df['debit'].sum()
    balance_trend = transactions_df['balance'].diff().mean()
    transaction_consistency = len(transactions_df) / 30  # Normalized by month
    
    # Detailed scoring components
    components = {
        'income_stability': min(30, (credit_sum / debit_sum) * 15) if debit_sum > 0 else 30,
        'balance_growth': 25 if balance_trend > 0 else 10,
        'transaction_history': min(25, transaction_consistency * 5),
        'payment_regularity': 20 if (transactions_df['debit'] > 0).all() else 10
    }
    
    total_score = sum(components.values())
    return int(total_score), components

def get_credit_improvement_tips(credit_components):
    """Generate personalized credit improvement suggestions"""
    tips = []
    if credit_components['income_stability'] < 25:
        tips.append("Maintain consistent income deposits to improve stability score")
    if credit_components['balance_growth'] < 20:
        tips.append("Focus on maintaining positive account balance growth")
    if credit_components['transaction_history'] < 20:
        tips.append("Increase regular transaction activity to build history")
    if credit_components['payment_regularity'] < 15:
        tips.append("Ensure regular and timely bill payments")
    return tips

def calculate_loan_upgrade_eligibility(transactions_df, current_loan):
    """Calculate eligibility for loan upgrades"""
    credit_score, _ = calculate_credit_score(transactions_df)
    monthly_income = transactions_df['credit'].mean()
    
    upgrade_eligible = (
        credit_score >= current_loan['upgrade_criteria']['min_credit_score'] and
        monthly_income > current_loan['min_amount'] * 0.1
    )
    
    return {
        'eligible': upgrade_eligible,
        'new_interest_rate': max(5.0, current_loan['interest_rate'] - 
                               current_loan['upgrade_criteria']['interest_reduction']),
        'max_amount_increase': monthly_income * 12 if upgrade_eligible else 0
    }

def display_loan_marketplace(transactions_df):
    """Enhanced loan marketplace interface with upgrade options"""
    st.header("🏦 Enhanced Loan Marketplace")
    
    # Load loan database
    loan_database = load_loan_database()
    
    # Calculate credit score and components
    credit_score, credit_components = calculate_credit_score(transactions_df)
    
    # Display credit score and improvement tips
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Your Credit Score", f"{credit_score}/100")
    with col2:
        st.subheader("Credit Improvement Tips")
        tips = get_credit_improvement_tips(credit_components)
        for tip in tips:
            st.markdown(f"* {tip}")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        loan_type = st.selectbox(
            "Loan Type",
            ['All'] + list(loan_database.keys())
        )
    with col2:
        max_interest = st.slider("Maximum Interest Rate (%)", 5.0, 20.0, 15.0)
    with col3:
        processing_time = st.selectbox(
            "Processing Time",
            ['All', 'Within 2 days', '2-5 days', '5+ days']
        )

    # Display loans
    for category, loans in loan_database.items():
        if loan_type == 'All' or loan_type == category:
            for loan in loans:
                if loan['interest_rate'] <= max_interest:
                    # Calculate eligibility
                    monthly_income = transactions_df['credit'].mean()
                    is_eligible = (
                        credit_score >= 60 and
                        monthly_income > loan['min_amount'] * 0.1
                    )
                    
                    # Display loan card
                    st.markdown(f"""
                    <div class="loan-card">
                        <h3>{loan['name']} by {loan['provider']}</h3>
                        <p>{'🟢 Eligible' if is_eligible else '🔴 Not Eligible'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Details"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Loan Details")
                            st.write(f"Interest Rate: {loan['interest_rate']}% p.a.")
                            st.write(f"Amount Range: ₹{loan['min_amount']:,} - ₹{loan['max_amount']:,}")
                            st.write(f"Processing Time: {loan['processing_time']}")
                            st.write(f"Processing Fee: {loan['processing_fee']}%")
                            
                            if is_eligible:
                                # Calculate upgrade eligibility
                                upgrade_info = calculate_loan_upgrade_eligibility(
                                    transactions_df, loan
                                )
                                
                                st.subheader("Upgrade Potential")
                                if upgrade_info['eligible']:
                                    st.markdown("""
                                    <div class="upgrade-card">
                                        <h4>🌟 Upgrade Available!</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.write(f"New Interest Rate: {upgrade_info['new_interest_rate']}%")
                                    st.write(f"Additional Amount Available: ₹{upgrade_info['max_amount_increase']:,.2f}")
                                else:
                                    st.write("Complete 6 months of timely repayments to unlock upgrades")
                        
                        with col2:
                            st.subheader("Required Documents")
                            for doc in loan['required_documents']:
                                st.write(f"- {doc}")
                            
                            st.subheader("Features")
                            for feature in loan['features']:
                                st.write(f"- {feature}")
                            
                            if is_eligible:
                                st.subheader("Suitable For")
                                for business_type in loan['suitable_for']:
                                    st.write(f"- {business_type}")

def main():
    st.title("💰 Enhanced CreditWorthy Loan Marketplace")
    
    uploaded_file = st.sidebar.file_uploader("Upload Bank Statement (JSON)", type=['json'])
    
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            transactions_df = pd.DataFrame(data['transactions'])
            display_loan_marketplace(transactions_df)
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("Please upload your bank statement to view personalized loan options")

if __name__ == "__main__":
    main()
