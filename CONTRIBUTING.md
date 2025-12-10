# Contributing to Fairness Framework

Thank you for your interest in contributing to the Fairness Framework! We welcome contributions from the community.

## 🎯 Ways to Contribute

- 🐛 **Bug Reports**: Report bugs via GitHub Issues
- ✨ **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve or translate documentation
- 🔧 **Code**: Submit bug fixes or new features
- 🧪 **Testing**: Add or improve test coverage
- 📊 **Datasets**: Contribute new case studies or benchmark datasets

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/fairness-framework.git
cd fairness-framework
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks (optional but recommended)
# pip install pre-commit
# pre-commit install
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes:
git checkout -b fix/issue-description
```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 style guidelines with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Grouped in order: stdlib, third-party, local
- **Docstrings**: Google style
- **Type hints**: Use for all public functions

```python
from typing import List, Optional

import numpy as np
import pandas as pd

from src.utils import helper_function


def detect_bias(data: pd.DataFrame,
                threshold: float = 0.05) -> dict:
    """Detect bias in dataset.

    Args:
        data: Input DataFrame with features and target.
        threshold: Significance threshold for bias detection.

    Returns:
        Dictionary containing bias detection results.

    Raises:
        ValueError: If data is empty or missing required columns.
    """
    pass
```

### Documentation

- **All public functions/classes**: Must have docstrings
- **Complex logic**: Add inline comments explaining why, not what
- **Examples**: Include usage examples in docstrings
- **README updates**: Update if you add new features

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_fairness_detector.py

# Run specific test
pytest tests/test_fairness_detector.py::test_bias_detection
```

**Test Requirements**:
- All new features must include tests
- Aim for >80% code coverage
- Tests should be fast (<1s each typically)
- Use fixtures for common test data

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(detector): add support for intersectional fairness metrics

Implements intersectional fairness analysis for multiple protected
attributes simultaneously.

Closes #123
```

```
fix(metrics): correct equalized odds calculation

The previous implementation didn't account for class imbalance.
This fixes the calculation to properly weight classes.
```

## 🔄 Pull Request Process

### 1. Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main

### 2. Submit PR

1. Push your branch to your fork
2. Open a Pull Request to `main` branch
3. Fill out the PR template
4. Link related issues (e.g., "Closes #123")

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
Describe tests you added/modified

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings
```

### 4. Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, PR will be merged

## 🐛 Reporting Bugs

Use GitHub Issues with the bug report template:

**Required Information**:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack trace
- Minimal reproducible example

**Example**:
```markdown
**Bug Description**
Bias detection fails on datasets with missing values

**To Reproduce**
```python
import pandas as pd
from src.fairness_detector import FairnessDetector

df = pd.DataFrame({'A': [1, None, 3], 'B': [1, 2, 3]})
detector = FairnessDetector()
detector.detect_bias(df)  # Raises ValueError
```

**Expected**: Handle missing values gracefully
**Actual**: ValueError: Cannot compute metrics with NaN values

**Environment**:
- Python 3.9.7
- Ubuntu 20.04
- fairness-framework v1.0.0
```

## ✨ Feature Requests

Use GitHub Issues with feature request template:

- Clear description of the feature
- Use case / motivation
- Proposed implementation (if any)
- Alternatives considered
- Additional context

## 📊 Contributing Datasets

We welcome contributions of new case studies:

1. Ensure data is public or properly licensed
2. Anonymize if necessary
3. Include metadata:
   - Source
   - Description
   - License
   - Protected attributes
   - Known biases
4. Add to `data/case_studies/` with README
5. Update experiments documentation

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Standards

**Expected Behavior**:
- Be respectful and inclusive
- Welcome diverse perspectives
- Accept constructive criticism gracefully
- Focus on what's best for the community

**Unacceptable Behavior**:
- Harassment or discriminatory language
- Personal attacks
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Violations can be reported to [your-email@domain.com]. All complaints will be reviewed and investigated.

## 🙋 Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security issues**: Email [your-email@domain.com] directly
- **Other**: Email [your-email@domain.com]

## 📚 Additional Resources

- [Code Style Guide](docs/style_guide.md) (if available)
- [Architecture Overview](docs/architecture.md) (if available)
- [Testing Guide](docs/testing.md) (if available)

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in papers (for significant contributions)

---

Thank you for contributing to making ML systems more fair and equitable!
