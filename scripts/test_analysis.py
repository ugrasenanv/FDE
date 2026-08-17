#!/usr/bin/env python3
"""Quick test to verify the churn analysis works"""

print("Testing Telco Churn Analysis Pipeline...\n")

# Import libraries
print("1. Importing libraries...")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')
print("   ✓ Libraries imported")

# Load data
print("\n2. Loading dataset...")
df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
print(f"   ✓ Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")

# Basic EDA
print("\n3. Performing EDA...")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
churn_rate = (df['Churn'] == 'Yes').mean() * 100
print(f"   ✓ Churn rate: {churn_rate:.2f}%")
print(f"   ✓ Missing values: {df.isnull().sum().sum()}")

# Split data
print("\n4. Splitting data...")
train_df, test_df = train_test_split(df, test_size=0.3, stratify=df['Churn'], random_state=42)
print(f"   ✓ Train: {len(train_df):,}, Test: {len(test_df):,}")

# Feature engineering
print("\n5. Engineering features...")
train_fe = train_df.copy()
test_fe = test_df.copy()

# Impute
median = train_fe['TotalCharges'].median()
train_fe['TotalCharges'] = train_fe['TotalCharges'].fillna(median)
test_fe['TotalCharges'] = test_fe['TotalCharges'].fillna(median)

# Derived features
train_fe['ChargePerMonth'] = train_fe.apply(lambda x: x['MonthlyCharges'] if x['tenure']==0 else x['TotalCharges']/x['tenure'], axis=1)
test_fe['ChargePerMonth'] = test_fe.apply(lambda x: x['MonthlyCharges'] if x['tenure']==0 else x['TotalCharges']/x['tenure'], axis=1)

services = ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies']
train_fe['NumAddOnServices'] = train_fe[services].apply(lambda x: (x=='Yes').sum(), axis=1)
test_fe['NumAddOnServices'] = test_fe[services].apply(lambda x: (x=='Yes').sum(), axis=1)

train_fe['IsNewCustomer'] = (train_fe['tenure'] < 6).astype(int)
test_fe['IsNewCustomer'] = (test_fe['tenure'] < 6).astype(int)

# Prepare features
y_train = (train_fe['Churn'] == 'Yes').astype(int)
y_test = (test_fe['Churn'] == 'Yes').astype(int)

X_train = train_fe.drop(['customerID','Churn'], axis=1)
X_test = test_fe.drop(['customerID','Churn'], axis=1)

# Encode
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

# Scale
scaler = StandardScaler()
numeric_cols = ['tenure','MonthlyCharges','TotalCharges','ChargePerMonth']
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

print(f"   ✓ Engineered {len(X_train.columns)} features")

# Train baseline
print("\n6. Training baseline model (Logistic Regression)...")
baseline = LogisticRegression(random_state=42, max_iter=1000)
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_test)
baseline_proba = baseline.predict_proba(X_test)[:,1]
baseline_auc = roc_auc_score(y_test, baseline_proba)
print(f"   ✓ Baseline AUC: {baseline_auc:.4f}")

# Train advanced
print("\n7. Training advanced model (Random Forest)...")
advanced = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
advanced.fit(X_train, y_train)
advanced_pred = advanced.predict(X_test)
advanced_proba = advanced.predict_proba(X_test)[:,1]
advanced_auc = roc_auc_score(y_test, advanced_proba)
print(f"   ✓ Advanced AUC: {advanced_auc:.4f}")

# Evaluate
print("\n8. Model evaluation...")
print(f"\n{'='*60}")
print(f"{'RESULTS SUMMARY':^60}")
print(f"{'='*60}")

def eval_model(y_true, y_pred, y_proba, name):
    print(f"\n{name}:")
    print(f"  Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"  Recall:    {recall_score(y_true, y_pred):.4f}")
    print(f"  F1 Score:  {f1_score(y_true, y_pred):.4f}")
    print(f"  AUC-ROC:   {roc_auc_score(y_true, y_proba):.4f}")

eval_model(y_test, baseline_pred, baseline_proba, "Logistic Regression")
eval_model(y_test, advanced_pred, advanced_proba, "Random Forest")

# Business impact
print(f"\n{'='*60}")
print(f"{'BUSINESS IMPACT':^60}")
print(f"{'='*60}")

CLV = 3000
COST = 100
SUCCESS = 0.3

tp = ((y_test==1) & (advanced_pred==1)).sum()
fp = ((y_test==0) & (advanced_pred==1)).sum()
predicted = (advanced_pred==1).sum()

saved = tp * SUCCESS
value = saved * CLV
campaign = predicted * COST
benefit = value - campaign

print(f"\nUsing Random Forest predictions:")
print(f"  Customers at risk (predicted): {predicted}")
print(f"  Correctly identified: {tp}")
print(f"  False alarms: {fp}")
print(f"  Customers saved: {saved:.0f}")
print(f"  Value saved: ${value:,.0f}")
print(f"  Campaign cost: ${campaign:,.0f}")
print(f"  Net benefit: ${benefit:,.0f}")
print(f"  ROI: {(benefit/campaign)*100:.0f}%")

print(f"\n{'='*60}")
print(f"✓ ANALYSIS COMPLETE!")
print(f"{'='*60}")
print(f"\nNext steps:")
print(f"  1. Open telco_churn_analysis.ipynb in Jupyter")
print(f"  2. Run all cells for full analysis with visualizations")
print(f"  3. Review business recommendations")
