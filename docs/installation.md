# Installation Guide

Complete guide for setting up the DeepBridge experimental validation environment.

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Git**: For cloning repositories
- **pip**: Python package manager
- **Optional**: conda for environment management

## 🔧 Step-by-Step Installation

### Step 1: Install DeepBridge Library

The DeepBridge library is located at `/home/guhaase/projetos/DeepBridge/deepbridge`.

#### Option A: Development Mode (Recommended for validation)

```bash
# Navigate to DeepBridge source directory
cd /home/guhaase/projetos/DeepBridge/deepbridge

# Install in editable/development mode
pip install -e .

# This allows you to modify DeepBridge code and see changes immediately
```

#### Option B: Normal Installation

```bash
# Navigate to DeepBridge source directory
cd /home/guhaase/projetos/DeepBridge/deepbridge

# Install normally
pip install .
```

#### Option C: From PyPI (if published)

```bash
# If DeepBridge is published to PyPI
pip install deepbridge
```

### Step 2: Verify DeepBridge Installation

```bash
# Test import
python -c "from deepbridge import DBDataset; print('✓ DeepBridge installed successfully')"

# Check version
python -c "import deepbridge; print(f'DeepBridge version: {deepbridge.__version__}')"
```

### Step 3: Clone Experiments Repository

```bash
# Navigate to desired location
cd /home/guhaase/projetos/DeepBridge/papers

# The repository should already be there
cd 02_Fairness_Framework
```

### Step 4: Install Experiment Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# This installs:
# - pandas, numpy, scipy
# - scikit-learn, xgboost, lightgbm
# - matplotlib, seaborn, plotly
# - aif360, fairlearn (for comparison)
# - jupyter, pytest
```

### Step 5: Verify Complete Installation

```bash
# Run verification
python -c "
from deepbridge import DBDataset
import pandas as pd
import numpy as np
print('✓ All imports successful')
print('✓ Installation complete')
"
```

## 🐳 Docker Installation (Alternative)

If you prefer using Docker:

```bash
# Build Docker image
docker build -t fairness-experiments -f docker/Dockerfile .

# Run container
docker run -it fairness-experiments

# Run with data volumes
docker run -it \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/experiments/results:/app/experiments/results \
  fairness-experiments
```

## 📦 Package Versions

The experiments were validated with:

- **Python**: 3.8+
- **DeepBridge**: 0.1.0+
- **pandas**: 1.3.0+
- **numpy**: 1.21.0+
- **scikit-learn**: 1.0.0+
- **aif360**: 0.5.0+
- **fairlearn**: 0.10.0+

See `requirements.txt` for complete list.

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'deepbridge'"

**Solution**:
```bash
# Make sure DeepBridge is installed
cd /home/guhaase/projetos/DeepBridge/deepbridge
pip install -e .

# Verify
python -c "import deepbridge"
```

### Issue: "ImportError: cannot import name 'DBDataset'"

**Solution**:
```bash
# DeepBridge might need to be reinstalled
cd /home/guhaase/projetos/DeepBridge/deepbridge
pip uninstall deepbridge -y
pip install -e .
```

### Issue: Dependencies conflict

**Solution**:
```bash
# Use a fresh virtual environment
python -m venv venv_clean
source venv_clean/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Permission denied

**Solution**:
```bash
# Install in user space
pip install --user -e /home/guhaase/projetos/DeepBridge/deepbridge
```

## 🧪 Verify Installation with Test

Create a file `test_installation.py`:

```python
#!/usr/bin/env python3
"""Test DeepBridge installation."""

from deepbridge import DBDataset
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame({
    'age': [25, 45, 35, 50],
    'gender': ['M', 'F', 'M', 'F'],
    'income': [50000, 80000, 60000, 90000],
    'approved': [1, 0, 1, 1]
})

# Create DBDataset
try:
    dataset = DBDataset(data=df, target_column='approved')
    print("✓ DBDataset created successfully")
    print(f"✓ Detected attributes: {dataset.detected_sensitive_attributes}")
    print("✓ Installation verified!")
except Exception as e:
    print(f"✗ Error: {e}")
```

Run it:
```bash
python test_installation.py
```

Expected output:
```
✓ DBDataset created successfully
✓ Detected attributes: ['gender']
✓ Installation verified!
```

## 📚 Next Steps

After installation:

1. **Read Quick Start**: See [quickstart.md](quickstart.md)
2. **Run Experiments**: See [../experiments/README.md](../experiments/README.md)
3. **Explore Notebooks**: `jupyter notebook experiments/notebooks/`
4. **Read Paper**: See [../paper/english/main.pdf](../paper/english/main.pdf)

## 🔗 Related Documentation

- **DeepBridge Source**: `/home/guhaase/projetos/DeepBridge/deepbridge`
- **Experiments Guide**: [../experiments/README.md](../experiments/README.md)
- **Quick Start**: [quickstart.md](quickstart.md)
- **Troubleshooting**: [troubleshooting.md](troubleshooting.md)

## 📧 Getting Help

If you encounter issues:

1. Check [troubleshooting.md](troubleshooting.md)
2. Check DeepBridge documentation
3. Open an issue on GitHub
4. Contact: your-email@domain.com

---

**Last Updated**: 2025-12-10
