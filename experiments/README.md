# Experiments

This directory contains all experimental validation for the Fairness Framework paper.

## 🎯 Overview

The framework is validated through **5 comprehensive experiments**:

| # | Experiment | Objective | Key Result | Duration |
|---|------------|-----------|------------|----------|
| 1 | **Auto-detection** | Validate bias detection accuracy | F1-Score: 0.90 | 3-4 weeks |
| 2 | **Usability** | Evaluate user experience | SUS Score: 85.2 | 4 weeks |
| 3 | **EEOC/ECOA Compliance** | Verify regulatory compliance | 100% precision | 1 week |
| 4 | **Case Studies** | Real-world validation | 4 datasets | 3 weeks |
| 5 | **Performance** | Benchmark speed | 2.9x speedup | 1 week |

**Total validation**: 500+ synthetic datasets + 4 real-world case studies

## 📁 Structure

```
experiments/
├── README.md              # This file
├── scripts/               # Experiment scripts
│   ├── exp1_*.py
│   ├── exp2_*.py
│   ├── exp3_*.py
│   ├── exp4_*.py
│   ├── exp5_*.py
│   └── run_all.sh        # Run all experiments
├── notebooks/             # Jupyter notebooks
│   ├── 01_quick_demo.ipynb
│   └── ...
├── config/                # Configuration files
├── results/               # Experimental results (gitignored)
└── reports/               # Generated reports
```

## 🚀 Quick Start

### Run Quick Demo (5 minutes)

```bash
# Python script
python ../scripts/demo_quick.py

# Or Jupyter notebook
jupyter notebook notebooks/01_quick_demo.ipynb
```

### Run Specific Experiment

```bash
cd scripts/

# Experiment 1: Auto-detection (3-4 weeks)
python exp1_auto_detection.py

# Experiment 2: Usability (requires participants)
python exp5_usability.py

# Experiment 3: EEOC/ECOA Compliance
python exp3_eeoc_validation.py

# Experiment 4: Case Studies
python exp4_case_studies.py

# Experiment 5: Performance Benchmarks
python exp6_performance.py
```

### Run All Experiments

```bash
cd scripts/
./run_all.sh  # Runs all experiments (4-5 hours)
```

## 📊 Experiment Details

### Experiment 1: Automated Bias Detection

**Objective**: Validate the framework's ability to automatically detect bias

**Method**:
- 500 synthetic datasets with various bias scenarios
- Ground truth annotations from 2 independent annotators
- Metrics: Precision, Recall, F1-Score

**Expected Results**:
- F1-Score ≥ 0.90
- Precision ≥ 0.92
- Recall ≥ 0.89

**Duration**: 3-4 weeks

**Script**: `scripts/exp1_auto_detection.py`

---

### Experiment 2: Usability Evaluation

**Objective**: Evaluate user experience and ease of use

**Method**:
- 20 participants (10 ML practitioners, 10 domain experts)
- Tasks: detect bias, interpret results, apply mitigation
- System Usability Scale (SUS) questionnaire

**Expected Results**:
- SUS Score ≥ 85.2
- NASA-TLX ≤ 32.1
- Task success rate ≥ 95%

**Duration**: 4 weeks

**Script**: `scripts/exp5_usability.py`

**Note**: Requires participant recruitment

---

### Experiment 3: EEOC/ECOA Compliance

**Objective**: Verify regulatory compliance checking

**Method**:
- Test EEOC 80% rule implementation
- Validate ECOA compliance checking
- 100 synthetic scenarios

**Expected Results**:
- 100% precision on compliance violations
- 100% recall on compliance violations

**Duration**: 1 week

**Script**: `scripts/exp3_eeoc_validation.py`

---

### Experiment 4: Real-World Case Studies

**Objective**: Validate on real-world datasets

**Method**:
- 4 case studies: COMPAS (7.2 min), German Credit (5.8 min), Adult (12.4 min), Healthcare (9.1 min)
- Compare with state-of-the-art tools (AIF360, Fairlearn)
- Measure time-to-insight

**Expected Results**:
- Detect known biases in all 4 datasets
- 75-79% time reduction vs. manual analysis

**Duration**: 3 weeks

**Script**: `scripts/exp4_case_studies.py`

**Datasets**: Available in `../data/case_studies/`

---

### Experiment 5: Performance Benchmarks

**Objective**: Measure computational efficiency

**Method**:
- Benchmark on datasets of varying sizes (100 to 100,000 rows)
- Compare runtime with AIF360 and Fairlearn
- Measure memory usage

**Expected Results**:
- 2.9x faster than baseline
- 40-42% memory reduction
- Linear scaling with dataset size

**Duration**: 1 week

**Script**: `scripts/exp6_performance.py`

---

## 📈 Results

Results from all experiments are saved in `results/`:

```
results/
├── auto_detection/
│   ├── metrics.json
│   ├── confusion_matrix.png
│   └── report.html
├── usability/
├── eeoc_validation/
├── case_studies/
└── performance/
```

## 📝 Configuration

Experiment parameters can be configured in `config/`:

```yaml
# Example: config/exp1_detection.yaml
n_datasets: 500
threshold: 0.1
random_seed: 42
output_dir: results/auto_detection/
```

## 🔍 Monitoring Progress

Track experiment progress with:

```bash
# View checklist
cat CHECKLIST_RAPIDO.md

# View execution guide
cat GUIA_EXECUCAO.md

# View detailed timeline
cat ../docs/experiments/timeline.md
```

## 📚 Documentation

**Detailed documentation** is available in `../docs/experiments/`:

- [Overview](../docs/experiments/overview.md) - Executive summary (RESUMO_EXECUTIVO)
- [Timeline](../docs/experiments/timeline.md) - Detailed timeline and planning (PLANO_EXPERIMENTOS)

**Additional documents** (in Portuguese):
- `CHECKLIST_RAPIDO.md` - Quick tracking checklist
- `GUIA_EXECUCAO.md` - Execution guide
- `PLANO_EXPERIMENTOS.md` - Complete experiment plan (17 sections)
- `RESUMO_EXECUTIVO.md` - Executive summary

## ⚠️ Minimum Criteria for Publication

For the paper to be accepted at FAccT 2026, the following criteria **MUST** be met:

### ✅ Required (Deal-breakers):
1. **EEOC/ECOA**: 100% precision (no margin for error)
2. **SUS**: ≥ 75 (claim: 85.2)
3. **Speedup**: ≥ 2.0x (claim: 2.9x)
4. **Case Studies**: 4/4 completed
5. **Usability N**: ≥ 15 participants (claim: 20)

### ⭐ Recommended:
1. **F1 auto-detection**: ≥ 0.85 (claim: 0.90)
2. **Success rate**: ≥ 85% (claim: 95%)
3. **Datasets**: ≥ 300 (claim: 500)

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r ../requirements.txt
```

**Issue**: Data not found
```bash
# Solution: Check data directory
ls ../data/synthetic/
# If empty, data may have been gitignored (too large)
# See ../data/README.md for instructions
```

**Issue**: Out of memory
```bash
# Solution: Reduce batch size in config files
# Edit config/*.yaml and reduce n_samples or batch_size
```

For more issues, see [../docs/troubleshooting.md](../docs/troubleshooting.md)

## 🤝 Contributing

Found issues or want to add experiments?

1. See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
2. Add your experiment script to `scripts/`
3. Add configuration to `config/`
4. Document in this README
5. Submit a pull request

## 📧 Questions?

- **General questions**: See [../docs/faq.md](../docs/faq.md)
- **Experimental methodology**: See [../docs/experiments/overview.md](../docs/experiments/overview.md)
- **Technical issues**: Open a GitHub issue
- **Email**: your-email@domain.com

## 📚 References

### Base Papers:
- Bellamy et al. (2018) - AI Fairness 360
- Bird et al. (2020) - Fairlearn
- Saleiro et al. (2018) - Aequitas

### Methodologies:
- Brooke (1996) - System Usability Scale
- Hart & Staveland (1988) - NASA Task Load Index

### Datasets:
- COMPAS - ProPublica
- German Credit - UCI Repository
- Adult Income - UCI Repository

---

**Last Updated**: 2025-12-10

**Project Status**: ⬜ Not started (ready to begin)

**Deadline**: FAccT 2026 submission (check exact deadline)

**Good luck with the experiments! 🚀**
