# Fairness Framework for Machine Learning

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/main/main.pdf)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **An automated framework for fairness detection and bias mitigation in machine learning with regulatory compliance (EEOC/ECOA)**

## 🎯 Overview

This repository contains the implementation and experiments for our paper on automated fairness detection in machine learning systems. Our framework provides:

- **Automated Bias Detection**: Identifies unfair patterns in ML models with high accuracy (F1-Score: 0.90)
- **Regulatory Compliance**: Ensures EEOC and ECOA compliance with 100% precision
- **Performance Optimized**: 2.9x faster than baseline approaches
- **User-Friendly**: Designed with practitioners in mind (SUS Score: 85.2)

The framework has been validated across 500+ synthetic datasets and 4 real-world case studies, demonstrating its effectiveness in detecting and mitigating various forms of algorithmic bias.

## ✨ Key Features

- 🔍 **Automatic Fairness Detection**: Detects demographic parity, equalized odds, and other fairness violations
- 📊 **Multiple Fairness Metrics**: Supports 10+ standard fairness metrics
- 🎯 **Regulatory Compliance**: Built-in EEOC and ECOA compliance checking
- 📈 **Comprehensive Reporting**: Generates detailed fairness reports with visualizations
- 🚀 **Production Ready**: Optimized for performance and scalability
- 🔧 **Easy Integration**: Simple API for integration into existing ML pipelines

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/username/fairness-framework.git
cd fairness-framework

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.fairness_detector import FairnessDetector

# Initialize detector
detector = FairnessDetector()

# Load your dataset
detector.load_data("data/case_studies/adult/adult.csv",
                   target="income",
                   sensitive_attrs=["race", "sex"])

# Detect bias
results = detector.detect_bias()

# Print report
print(results.summary())

# Visualize results
results.plot()
```

### Run Demo

```bash
# Quick demo (5 minutes)
python scripts/demo_quick.py

# Full experiments (4-5 hours)
cd experiments/scripts
./run_all.sh
```

## 📊 Experiments and Results

Our framework was evaluated through 5 comprehensive experiments:

| Experiment | Objective | Key Result | Status |
|------------|-----------|------------|--------|
| **Exp 1** | Auto-detection accuracy | F1-Score: 0.90 | ✅ Validated |
| **Exp 2** | Usability evaluation | SUS Score: 85.2 | ✅ Validated |
| **Exp 3** | EEOC/ECOA compliance | 100% precision | ✅ Validated |
| **Exp 4** | Real-world case studies | 4 datasets | ✅ Validated |
| **Exp 5** | Performance benchmarks | 2.9x speedup | ✅ Validated |

**Tested on 500+ synthetic datasets** covering various bias scenarios and data distributions.

### Reproducing Results

See [experiments/README.md](experiments/README.md) for detailed instructions on reproducing all experiments.

```bash
# Setup environment
cd experiments
chmod +x setup.sh && ./setup.sh

# Run specific experiment
python scripts/exp1_detection.py

# Run all experiments
./scripts/run_all.sh
```

## 📁 Repository Structure

```
fairness-framework/
├── paper/                     # Research paper (3 versions)
│   ├── main/                  # Main English version
│   ├── facct2026/             # FAccT 2026 submission
│   └── portuguese/            # Portuguese version
├── src/                       # Framework source code
│   ├── fairness_detector.py   # Main detector class
│   ├── metrics.py             # Fairness metrics
│   └── visualization.py       # Plotting utilities
├── experiments/               # Experimental validation
│   ├── scripts/               # Experiment scripts
│   ├── notebooks/             # Jupyter notebooks
│   └── results/               # Experimental results
├── data/                      # Datasets
│   ├── synthetic/             # 500+ synthetic datasets
│   ├── case_studies/          # 4 real-world datasets
│   └── ground_truth/          # Annotated ground truth
├── docs/                      # Documentation
│   ├── quickstart.md          # 15-minute tutorial
│   ├── experiments/           # Experiment details
│   └── api/                   # API reference
├── tests/                     # Unit tests
└── docker/                    # Docker configuration
```

## 📖 Documentation

- **[Quick Start Guide](docs/quickstart.md)**: Get started in 15 minutes
- **[Experiments Overview](docs/experiments/overview.md)**: Detailed experimental methodology
- **[API Reference](docs/api/index.md)**: Complete API documentation
- **[Troubleshooting](docs/troubleshooting.md)**: Common issues and solutions
- **[FAQ](docs/faq.md)**: Frequently asked questions

## 🐳 Docker

```bash
# Build image
docker build -t fairness-framework .

# Run container
docker run -it fairness-framework

# Run with data volume
docker run -it -v $(pwd)/data:/app/data fairness-framework
```

## 📦 Requirements

- Python 3.8+
- NumPy >= 1.19.0
- Pandas >= 1.1.0
- scikit-learn >= 0.23.0
- fairlearn >= 0.7.0
- AIF360 >= 0.4.0

See [requirements.txt](requirements.txt) for complete list.

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_fairness_detector.py
```

## 📄 Citation

If you use this framework in your research, please cite our paper:

```bibtex
@article{fairness-framework-2025,
  title={Automated Fairness Detection Framework with Regulatory Compliance},
  author={Haase, Gustavo and Others},
  journal={Conference/Journal Name},
  year={2025},
  note={Paper available at: https://github.com/username/fairness-framework}
}
```

For software citation, see [CITATION.cff](CITATION.cff).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built on top of [Fairlearn](https://github.com/fairlearn/fairlearn) and [AIF360](https://github.com/Trusted-AI/AIF360)
- Case study datasets from [UCI ML Repository](https://archive.ics.uci.edu/ml/)
- Inspired by regulatory frameworks: EEOC, ECOA, GDPR, AI Act

## 📧 Contact

- **Author**: Gustavo Haase
- **Email**: [your-email@domain.com]
- **Project Link**: [https://github.com/username/fairness-framework](https://github.com/username/fairness-framework)

## 🔗 Related Work

- [Fairlearn](https://github.com/fairlearn/fairlearn): Python library for fairness assessment
- [AIF360](https://github.com/Trusted-AI/AIF360): Comprehensive bias detection toolkit
- [What-If Tool](https://pair-code.github.io/what-if-tool/): Visual ML fairness inspector

## 📊 Project Status

- ✅ **Paper**: Under review / Published [Update as needed]
- ✅ **Code**: Stable release v1.0.0
- ✅ **Experiments**: Fully reproducible
- 🔄 **Documentation**: Continuous improvement

---

**Note**: This is a research prototype. For production use, additional testing and validation is recommended.

**Last Updated**: 2025-12-10
