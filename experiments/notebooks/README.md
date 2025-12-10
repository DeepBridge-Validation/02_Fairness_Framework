# DeepBridge Demonstration Notebooks

This directory contains Jupyter notebooks demonstrating the use of DeepBridge for fairness analysis.

## 📓 Available Notebooks

### 1. [01_quickstart_deepbridge.ipynb](01_quickstart_deepbridge.ipynb)
**Duration**: 5-10 minutes

**What it covers**:
- Basic DeepBridge usage
- Creating DBDataset
- Auto-detection of sensitive attributes
- Simple fairness analysis
- Sample data with intentional bias

**Best for**: First-time users, quick introduction

### 2. [02_case_studies_deepbridge.ipynb](02_case_studies_deepbridge.ipynb)
**Duration**: 30-45 minutes

**What it covers**:
- Real-world case studies:
  - COMPAS (criminal recidivism)
  - Adult Income (census data)
  - German Credit (credit risk)
  - Bank Marketing (marketing campaigns)
- Detailed fairness analysis
- EEOC/ECOA compliance checking
- Bias identification

**Best for**: Understanding real applications, paper validation

## 🚀 Getting Started

### Prerequisites

1. **Install DeepBridge**:
   ```bash
   cd /home/guhaase/projetos/DeepBridge/deepbridge
   pip install -e .
   ```

2. **Install Jupyter**:
   ```bash
   pip install jupyter notebook
   ```

3. **Install dependencies**:
   ```bash
   cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework
   pip install -r requirements.txt
   ```

### Running Notebooks

```bash
# From this directory
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework/experiments/notebooks

# Start Jupyter
jupyter notebook

# Your browser will open, select a notebook to begin
```

Or run from repository root:
```bash
cd /home/guhaase/projetos/DeepBridge/papers/02_Fairness_Framework
jupyter notebook experiments/notebooks/
```

## 📊 Expected API (DeepBridge)

The notebooks assume the following DeepBridge API:

```python
from deepbridge import DBDataset
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Create DBDataset (auto-detects sensitive attributes)
dataset = DBDataset(
    data=df,
    target_column="target"
)

# Check detected attributes
print(dataset.detected_sensitive_attributes)  # e.g., ['gender', 'race', 'age']

# Run fairness analysis
results = dataset.analyze_fairness()
print(results)
```

## ⚠️ Implementation Notes

The notebooks demonstrate the **intended API** for DeepBridge based on the experimental validation scripts in `experiments/scripts/`.

**Current Status**:
- ✅ DeepBridge library installed and functional
- ✅ Basic `DBDataset` class available
- ⚠️ `detected_sensitive_attributes` attribute - check DeepBridge implementation
- ⚠️ `analyze_fairness()` method - check DeepBridge implementation

If you encounter `AttributeError` for these methods:
1. Check DeepBridge version: `pip show deepbridge`
2. Verify you're using the latest version from `/home/guhaase/projetos/DeepBridge/deepbridge`
3. Review DeepBridge source code for current API
4. Update notebooks if API has changed

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'deepbridge'"

**Solution**:
```bash
pip install -e /home/guhaase/projetos/DeepBridge/deepbridge
```

### "AttributeError: 'DBDataset' object has no attribute 'detected_sensitive_attributes'"

**Solution**:
- This feature may be in development
- Check the experimental scripts in `experiments/scripts/exp1_auto_detection.py` for current usage
- Review DeepBridge source code: `/home/guhaase/projetos/DeepBridge/deepbridge`

### Jupyter kernel crashes

**Solution**:
```bash
# Create fresh virtual environment
python3 -m venv venv_notebooks
source venv_notebooks/bin/activate
pip install --upgrade pip
pip install jupyter notebook
pip install -r requirements.txt
pip install -e /home/guhaase/projetos/DeepBridge/deepbridge
```

### Case study data not found

**Solution**:
- Ensure case study datasets are in `data/case_studies/`
- Download or generate datasets as needed
- See `data/README.md` for dataset sources

## 📚 Additional Resources

- **Documentation**: [docs/](../../docs/)
  - [Quick Start Guide](../../docs/quickstart.md)
  - [Installation Guide](../../docs/installation.md)
- **Experimental Scripts**: [experiments/scripts/](../scripts/)
  - `exp1_auto_detection.py` - Validates auto-detection
  - `exp4_case_studies.py` - Case study analysis
- **DeepBridge Source**: `/home/guhaase/projetos/DeepBridge/deepbridge`
- **Paper**: [paper/main/](../../paper/main/)

## 🤝 Contributing

Found an issue or want to improve a notebook?

1. Update the notebook
2. Test it thoroughly
3. Submit a pull request
4. See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## 📧 Questions?

- Check [docs/faq.md](../../docs/faq.md)
- Review [troubleshooting guide](../../docs/troubleshooting.md)
- Open an issue on GitHub

---

**Last Updated**: 2025-12-10

**Status**: ✅ Notebooks created with intended DeepBridge API
