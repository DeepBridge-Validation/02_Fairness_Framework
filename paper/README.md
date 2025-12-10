# Research Paper

This directory contains the research paper in multiple versions and languages.

## 📁 Structure

- **main/**: Main English version (reference version)
- **facct2026/**: Version formatted for FAccT 2026 conference submission
- **portuguese/**: Portuguese version for arXiv and local dissemination

## 📄 Versions

### Main Version (English)
- **File**: `main/main.pdf`
- **Status**: Complete (17 pages)
- **Use**: General reference, citations, preprints

### FAccT 2026 Submission
- **File**: `facct2026/main.pdf`
- **Status**: Ready for submission
- **Conference**: ACM Conference on Fairness, Accountability, and Transparency
- **Format**: ACM conference proceedings format

### Portuguese Version
- **File**: `portuguese/main.pdf`
- **Status**: Complete
- **Use**: arXiv submission, Brazilian dissemination

## 🔨 Compilation

Each version has its own LaTeX source files. To compile:

```bash
# Compile main version
cd main/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or use latexmk (recommended)
latexmk -pdf main.tex
```

## 📊 Paper Highlights

- **Title**: Automated Fairness Detection Framework with Regulatory Compliance
- **Pages**: 17
- **Key Results**:
  - F1-Score: 0.90 for bias detection
  - 100% precision on EEOC/ECOA compliance
  - 2.9x performance speedup
  - SUS Score: 85.2 for usability

## 🔗 Related Files

- Experimental validation: See `/experiments/` directory
- Source code: See `/src/` directory
- Documentation: See `/docs/` directory

## 📧 Contact

For questions about the paper, contact [your-email@domain.com]
