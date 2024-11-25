import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the pickled dataset
with open('family_financial_data.pkl', 'rb') as f:
    dataset = pickle.load(f)

# Title of the app
st.title("Family Financial Health Dashboard")
st.markdown("### Insights into Spending Patterns, Correlations, and Financial Health")

# Sidebar for Navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose what you want to explore:", 
                              ("Family Spending Patterns", "Member Spending Patterns", 
                               "Correlations Between Financial Metrics", "Financial Health Score", 
                               "Spending Distribution"))

# 1. Family-Level Spending Patterns
if option == "Family Spending Patterns":
    st.subheader("Family-Level Spending Patterns")
    family_spending = dataset.groupby("Family ID")['Amount'].sum().reset_index()
    st.write(family_spending)
    
    # Bar plot for family spending distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=family_spending, x='Family ID', y='Amount', palette='Set2', ax=ax)
    ax.set_title("Total Family Spending Distribution")
    ax.set_xlabel('Family ID')
    ax.set_ylabel('Total Spending Amount')
    st.pyplot(fig)

# 2. Member-Level Spending Patterns
elif option == "Member Spending Patterns":
    st.subheader("Member-Level Spending Patterns")
    member_spending = dataset.groupby("Member ID")['Amount'].sum().reset_index()
    st.write(member_spending)
    
    # Box plot for member spending trends
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=member_spending, x='Amount', color='lightgreen', ax=ax)
    ax.set_title("Member-wise Spending Distribution")
    ax.set_xlabel('Total Spending Amount')
    st.pyplot(fig)

# 3. Understanding Correlations Between Financial Metrics
elif option == "Correlations Between Financial Metrics":
    st.subheader("Understanding Key Financial Metrics Correlations")
    
    # Income vs Expenses Correlation
    corr_income_expenses = dataset['Income'].corr(dataset['Monthly Expenses'])
    st.write(f"Correlation between Income and Monthly Expenses: {corr_income_expenses:.2f}")
    
    # Savings vs Credit Card Spending Correlation
    corr_savings_spending = dataset['Savings'].corr(dataset['Credit Card Spending'])
    st.write(f"Correlation between Savings and Credit Card Spending: {corr_savings_spending:.2f}")
    
    # Scatter plot for Income vs Expenses
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=dataset, x='Income', y='Monthly Expenses', ax=ax, color='orange')
    ax.set_title("Income vs Monthly Expenses")
    ax.set_xlabel('Income')
    ax.set_ylabel('Monthly Expenses')
    st.pyplot(fig)

# 4. Financial Health Score (Scoring Mechanism)
elif option == "Financial Health Score":
    st.subheader("Family Financial Health Score")

    # Scoring function (same as before)
    def calculate_financial_health(row):
        savings_to_income = row["Savings"] / row["Income"]
        expenses_to_income = row["Monthly Expenses"] / row["Income"]
        loan_to_income = row["Loan Payments"] / row["Income"]
        credit_card_spending_ratio = row["Credit Card Spending"] / row["Income"]
        category_spending_ratio = row["Travel/Entertainment Spending"] / row["Monthly Expenses"]
        financial_goals_met = row["Financial Goals Met (%)"] / 100

        score = (savings_to_income * 0.2) + (1 - expenses_to_income * 0.2) + (1 - loan_to_income * 0.2) \
                + (1 - credit_card_spending_ratio * 0.1) + (1 - category_spending_ratio * 0.1) + (financial_goals_met * 0.2)
        return score * 100

    # Apply the scoring function
    dataset['Financial Health Score'] = dataset.apply(calculate_financial_health, axis=1)
    family_scores = dataset.groupby('Family ID')['Financial Health Score'].max().reset_index()
    st.write(family_scores)

    # Justification for scoring logic and weights
    st.markdown("""
    ### Scoring Mechanism Explanation:
    The **Financial Health Score** is calculated using the following factors:
    - **Savings-to-Income Ratio (20%)**: A higher ratio is considered better.
    - **Monthly Expenses as a percentage of Income (20%)**: Lower expenses as a percentage of income are considered better.
    - **Loan Payments as a percentage of Income (20%)**: Lower loan payments are considered better.
    - **Credit Card Spending trends (10%)**: Less credit card spending indicates better financial health.
    - **Travel/Entertainment Spending ratio (10%)**: Higher spending on non-essential categories lowers the score.
    - **Financial Goals Met (%) (20%)**: Meeting financial goals contributes positively to the score.
    
    All these factors are weighted to give a final score ranging from 0 to 100, where a higher score indicates better financial health.
    """)
    
    # Plotting the financial health scores distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(family_scores['Financial Health Score'], bins=10, kde=True, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Distribution of Family Financial Health Scores")
    ax.set_xlabel('Financial Health Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# 5. Spending Distribution Across Categories
elif option == "Spending Distribution":
    st.subheader("Spending Distribution Across Categories")
    category_spending = dataset.groupby('Category')['Amount'].sum().reset_index()
    
    # Pie chart using Plotly
    fig = px.pie(category_spending, names='Category', values='Amount', title='Spending Distribution by Category')
    st.plotly_chart(fig)

# Footer message
st.markdown("##### Powered by Sahid Ahamad | Family Financial Dashboard")
