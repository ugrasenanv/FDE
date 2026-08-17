# Setup Guide

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Git**: For cloning the repository
- **Jupyter**: For running notebooks (included in requirements.txt)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ugrasenanv/FDE-assessment.git
cd FDE-assessment
```

### 2. Create Virtual Environment (Recommended)

**Using venv:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n churn-pred python=3.8
conda activate churn-pred
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- scikit-learn >= 1.0.0
- jupyter >= 1.0.0

### 4. Download Dataset

The dataset is already included in `data/` folder. If you need to re-download:

1. Go to [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
2. Click "Download"
3. Extract and place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/` folder

**Or using Kaggle API:**
```bash
pip install kaggle
kaggle datasets download -d blastchar/telco-customer-churn
unzip telco-customer-churn.zip
mv WA_Fn-UseC_-Telco-Customer-Churn.csv data/
```

### 5. Verify Installation

```bash
python scripts/test_analysis.py
```

**Expected output:**
```
Testing Telco Churn Analysis Pipeline...
1. Importing libraries...
   ✓ Libraries imported
2. Loading dataset...
   ✓ Loaded 7,043 rows × 21 columns
...
✓ ANALYSIS COMPLETE!
```

## Running the Analysis

### Option 1: Jupyter Notebook (Recommended)

```bash
jupyter notebook telco_churn_analysis.ipynb
```

**Features:**
- Interactive cells
- Visualizations
- Detailed explanations
- Business insights

### Option 2: Command Line Script

```bash
python scripts/test_analysis.py
```

**Benefits:**
- Quick execution (~30 seconds)
- Complete analysis
- Results in terminal

### Option 3: Validate Notebook

```bash
python scripts/validate_notebook.py
```

**Purpose:**
- Verify notebook structure
- Check all sections present
- Validate code cells

## Project Structure

```
FDE-assessment/
├── data/                    # Dataset folder
│   └── WA_Fn-UseC_-...csv  # Telco churn dataset
├── docs/                    # Documentation
│   ├── RESULTS_SUMMARY.md
│   ├── PROJECT_STATUS.md
│   └── ...
├── scripts/                 # Utility scripts
│   ├── test_analysis.py
│   ├── create_notebook.py
│   └── validate_notebook.py
├── telco_churn_analysis.ipynb  # Main notebook
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Troubleshooting

### Issue: Module not found

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Dataset not found

**Error:** `FileNotFoundError: data/WA_Fn-UseC_-Telco-Customer-Churn.csv`

**Solution:**
- Verify file is in `data/` folder
- Check file name matches exactly
- Re-download from Kaggle if needed

### Issue: Jupyter not launching

**Solution:**
```bash
pip install jupyter notebook
jupyter notebook
```

### Issue: ImportError for sklearn

**Solution:**
```bash
pip install --upgrade scikit-learn
```

### Issue: Plots not showing in Jupyter

**Solution:** Add this to first cell:
```python
%matplotlib inline
```

## Development

### Running Tests

```bash
# Run quick analysis
python scripts/test_analysis.py

# Validate notebook structure
python scripts/validate_notebook.py

# Regenerate notebook
python scripts/create_notebook.py
```

### Modifying the Analysis

1. Open `telco_churn_analysis.ipynb`
2. Make changes to cells
3. Run all cells: `Kernel > Restart & Run All`
4. Save changes

### Adding New Features

1. Modify feature engineering section
2. Retrain models
3. Update documentation
4. Test end-to-end

## Environment Variables

No environment variables required for basic usage.

## System Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 4 GB
- Storage: 1 GB free space

**Recommended:**
- CPU: Quad-core processor
- RAM: 8 GB
- Storage: 2 GB free space

## Performance

- **Dataset loading:** < 1 second
- **EDA:** 2-3 seconds
- **Feature engineering:** 1-2 seconds
- **Logistic Regression training:** < 1 second
- **Random Forest training:** 20-30 seconds
- **Total execution:** ~30-40 seconds

## Getting Help

- **Issues:** Open an issue on GitHub
- **Questions:** Check `docs/` folder for detailed documentation

## Next Steps

After successful setup:

1. Run the Jupyter notebook
2. Review `docs/RESULTS_SUMMARY.md` for analysis results
3. Check `docs/PROJECT_STATUS.md` for task completion
4. Explore different hyperparameters
5. Try additional features

---

**Need help?** Open an issue on GitHub or refer to the documentation in `docs/` folder.
