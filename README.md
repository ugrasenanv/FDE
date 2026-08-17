# FDE Assessment - Telco Customer Churn Prediction

Machine learning project predicting customer churn for telecommunications companies using Logistic Regression and Random Forest models.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-green.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📊 Project Overview

This project analyzes customer churn patterns in a telecommunications dataset and builds predictive models to identify at-risk customers. The analysis includes comprehensive EDA, feature engineering, model comparison, and business impact assessment.

**Key Results:**
- **Best Model**: Logistic Regression (AUC: 0.8497, Accuracy: 80.97%)
- **Business Impact**: $235,100 net benefit, 575% ROI
- **Churn Rate**: 26.54% of customers
- **At-Risk Customers Identified**: 305 correctly predicted

## 🗂️ Repository Structure

```
FDE-assessment/
│
├── data/                                      # Dataset
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── docs/                                      # Documentation
│   ├── RESULTS_SUMMARY.md                     # Detailed results and recommendations
│   ├── PROJECT_STATUS.md                      # Task completion tracking
│   ├── TASK_COMPLETION_EVIDENCE.md            # Evidence of completed tasks
│   └── PROGRAM_EXECUTION_VERIFIED.md          # Execution verification
│
├── scripts/                                   # Utility scripts
│   ├── test_analysis.py                       # Quick command-line analysis
│   ├── create_notebook.py                     # Regenerate Jupyter notebook
│   └── validate_notebook.py                   # Validate notebook structure
│
├── telco_churn_analysis.ipynb                # Main Jupyter notebook
├── README.md                                  # This file
├── .gitignore                                 # Git ignore rules
└── requirements.txt                           # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ugrasenanv/FDE-assessment.git
cd FDE-assessment
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download dataset** (if not included)
- Download from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/` folder

### Usage

#### Option 1: Quick Analysis (Command Line)
```bash
python scripts/test_analysis.py
```
**Output:** Complete analysis with results in ~30 seconds

#### Option 2: Interactive Notebook (Recommended)
```bash
jupyter notebook telco_churn_analysis.ipynb
```
**Features:** 
- Step-by-step analysis
- Interactive visualizations
- Detailed explanations
- Business insights

#### Option 3: Validate Notebook
```bash
python scripts/validate_notebook.py
```

## 📈 Analysis Workflow

### 1. Exploratory Data Analysis
- Dataset: 7,043 customers × 21 features
- Churn rate: 26.54%
- Key findings: Contract type and tenure are strongest predictors

### 2. Feature Engineering
- **Derived Features:**
  - `ChargePerMonth`: Normalized spending
  - `NumAddOnServices`: Engagement indicator
  - `IsNewCustomer`: High-risk segment flag
- **Transformations:**
  - Missing value imputation (median)
  - Label encoding for binary features
  - One-hot encoding for multi-class features
  - Standard scaling for numeric features

### 3. Model Development

**Baseline Model: Logistic Regression**
- Fast training (<1 second)
- Highly interpretable
- AUC: 0.8497 ⭐

**Advanced Model: Random Forest**
- Hyperparameter tuned (GridSearchCV)
- Feature importance scores
- AUC: 0.8189

### 4. Model Evaluation

| Metric | Logistic Regression | Random Forest |
|--------|---------------------|---------------|
| AUC-ROC | **0.8497** | 0.8189 |
| Accuracy | **80.97%** | 78.66% |
| Precision | **67.63%** | 62.56% |
| Recall | **54.37%** | 48.84% |
| F1 Score | **60.28%** | 54.85% |

**Winner:** Logistic Regression (simpler model performs better!)

### 5. Business Interpretation

**Top Churn Drivers:**
1. Contract type (month-to-month = high risk)
2. Customer tenure (< 12 months = high risk)
3. Monthly charges (price sensitivity)
4. Service engagement (more services = lower churn)
5. Internet service type

**Financial Impact:**
- Customers at risk: 409 flagged
- Correctly identified: 305 churners
- Expected saves: 92 customers
- Value saved: $276,000
- Campaign cost: $40,900
- **Net benefit: $235,100**
- **ROI: 575%**

## 💡 Key Features

- ✅ **Complete ML Pipeline**: Data loading → EDA → Feature engineering → Modeling → Evaluation
- ✅ **Two Models Compared**: Baseline (Logistic) vs Advanced (Random Forest)
- ✅ **Justified Transformations**: Every feature engineering step documented
- ✅ **Business Focus**: ROI calculation and actionable recommendations
- ✅ **Production Ready**: Clean code, no data leakage, reproducible results
- ✅ **Well Documented**: Comprehensive docs and inline comments

## 📊 Visualizations

The Jupyter notebook includes:
- Churn distribution charts
- Feature distributions by churn status
- Correlation heatmaps
- Confusion matrices
- ROC curves
- Feature importance plots

## 🎯 Business Recommendations

### Immediate Actions:
1. **Target new customers** (< 12 months) with enhanced onboarding
2. **Incentivize contract upgrades** from month-to-month to annual
3. **Promote add-on services** to increase engagement
4. **Deploy retention campaigns** for predicted at-risk customers

## 📚 Documentation

Detailed documentation available in `docs/`:

- **[RESULTS_SUMMARY.md](docs/RESULTS_SUMMARY.md)** - Complete analysis results and business recommendations
- **[PROJECT_STATUS.md](docs/PROJECT_STATUS.md)** - Task tracking and deliverables
- **[TASK_COMPLETION_EVIDENCE.md](docs/TASK_COMPLETION_EVIDENCE.md)** - Proof of task completion
- **[PROGRAM_EXECUTION_VERIFIED.md](docs/PROGRAM_EXECUTION_VERIFIED.md)** - Execution verification

## 🛠️ Technical Details

**Libraries Used:**
- pandas, numpy - Data manipulation
- matplotlib, seaborn - Visualization
- scikit-learn - Machine learning

**Models:**
- Logistic Regression (baseline)
- Random Forest with GridSearchCV (advanced)

**Evaluation Metrics:**
- Accuracy, Precision, Recall, F1 Score, AUC-ROC
- Confusion matrices
- ROC curves

## 📄 Dataset

**Source:** [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

**Features:**
- Customer demographics (gender, age, dependents)
- Service subscriptions (phone, internet, add-ons)
- Account information (tenure, contract, payment method)
- Billing (monthly charges, total charges)
- Target: Churn (Yes/No)

**Size:** 7,043 customers × 21 features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Vellaichamy Ugrasenan**
- GitHub: [@ugrasenanv](https://github.com/ugrasenanv)
- LinkedIn: [vellaichamy](https://www.linkedin.com/in/vellaichamy/)
- Portfolio: [vellaichamy.vercel.app](https://vellaichamy.vercel.app/)

