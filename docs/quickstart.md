# Quick Start Guide

Get started with DeepBridge experimental validation in 15 minutes.

## ⚡ Prerequisites

- Python 3.8 or higher
- pip or conda
- Git (for cloning repository)
- DeepBridge library (from `/home/guhaase/projetos/DeepBridge/deepbridge`)

## 📥 Installation

### Step 1: Install DeepBridge

```bash
# Navigate to DeepBridge source
cd /home/guhaase/projetos/DeepBridge/deepbridge

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Step 2: Install Experiment Dependencies

```bash
# Navigate to this repository
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install experiment dependencies
pip install -r requirements.txt
```

### Option 2: conda

```bash
# Clone repository
git clone https://github.com/username/fairness-framework.git
cd fairness-framework

# Create conda environment
conda env create -f environment.yml
conda activate fairness-framework
```

### Option 3: Docker

```bash
# Clone and build
git clone https://github.com/username/fairness-framework.git
cd fairness-framework
docker build -t fairness-framework -f docker/Dockerfile .

# Run
docker run -it fairness-framework
```

## 🎯 First Example (5 minutes)

### 1. Import DeepBridge

```python
from deepbridge import DBDataset
import pandas as pd
```

### 2. Load Sample Data

```python
# Load one of the case study datasets
df = pd.read_csv("data/case_studies/adult/adult.csv")

# Or create a simple example
data = {
    'age': [25, 45, 35, 50, 28],
    'income': [50000, 80000, 60000, 95000, 45000],
    'gender': ['M', 'F', 'M', 'F', 'M'],
    'race': ['White', 'Black', 'Asian', 'White', 'Hispanic'],
    'approved': [1, 0, 1, 1, 0]
}
df = pd.DataFrame(data)
```

### 3. Create DBDataset (Auto-detects Sensitive Attributes)

```python
# Create dataset - DeepBridge automatically detects sensitive attributes
dataset = DBDataset(
    data=df,
    target_column='approved'
)

# Check what was detected
print(f"Detected sensitive attributes: {dataset.detected_sensitive_attributes}")
print(f"Target column: {dataset.target_column}")
```

### 4. Analyze Fairness

```python
# Run fairness analysis
results = dataset.analyze_fairness()

# Print results
print(results)
```

## 📊 Run Demo Notebook

```bash
# Start Jupyter
jupyter notebook

# Open: experiments/notebooks/01_quick_demo.ipynb
```

Or use Docker:

```bash
docker-compose -f docker/docker-compose.yml up
# Access: http://localhost:8888
```

## 🧪 Run Sample Experiment

```bash
# Quick test (< 5 minutes)
cd experiments/scripts
python exp1_detection.py --quick-test --n-datasets 10

# Full experiment (~ 1 hour)
python exp1_detection.py --n-datasets 100
```

## 🔍 Verify Installation

```bash
# Run tests
pytest tests/ -v

# Check Python imports
python -c "from src.fairness_detector import FairnessDetector; print('OK')"

# Run verification script
python scripts/verify_installation.py
```

## 📖 Common Use Cases

### Use Case 1: Check Demographic Parity

```python
from src.metrics import demographic_parity

# Compute demographic parity difference
dp = demographic_parity(
    y_true=df['target'],
    y_pred=predictions,
    sensitive=df['sensitive_attr']
)

print(f"Demographic Parity Difference: {dp:.3f}")
# Threshold: |dp| > 0.1 indicates potential bias
```

### Use Case 2: Check Equal Opportunity

```python
from src.metrics import equal_opportunity_difference

# Compute equal opportunity difference
eod = equal_opportunity_difference(
    y_true=df['target'],
    y_pred=predictions,
    sensitive=df['sensitive_attr']
)

print(f"Equal Opportunity Difference: {eod:.3f}")
```

### Use Case 3: Generate Full Report

```python
# Run all fairness checks
detector = FairnessDetector()
detector.load_data(df, target='target', sensitive=['race', 'sex'])

# Full analysis
report = detector.analyze()

# Export
report.to_html("full_fairness_report.html")
report.to_pdf("full_fairness_report.pdf")
```

## 🎓 Next Steps

Now that you have the basics:

1. **Learn the API**: See [API Reference](api/index.md)
2. **Explore Experiments**: Check [experiments/](experiments/overview.md)
3. **Read the Paper**: See [paper/english/main.pdf](../paper/english/main.pdf)
4. **Try Case Studies**: Explore [data/case_studies/](../data/case_studies/)

## 🐛 Troubleshooting

### Import Errors

```bash
# Ensure you're in the right directory
cd /path/to/fairness-framework

# Check Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Or in Python:
import sys
sys.path.append('/path/to/fairness-framework')
```

### Data Not Found

```bash
# Generate synthetic data
python scripts/generate_synthetic_data.py --count 50

# Download case studies
bash scripts/download_case_studies.sh
```

### Dependencies Issues

```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

For more issues, see [Troubleshooting Guide](troubleshooting.md).

## 💡 Tips

- **Start small**: Test with 10-50 datasets before running full experiments
- **Use notebooks**: Jupyter notebooks in `experiments/notebooks/` are interactive
- **Check examples**: See `examples/` directory for more code samples
- **Read logs**: Enable verbose mode: `detector.set_verbose(True)`

## 📚 Additional Resources

- [Installation Guide](installation.md): Detailed installation
- [Experiments Overview](experiments/overview.md): Methodology
- [FAQ](faq.md): Common questions
- [CONTRIBUTING.md](../CONTRIBUTING.md): How to contribute

## 📧 Get Help

- **Issues**: [GitHub Issues](https://github.com/username/fairness-framework/issues)
- **Email**: your-email@domain.com
- **Paper**: See `paper/english/main.pdf` for theoretical background

---

**Estimated time**: 15 minutes for installation + first example

Ready to detect bias? Let's go! 🚀
