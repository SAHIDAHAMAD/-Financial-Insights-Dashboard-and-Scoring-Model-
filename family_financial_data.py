import pandas as pd
import numpy as np

dataset = pd.read_excel(r"C:\Assignment 2\family_financial_and_transactions_data.xlsx")

# Family - level spending pattern
family_spending = dataset.groupby("Family ID")['Amount'].sum()
print("family-level-spending :",family_spending)

#  member-level spending patterns. 
member_lavel = dataset.groupby("Member ID")['Amount'].sum()
print("member-lavel-spending :",member_lavel)

# Income vs Expenses

corr_income_expenses = dataset['Income'].corr(dataset['Monthly Expenses'])
print("corr_income_expenses :",corr_income_expenses)

# Savings vs spending habits

corr_savings_spending = dataset['Savings'].corr(dataset['Credit Card Spending'])
print("corr_savings_spending :",corr_savings_spending)

# Create a new column to calculate Travel/Entertainment Spending (you can change category as needed)
dataset['Travel/Entertainment Spending'] = dataset['Category'].apply(lambda x: dataset.loc[dataset['Category'] == x, 'Amount'].sum() if x in ['Travel', 'Entertainment'] else 0)

# Scoring function
def calculate_financial_health(row):
    # Factor 1: Savings-to-Income Ratio
    savings_to_income = row["Savings"] / row["Income"]
    
    # Factor 2: Monthly Expenses as a percentage of Income
    expenses_to_income = row["Monthly Expenses"] / row["Income"]
    
    # Factor 3: Loan Payments as a percentage of Income
    loan_to_income = row["Loan Payments"] / row["Income"]
    
    # Factor 4: Credit Card Spending trends (lower is better)
    credit_card_spending_ratio = row["Credit Card Spending"] / row["Income"]
    
    # Factor 5: Spending category distribution (higher travel/entertainment lowers score)
    category_spending_ratio = row["Travel/Entertainment Spending"] / row["Monthly Expenses"]
    
    # Factor 6: Financial Goals Met
    financial_goals_met = row["Financial Goals Met (%)"] / 100  # Convert to 0-1 scale

    # Weighted scoring (weights sum to 1)
    score = (savings_to_income * 0.2) + (1 - expenses_to_income * 0.2) + (1 - loan_to_income * 0.2) \
            + (1 - credit_card_spending_ratio * 0.1) + (1 - category_spending_ratio * 0.1) + (financial_goals_met * 0.2)
    
    # Convert to scale of 0-100
    return score * 100

# Apply the scoring function
dataset['Financial Health Score'] = dataset.apply(calculate_financial_health, axis=1)

# Display the results
print(dataset[['Family ID', 'Financial Health Score']])

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. Spending distribution across categories
category_spending = dataset.groupby('Category')['Amount'].sum().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(data=category_spending, x='Category', y='Amount', palette='Set2')
plt.title('Spending Distribution Across Categories')
plt.xlabel('Category')
plt.ylabel('Amount Spent')
plt.xticks(rotation=45)
plt.show()

# Grouping by Family ID and calculating maximum Financial Health Score
family_scores = dataset.groupby('Family ID')['Financial Health Score'].max().reset_index()

# Creating a histogram to show the distribution of family financial health scores
plt.figure(figsize=(10,6))
sns.histplot(family_scores['Financial Health Score'], bins=10, kde=True, color='skyblue', edgecolor='black')

# Enhancing the visualization with title and labels
plt.title('Distribution of Family-wise Financial Health Scores', fontsize=16)
plt.xlabel('Financial Health Score', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the plot
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Grouping by Member ID and calculating total spending
member_spending = dataset.groupby('Member ID')['Amount'].sum().reset_index()

# Creating a boxplot to show the distribution of member spending
plt.figure(figsize=(10,6))
sns.boxplot(data=member_spending, x='Amount', color='lightgreen')

# Enhancing the visualization with title and labels
plt.title('Member-wise Spending Distribution', fontsize=16)
plt.xlabel('Total Spending Amount', fontsize=14)
plt.ylabel('Member ID', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display the plot
plt.show()


# 4. (Optional) A Plotly pie chart to visualize spending distribution across categories
fig = px.pie(category_spending, names='Category', values='Amount', title='Spending Distribution by Category')
fig.show()

import pickle
# Pickle the file
with open('family_financial_data.pkl', 'wb') as f:
    pickle.dump(dataset, f)

print("Dataset has been pickled successfully.")