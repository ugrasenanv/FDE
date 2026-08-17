#!/usr/bin/env python3
"""
Script to create the Telco Churn Analysis Jupyter Notebook
Run this to generate: telco_churn_analysis.ipynb
"""

import json

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Helper to add markdown cell
def add_markdown(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [text]
    })

# Helper to add code cell
def add_code(code):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [code]
    })

# Title
add_markdown("""# Telco Customer Churn Prediction Analysis

## Table of Contents
1. [Introduction](#intro)
2. [Setup](#setup)
3. [EDA](#eda)
4. [Data Split](#split)
5. [Feature Engineering](#features)
6. [Baseline Model](#baseline)
7. [Advanced Model](#advanced)
8. [Evaluation](#eval)
9. [Business Insights](#business)
10. [Summary](#summary)""")

# Introduction
add_markdown("""## 1. Introduction <a name="intro"></a>

Predict customer churn for a telecom company using machine learning.

**Dataset:** Download from https://www.kaggle.com/datasets/blastchar/telco-customer-churn
Place as: `WA_Fn-UseC_-Telco-Customer-Churn.csv`""")

# Setup
add_markdown("## 2. Setup <a name=\"setup\"></a>")

add_code("""# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import *
import warnings
import time

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
RANDOM_STATE = 42
print("✓ Libraries imported")""")

add_code("""# Load dataset
try:
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    print(f"✓ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    display(df.head())
except FileNotFoundError:
    print("❌ Dataset not found!")
    print("Download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
    raise""")

# EDA
add_markdown("## 3. Exploratory Data Analysis <a name=\"eda\"></a>")

add_code("""# Summary statistics
print("NUMERIC FEATURES SUMMARY")
print("="*70)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
display(df[numeric_cols].describe())""")

add_code("""# Missing values
print("\\nMISSING VALUES")
print("="*70)
missing = df.isnull().sum()
if missing.sum() > 0:
    display(missing[missing > 0])
else:
    print("✓ No missing values")""")

add_code("""# Churn rate
print("\\nCHURN RATE ANALYSIS")
print("="*70)
churn_rate = (df['Churn'] == 'Yes').mean() * 100
print(f"Total: {len(df):,} customers")
print(f"Churn rate: {churn_rate:.2f}%")
print(f"Churned: {(df['Churn']=='Yes').sum():,}")
print(f"Retained: {(df['Churn']=='No').sum():,}")""")

add_code("""# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Churn distribution
df['Churn'].value_counts().plot(kind='bar', ax=axes[0,0], color=['green','red'])
axes[0,0].set_title('Churn Distribution')

# Tenure
df['tenure'].hist(bins=30, ax=axes[0,1], color='steelblue')
axes[0,1].set_title('Tenure Distribution')

# Monthly charges
df['MonthlyCharges'].hist(bins=30, ax=axes[1,0], color='coral')
axes[1,0].set_title('Monthly Charges')

# Tenure vs Churn
df.boxplot(column='tenure', by='Churn', ax=axes[1,1])
axes[1,1].set_title('Tenure by Churn')
plt.suptitle('')

plt.tight_layout()
plt.show()
print("✓ Visualizations complete")""")

# Data Split
add_markdown("## 4. Data Splitting <a name=\"split\"></a>")

add_code("""# Train-test split
train_df, test_df = train_test_split(df, test_size=0.3, stratify=df['Churn'], random_state=RANDOM_STATE)

print("DATA SPLIT")
print("="*70)
print(f"Train: {len(train_df):,} (70%)")
print(f"Test: {len(test_df):,} (30%)")
print(f"\\nChurn rates:")
print(f"  Train: {(train_df['Churn']=='Yes').mean()*100:.2f}%")
print(f"  Test: {(test_df['Churn']=='Yes').mean()*100:.2f}%")
print("✓ Split complete")""")

# Feature Engineering
add_markdown("""## 5. Feature Engineering <a name=\"features\"></a>

**Transformations:**
1. Missing value imputation (TotalCharges)
2. Derived features (ChargePerMonth, NumAddOnServices, IsNewCustomer)
3. Categorical encoding
4. Numeric scaling""")

add_code("""# Feature engineering
train_fe = train_df.copy()
test_fe = test_df.copy()

# Impute TotalCharges
median_total = train_fe['TotalCharges'].median()
train_fe['TotalCharges'] = train_fe['TotalCharges'].fillna(median_total)
test_fe['TotalCharges'] = test_fe['TotalCharges'].fillna(median_total)

# Derived features
train_fe['ChargePerMonth'] = train_fe.apply(lambda x: x['MonthlyCharges'] if x['tenure']==0 else x['TotalCharges']/x['tenure'], axis=1)
test_fe['ChargePerMonth'] = test_fe.apply(lambda x: x['MonthlyCharges'] if x['tenure']==0 else x['TotalCharges']/x['tenure'], axis=1)

services = ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies']
train_fe['NumAddOnServices'] = train_fe[services].apply(lambda x: (x=='Yes').sum(), axis=1)
test_fe['NumAddOnServices'] = test_fe[services].apply(lambda x: (x=='Yes').sum(), axis=1)

train_fe['IsNewCustomer'] = (train_fe['tenure'] < 6).astype(int)
test_fe['IsNewCustomer'] = (test_fe['tenure'] < 6).astype(int)

# Separate target
y_train = (train_fe['Churn'] == 'Yes').astype(int)
y_test = (test_fe['Churn'] == 'Yes').astype(int)

X_train = train_fe.drop(['customerID','Churn'], axis=1)
X_test = test_fe.drop(['customerID','Churn'], axis=1)

# Encode categorical
binary_cols = ['gender','Partner','Dependents','PhoneService','PaperlessBilling',
               'MultipleLines','OnlineSecurity','OnlineBackup','DeviceProtection',
               'TechSupport','StreamingTV','StreamingMovies']

for col in binary_cols:
    if col in X_train.columns:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col])
        X_test[col] = le.transform(X_test[col])

X_train = pd.get_dummies(X_train, columns=['InternetService','Contract','PaymentMethod'], drop_first=True)
X_test = pd.get_dummies(X_test, columns=['InternetService','Contract','PaymentMethod'], drop_first=True)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# Scale numeric
scaler = StandardScaler()
numeric_cols = ['tenure','MonthlyCharges','TotalCharges','ChargePerMonth']
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

print("FEATURE ENGINEERING COMPLETE")
print("="*70)
print(f"Features: {len(X_train.columns)}")
print(f"Train: {X_train.shape}")
print(f"Test: {X_test.shape}")""")

# Baseline Model
add_markdown("## 6. Baseline Model: Logistic Regression <a name=\"baseline\"></a>")

add_code("""# Train baseline model
start = time.time()
baseline = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
baseline.fit(X_train, y_train)
baseline_time = time.time() - start

baseline_pred = baseline.predict(X_test)
baseline_proba = baseline.predict_proba(X_test)[:,1]

print("BASELINE MODEL: LOGISTIC REGRESSION")
print("="*70)
print(f"Training time: {baseline_time:.2f}s")
print(f"Predictions: {len(baseline_pred):,}")

# Top coefficients
coeffs = pd.DataFrame({'Feature': X_train.columns, 'Coef': baseline.coef_[0]})
coeffs = coeffs.reindex(coeffs['Coef'].abs().sort_values(ascending=False).index)
print(f"\\nTop 10 Coefficients:")
display(coeffs.head(10))""")

# Advanced Model
add_markdown("## 7. Advanced Model: Random Forest <a name=\"advanced\"></a>")

add_code("""# Train advanced model with tuning
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}

rf = RandomForestClassifier(random_state=RANDOM_STATE)
grid = GridSearchCV(rf, param_grid, cv=3, scoring='roc_auc', n_jobs=-1)

start = time.time()
grid.fit(X_train, y_train)
advanced_time = time.time() - start

advanced = grid.best_estimator_
advanced_pred = advanced.predict(X_test)
advanced_proba = advanced.predict_proba(X_test)[:,1]

print("ADVANCED MODEL: RANDOM FOREST")
print("="*70)
print(f"Training time: {advanced_time:.2f}s")
print(f"Best params: {grid.best_params_}")
print(f"Best CV AUC: {grid.best_score_:.4f}")

# Feature importance
importance = pd.DataFrame({'Feature': X_train.columns, 'Importance': advanced.feature_importances_})
importance = importance.sort_values('Importance', ascending=False)
print(f"\\nTop 10 Important Features:")
display(importance.head(10))

plt.figure(figsize=(10,6))
plt.barh(importance.head(10)['Feature'], importance.head(10)['Importance'])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()""")

# Evaluation
add_markdown("## 8. Model Evaluation <a name=\"eval\"></a>")

add_code("""# Evaluate models
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve

def eval_model(y_true, y_pred, y_proba, name):
    return {
        'Model': name,
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred),
        'Recall': recall_score(y_true, y_pred),
        'F1': f1_score(y_true, y_pred),
        'AUC': roc_auc_score(y_true, y_proba)
    }

baseline_metrics = eval_model(y_test, baseline_pred, baseline_proba, 'Logistic Regression')
advanced_metrics = eval_model(y_test, advanced_pred, advanced_proba, 'Random Forest')

comparison = pd.DataFrame([baseline_metrics, advanced_metrics]).set_index('Model')

print("MODEL COMPARISON")
print("="*70)
display(comparison)""")

add_code("""# Confusion matrices
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

cm1 = confusion_matrix(y_test, baseline_pred)
cm2 = confusion_matrix(y_test, advanced_pred)

sns.heatmap(cm1, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Logistic Regression')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

sns.heatmap(cm2, annot=True, fmt='d', cmap='Greens', ax=axes[1])
axes[1].set_title('Random Forest')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

plt.tight_layout()
plt.show()

# ROC curves
fpr1, tpr1, _ = roc_curve(y_test, baseline_proba)
fpr2, tpr2, _ = roc_curve(y_test, advanced_proba)

plt.figure(figsize=(10,6))
plt.plot(fpr1, tpr1, label=f'Logistic Regression (AUC={baseline_metrics["AUC"]:.3f})', linewidth=2)
plt.plot(fpr2, tpr2, label=f'Random Forest (AUC={advanced_metrics["AUC"]:.3f})', linewidth=2)
plt.plot([0,1], [0,1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves')
plt.legend()
plt.grid(alpha=0.3)
plt.show()""")

# Business Insights
add_markdown("## 9. Business Interpretation <a name=\"business\"></a>")

add_code("""# Business impact
CLV = 3000  # Customer lifetime value
CAMPAIGN_COST = 100
SUCCESS_RATE = 0.3

actual_churners = (y_test == 1).sum()
predicted_churners = (advanced_pred == 1).sum()
tp = ((y_test==1) & (advanced_pred==1)).sum()
fp = ((y_test==0) & (advanced_pred==1)).sum()
fn = ((y_test==1) & (advanced_pred==0)).sum()

customers_saved = tp * SUCCESS_RATE
value_saved = customers_saved * CLV
campaign_cost = predicted_churners * CAMPAIGN_COST
net_benefit = value_saved - campaign_cost
roi = (net_benefit / campaign_cost) * 100

print("BUSINESS IMPACT")
print("="*70)
print(f"\\nAssumptions:")
print(f"  CLV: ${CLV:,}")
print(f"  Campaign cost: ${CAMPAIGN_COST}")
print(f"  Success rate: {SUCCESS_RATE*100:.0f}%")
print(f"\\nResults:")
print(f"  Actual churners: {actual_churners}")
print(f"  Predicted churners: {predicted_churners}")
print(f"  Correctly identified: {tp} ({tp/actual_churners*100:.1f}%)")
print(f"  False alarms: {fp}")
print(f"  Missed: {fn}")
print(f"\\n  Customers saved: {customers_saved:.0f}")
print(f"  Value saved: ${value_saved:,.0f}")
print(f"  Campaign cost: ${campaign_cost:,.0f}")
print(f"  Net benefit: ${net_benefit:,.0f}")
print(f"  ROI: {roi:.1f}%")""")

# Summary
add_markdown("## 10. Summary <a name=\"summary\"></a>")

add_code("""print("="*70)
print("SUMMARY AND RECOMMENDATIONS")
print("="*70)

print(f"\\n📊 KEY FINDINGS:")
print(f"\\n1. Model Performance:")
print(f"   • Random Forest: {advanced_metrics['AUC']:.1%} AUC")
print(f"   • Logistic Regression: {baseline_metrics['AUC']:.1%} AUC")
print(f"   • Improvement: {(advanced_metrics['AUC']-baseline_metrics['AUC'])*100:.1f}%")

print(f"\\n2. Top Churn Drivers:")
for idx, row in importance.head(5).iterrows():
    print(f"   • {row['Feature']}")

print(f"\\n3. Business Value:")
print(f"   • Net benefit: ${net_benefit:,.0f}")
print(f"   • ROI: {roi:.0f}%")
print(f"   • {tp} churners correctly identified")

print(f"\\n💡 RECOMMENDATIONS:")
print(f"\\n1. Deploy Random Forest model")
print(f"2. Target customers with tenure < 12 months")
print(f"3. Promote long-term contracts")
print(f"4. Increase add-on service adoption")
print(f"5. A/B test retention campaigns")

print(f"\\n✓ Analysis complete!")""")

# Save notebook
with open('telco_churn_analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("✓ Notebook created: telco_churn_analysis.ipynb")
