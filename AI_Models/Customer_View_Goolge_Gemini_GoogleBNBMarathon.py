import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
import google.generativeai as genai
from youtube_search import YoutubeSearch

# Gemini API Configuration
GOOGLE_API_KEY = "Your API"  # Hardcoded API key
genai.configure(api_key=GOOGLE_API_KEY)

class CreditScoreEnhancer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.languages = {
            'English': 'en',
            'Hindi': 'hi',
            'Kannada': 'kn',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Malayalam': 'ml'
        }

    def generate_localized_credit_improvement_tips(self, language='English', score=None):
        """
        Generate credit score improvement tips in the specified language
        """
        prompt = f"""
        Generate comprehensive, actionable credit score improvement tips 
        in {language} language. Provide:
        - 5-7 specific strategies
        - Detailed explanation for each strategy
        - Potential impact on credit score
        - Practical implementation steps
        
        Context:
        - Current language: {language}
        - Current credit score: {score or 'Not specified'}
        """

        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating tips: {str(e)}"

    def fetch_youtube_recommendations(self, query, language='English', max_results=5):
        """
        Fetch YouTube video recommendations for credit score improvement
        """
        localized_query = f"{query} in {language}"
        try:
            yt_results = YoutubeSearch(localized_query, max_results=max_results).to_dict()
            return [
                {
                    'title': video['title'],
                    'channel': video['channel'],
                    'thumbnail': video['thumbnails'][0],
                    'link': f"https://youtube.com/watch?v={video['id']}"
                } for video in yt_results
            ]
        except Exception as e:
            st.error(f"Error fetching YouTube videos: {str(e)}")
            return []

    def fetch_government_resources(self, language='English'):
        """
        Fetch government and official financial literacy resources
        """
        resources = {
            'English': [
                {'name': 'RBI Financial Literacy', 'url': 'https://www.rbi.org.in/Scripts/Financial_Literacy.aspx'},
                {'name': 'SEBI Investor Education', 'url': 'https://www.sebi.gov.in/investor-education.html'}
            ],
            'Hindi': [
                {'name': 'RBI वित्तीय साक्षरता', 'url': 'https://www.rbi.org.in/Scripts/Financial_Literacy.aspx'},
                {'name': 'SEBI निवेशक शिक्षा', 'url': 'https://www.sebi.gov.in/investor-education.html'}
            ]
            # Add more language-specific resources
        }
        return resources.get(language, resources['English'])

def clean_date(date_str):
    """Clean date string by removing INB suffix if present"""
    return re.sub(r'INB$', '', date_str)

def prepare_transaction_data(transactions):
    df = pd.DataFrame(transactions)
    
    # Clean date strings and convert to datetime
    df['date'] = df['date'].apply(clean_date)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%y')
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    
    # Convert amount columns to float
    df['credit'] = pd.to_numeric(df['credit'], errors='coerce').fillna(0)
    df['debit'] = pd.to_numeric(df['debit'], errors='coerce').fillna(0)
    df['balance'] = pd.to_numeric(df['balance'], errors='coerce').fillna(0)
    
    return df

def categorize_nano_entrepreneur_transactions(description):
    """Enhanced transaction categorization for nano-entrepreneurs"""
    categories = {
        'BUSINESS_INCOME': ['SALARY', 'INVESTMENT', 'BONUS', 'RETURNS', 'CREDIT'],
        'BUSINESS_EXPENSE': ['UTILITY', 'BILL', 'SHOPPING', 'STORE'],
        'PERSONAL_EXPENSE': ['COFFEE', 'FOOD', 'BEVERAGES'],
        'TRANSFER': ['RENT', 'TRANSFER', 'REFUND'],
        'OTHERS': []
    }
    
    description = str(description).upper()
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'OTHERS'

def calculate_financial_metrics(df, summary_data):
    metrics = {}
    
    # Basic transaction metrics
    metrics['total_transactions'] = len(df)
    metrics['total_credits'] = df['credit'].sum()
    metrics['total_debits'] = df['debit'].sum()
    metrics['net_cashflow'] = metrics['total_credits'] - metrics['total_debits']
    
    # Balance metrics
    metrics['opening_balance'] = float(summary_data.get('opening_balance', 0))
    metrics['closing_balance'] = float(summary_data.get('closing_balance', 0))
    metrics['avg_balance'] = df['balance'].mean()
    metrics['balance_volatility'] = df['balance'].std()
    
    # Transaction patterns
    metrics['avg_transaction_size'] = df['debit'][df['debit'] > 0].mean()
    metrics['transaction_frequency'] = len(df) / 30  # transactions per day
    
    # Credit patterns
    credit_txns = len(df[df['credit'] > 0])
    metrics['credit_frequency'] = credit_txns / max(len(df), 1)
    metrics['avg_credit_amount'] = df[df['credit'] > 0]['credit'].mean() if credit_txns > 0 else 0
    
    return metrics

def calculate_nano_entrepreneur_score(metrics):
    """
    Custom scoring for nano-entrepreneurs considering unique financial patterns
    """
    # Income Stability (40 points)
    income_stability = min(
        metrics['credit_frequency'] * 20 +  # Frequency of income
        (metrics['avg_credit_amount'] > 10000) * 20  # Consistent income threshold
    , 40)
    
    # Business Resilience (30 points)
    business_resilience = min(
        (metrics['net_cashflow'] > 0) * 20 +  # Positive cash flow
        (metrics['balance_volatility'] < metrics['avg_balance'] * 0.3) * 10  # Low balance fluctuation
    , 30)
    
    # Transaction Discipline (20 points)
    transaction_discipline = min(
        (metrics['transaction_frequency'] > 0.5) * 10 +  # Regular transactions
        (metrics['avg_transaction_size'] < metrics['avg_credit_amount'] * 0.5) * 10  # Controlled spending
    , 20)
    
    # Growth Potential (10 points)
    growth_potential = min(
        (metrics['closing_balance'] > metrics['opening_balance']) * 5 +
        (metrics['total_credits'] > metrics['total_debits']) * 5
    , 10)
    
    # Total Nano-Entrepreneur Score
    nano_score = income_stability + business_resilience + transaction_discipline + growth_potential
    
    return {
        'score': min(max(nano_score, 0), 100),
        'breakdown': {
            'Income Stability': income_stability,
            'Business Resilience': business_resilience,
            'Transaction Discipline': transaction_discipline,
            'Growth Potential': growth_potential
        }
    }

# 

def generate_ai_insights(df, metrics, nano_score):
    """
    Generate AI-powered insights with fallback for API failures
    """
    try:
        # Existing Gemini API logic
        top_credit_transaction = df[df['credit'] > 0].sort_values('credit', ascending=False).iloc[0]
        worst_transaction = df[df['debit'] > 0].sort_values('debit', ascending=False).iloc[0]
        
        prompt = f"""
        Analyze the financial data for a nano entrepreneur with the following details:
        
        Financial Metrics:
        - Total Transactions: {metrics['total_transactions']}
        - Total Credits: ₹{metrics['total_credits']:.2f}
        - Total Debits: ₹{metrics['total_debits']:.2f}
        - Net Cashflow: ₹{metrics['net_cashflow']:.2f}
        
        Nano Entrepreneur Score: {nano_score['score']}/100
        Score Breakdown:
        - Income Stability: {nano_score['breakdown']['Income Stability']}
        - Business Resilience: {nano_score['breakdown']['Business Resilience']}
        - Transaction Discipline: {nano_score['breakdown']['Transaction Discipline']}
        - Growth Potential: {nano_score['breakdown']['Growth Potential']}
        
        Top Credit Transaction:
        - Date: {top_credit_transaction['date']}
        - Amount: ₹{top_credit_transaction['credit']}
        - Description: {top_credit_transaction['description']}
        
        Worst Transaction:
        - Date: {worst_transaction['date']}
        - Amount: ₹{worst_transaction['debit']}
        - Description: {worst_transaction['description']}
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        # Fallback insights based on financial metrics
        income_ratio = metrics['total_credits'] / max(metrics['total_debits'], 1)
        avg_transaction = metrics['total_debits'] / max(metrics['total_transactions'], 1)
        
        insights = f"""
### Financial Health Analysis

#### Income and Expense Analysis
- Your income to expense ratio is {income_ratio:.2f}, indicating {'strong' if income_ratio > 2 else 'moderate' if income_ratio > 1 else 'concerning'} financial health
- Average transaction size: ₹{avg_transaction:,.2f}
- Net cashflow: ₹{metrics['net_cashflow']:,.2f} ({'positive' if metrics['net_cashflow'] > 0 else 'negative'})

#### Strengths
- {'Strong income stability' if nano_score['breakdown']['Income Stability'] > 30 else 'Room for improving income stability'}
- {'Good business resilience' if nano_score['breakdown']['Business Resilience'] > 20 else 'Opportunity to build business resilience'}

#### Areas for Improvement
- {'Focus on transaction discipline' if nano_score['breakdown']['Transaction Discipline'] < 15 else 'Good transaction management'}
- {'Look for growth opportunities' if nano_score['breakdown']['Growth Potential'] < 7 else 'Strong growth trajectory'}

#### Recommendations
1. {'Consider diversifying income sources' if nano_score['breakdown']['Income Stability'] < 30 else 'Maintain strong income streams'}
2. {'Build emergency reserves' if metrics['avg_balance'] < metrics['total_debits'] else 'Continue maintaining healthy reserves'}
3. {'Review and optimize expenses' if income_ratio < 1.5 else 'Maintain current expense management'}
4. {'Focus on consistent transactions' if nano_score['breakdown']['Transaction Discipline'] < 15 else 'Keep up disciplined transaction patterns'}
"""
        return insights

def display_credit_score_improvement_section(credit_score, selected_language):
    """
    Display credit score improvement strategies section
    """
    st.header("💡 Credit Score Improvement Strategies")
    
    # Initialize Credit Score Enhancer
    enhancer = CreditScoreEnhancer(GOOGLE_API_KEY)

    # Generate Localized Tips
    st.subheader(f"Credit Improvement Tips in {selected_language}")
    tips = enhancer.generate_localized_credit_improvement_tips(
        language=selected_language, 
        score=credit_score
    )
    st.markdown(tips)

    # YouTube Recommendations
    st.subheader("📹 Recommended Learning Videos")
    videos = enhancer.fetch_youtube_recommendations(
        "credit score improvement financial literacy", 
        language=selected_language
    )
    
    # Display Video Recommendations
    cols = st.columns(len(videos))
    for i, video in enumerate(videos):
        with cols[i]:
            st.image(video['thumbnail'], use_container_width=True)
            st.write(video['title'])
            st.link_button("Watch Video", video['link'])

    # Government Resources
    st.subheader("🏛️ Official Financial Resources")
    resources = enhancer.fetch_government_resources(language=selected_language)
    for resource in resources:
        st.write(f"[{resource['name']}]({resource['url']})")

def main():
    st.set_page_config(page_title="Nano Entrepreneur Financial Platform", layout="wide")
    st.title("🚀 Nano Entrepreneur Financial Analysis & Credit Improvement")
    
    # Language Selection
    st.sidebar.header("🌐 Language Preference")
    selected_language = st.sidebar.selectbox(
        "Choose Your Preferred Language", 
        list(CreditScoreEnhancer('').languages.keys())
    )
    
    # Sidebar Tips
    st.sidebar.header("💡 Financial Management Tips")
    st.sidebar.write("""
    - Maintain consistent income streams
    - Control and minimize unnecessary expenses
    - Build an emergency fund
    - Invest in business growth
    - Regularly review financial performance
    """)
    
    uploaded_file = st.file_uploader("Upload Bank Statement", type=['json'])
    
    if uploaded_file is not None:
        try:
            bank_data = json.load(uploaded_file)
            
            # Process transactions
            df = prepare_transaction_data(bank_data['transactions'])
            df['category'] = df['description'].apply(categorize_nano_entrepreneur_transactions)
            
            # Calculate financial metrics
            metrics = calculate_financial_metrics(df, bank_data['summary'])
            
            # Nano Entrepreneur Score
            nano_score = calculate_nano_entrepreneur_score(metrics)
            
            # Generate AI Insights
            ai_insights = generate_ai_insights(df, metrics, nano_score)
            
            # Entrepreneur Profile Section
            st.header("📊 Entrepreneur Profile")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Name:", bank_data['personal_info'].get('customer_id', 'N/A'))
                st.write("Mobile:", bank_data['personal_info'].get('mobile', 'N/A'))
                st.write("KYC Status:", bank_data['personal_info'].get('kyc_status', 'N/A'))
            
            # Nano Entrepreneur Score Section
            with col2:
                st.metric("Nano Entrepreneur Score", f"{nano_score['score']:.2f}/100")
                st.write("Score Breakdown:")
                for category, score in nano_score['breakdown'].items():
                    st.progress(score/40, text=f"{category}: {score:.2f}")
            
            # AI-Powered Insights Section
            st.header("🤖 AI-Powered Financial Insights")
            st.write(ai_insights)
            
            # Account Summary
            st.header("💰 Account Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Opening Balance", 
                         f"₹{float(bank_data['summary']['opening_balance']):,.2f}")
            with col2:
                st.metric("Closing Balance", 
                         f"₹{float(bank_data['summary']['closing_balance']):,.2f}")
            with col3:
                st.metric("Total Credits", f"₹{df['credit'].sum():,.2f}")
            with col4:
                st.metric("Total Debits", f"₹{df['debit'].sum():,.2f}")

            # Visualizations
            st.header("📈 Financial Visualizations")
            
            # Transaction Categories Spending
            spending_by_category = df.groupby('category')['debit'].sum()
            fig_category = px.pie(
                values=spending_by_category.values,
                names=spending_by_category.index,
                title='Spending by Category',
                color=spending_by_category.index,
                color_discrete_map={
                    'BUSINESS_INCOME': 'green',
                    'BUSINESS_EXPENSE': 'red',
                    'PERSONAL_EXPENSE': 'blue',
                    'TRANSFER': 'orange',
                    'OTHERS': 'gray'
                }
            )
            st.plotly_chart(fig_category)
            
            # Income vs Expense Trend
            income = df[df['category'] == 'BUSINESS_INCOME']['credit'].sum()
            expenses = df[df['category'].isin(['BUSINESS_EXPENSE', 'PERSONAL_EXPENSE'])]['debit'].sum()
            
            fig_income_expense = px.bar(
                x=['Income', 'Expenses'],
                y=[income, expenses],
                title='Income vs Expenses Comparison'
            )
            st.plotly_chart(fig_income_expense)
            
            # Detailed Transactions Table
            st.header("📝 Detailed Transactions")
            st.dataframe(df[['date', 'description', 'credit', 'debit', 'balance', 'category']]
                        .sort_values('date', ascending=False))
            
            # Credit Score Improvement Section
            display_credit_score_improvement_section(nano_score['score'], selected_language)
            
            # Future AI-Powered Financial Features
            st.header("🚀 Future AI-Powered Financial Features")
            future_features = {
                "Predictive Cash Flow Forecasting": "Advanced machine learning models to predict future cash flows based on historical transaction patterns.",
                "Automated Expense Categorization": "AI-driven intelligent categorization of expenses with 95%+ accuracy.",
                "Business Growth Recommendations": "Personalized strategies derived from transaction analysis and market trends.",
                "Risk Assessment": "Comprehensive financial risk evaluation using advanced statistical models.",
                "Personalized Financial Coaching": "AI-powered financial advisor providing tailored guidance and improvement strategies."
            }

            for feature, description in future_features.items():
                with st.expander(feature):
                    st.write(description)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()

# Additional dependencies to install:
# pip install streamlit google-generativeai youtube-search-python plotly pandas numpy
