# Publication Figures - DeepBridge Fairness Framework

## Figures Overview

All figures are generated at 300 DPI in both PNG and PDF formats for maximum flexibility.

### Figure 1: Detection Performance
**File**: `figure1_detection_performance.{png,pdf}`
**Description**: Bar chart showing Precision, Recall, and F1-Score for automatic sensitive attribute detection.
**Usage in paper**: Section Results, subsection "Detection Accuracy (RQ1)"

### Figure 2: Performance Comparison
**File**: `figure2_performance_comparison.{png,pdf}`
**Description**: Bar chart comparing execution time between DeepBridge (automatic) and manual identification.
**Usage in paper**: Section Results, subsection "Computational Performance (RQ2)"

### Figure 3: Inter-Rater Agreement Distribution
**File**: `figure3_inter_rater_distribution.{png,pdf}`
**Description**: Histogram showing distribution of Cohen's Kappa across 500 datasets.
**Usage in paper**: Section Results, subsection "Ground Truth Quality"

### Figure 4: Precision-Recall Trade-off
**File**: `figure4_precision_recall.{png,pdf}`
**Description**: Scatter plot showing operating point with iso-F1 curves.
**Usage in paper**: Section Discussion or Appendix

### Figure 5: Confusion Matrix
**File**: `figure5_confusion_matrix.{png,pdf}`
**Description**: Normalized confusion matrix for sensitive attribute detection.
**Usage in paper**: Section Results or Appendix

### Figure 6: Speedup by Dataset Size
**File**: `figure6_speedup_by_size.{png,pdf}`
**Description**: Line plot showing how speedup scales with dataset size.
**Usage in paper**: Section Discussion, subsection "Scalability"

## LaTeX Integration

To include these figures in your LaTeX document:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/publication/figure1_detection_performance.pdf}
    \caption{Automatic sensitive attribute detection performance across 100 datasets.
             Error bars represent 95\% confidence intervals.}
    \label{fig:detection_performance}
\end{figure}
```

## Quality Standards

- **Resolution**: 300 DPI (publication quality)
- **Formats**: PNG (raster) and PDF (vector)
- **Fonts**: Times New Roman (serif, standard for academic publications)
- **Color palette**: Colorblind-friendly
- **Size**: Optimized for two-column format (ACM/IEEE standard)

## Regeneration

To regenerate all figures with updated data:

```bash
cd scripts/
python generate_publication_figures.py
```

This will overwrite existing figures with fresh versions based on the latest experimental results.
