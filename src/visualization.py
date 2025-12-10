"""
Visualization Functions

This module provides visualization functions for fairness analysis,
including plots for metrics, group comparisons, and reports.
"""

from typing import Union, List, Optional, Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def plot_fairness_report(results, save_path: Optional[str] = None) -> None:
    """Plot comprehensive fairness report.

    Args:
        results: BiasDetectionResult object
        save_path: Optional path to save figure

    Example:
        >>> from src.fairness_detector import FairnessDetector
        >>> detector = FairnessDetector()
        >>> results = detector.detect_bias(data)
        >>> plot_fairness_report(results)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Fairness Analysis Report', fontsize=16, fontweight='bold')

    # Plot 1: Metric values
    if results.metrics:
        ax = axes[0, 0]
        metrics_names = list(results.metrics.keys())
        metrics_values = list(results.metrics.values())

        colors = ['red' if abs(v) > 0.1 else 'green' for v in metrics_values]
        ax.barh(metrics_names, metrics_values, color=colors, alpha=0.7)
        ax.axvline(x=0.1, color='red', linestyle='--', label='Threshold (+0.1)')
        ax.axvline(x=-0.1, color='red', linestyle='--', label='Threshold (-0.1)')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_xlabel('Metric Value')
        ax.set_title('Fairness Metrics')
        ax.legend()

    # Plot 2: Status summary
    ax = axes[0, 1]
    ax.axis('off')
    status_text = "BIAS DETECTED ⚠️" if results.has_bias else "NO BIAS ✓"
    color = 'red' if results.has_bias else 'green'

    ax.text(0.5, 0.7, status_text, ha='center', va='center',
            fontsize=24, fontweight='bold', color=color)

    if results.bias_type:
        ax.text(0.5, 0.5, f"Type: {results.bias_type}", ha='center', va='center',
                fontsize=14)

    if results.sensitive_attrs:
        attrs_text = f"Attributes: {', '.join(results.sensitive_attrs)}"
        ax.text(0.5, 0.3, attrs_text, ha='center', va='center', fontsize=12)

    # Plot 3: Recommendations (if any)
    ax = axes[1, 0]
    ax.axis('off')
    if results.recommendations:
        rec_text = "Recommendations:\n\n" + "\n".join(
            [f"{i+1}. {rec}" for i, rec in enumerate(results.recommendations[:5])]
        )
        ax.text(0.05, 0.95, rec_text, ha='left', va='top',
                fontsize=10, wrap=True)
        ax.set_title('Recommendations')

    # Plot 4: Placeholder for additional info
    ax = axes[1, 1]
    ax.axis('off')
    ax.text(0.5, 0.5, 'Additional analysis can be added here',
            ha='center', va='center', fontsize=10, style='italic')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_metric_comparison(
    metrics: Dict[str, float],
    threshold: float = 0.1,
    save_path: Optional[str] = None
) -> None:
    """Plot comparison of multiple fairness metrics.

    Args:
        metrics: Dictionary of metric names and values
        threshold: Fairness threshold (default: 0.1)
        save_path: Optional path to save figure

    Example:
        >>> metrics = {
        >>>     'demographic_parity': 0.15,
        >>>     'equalized_odds': 0.08,
        >>>     'equal_opportunity': 0.12
        >>> }
        >>> plot_metric_comparison(metrics)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    names = list(metrics.keys())
    values = list(metrics.values())

    colors = ['red' if abs(v) > threshold else 'green' for v in values]

    bars = ax.barh(names, values, color=colors, alpha=0.7)

    ax.axvline(x=threshold, color='red', linestyle='--', alpha=0.5, label=f'Threshold (+{threshold})')
    ax.axvline(x=-threshold, color='red', linestyle='--', alpha=0.5, label=f'Threshold (-{threshold})')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

    ax.set_xlabel('Metric Value', fontsize=12)
    ax.set_title('Fairness Metrics Comparison', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_group_comparison(
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series],
    group_names: Optional[List[str]] = None,
    save_path: Optional[str] = None
) -> None:
    """Plot comparison of prediction rates by group.

    Args:
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values
        group_names: Optional custom names for groups
        save_path: Optional path to save figure

    Example:
        >>> plot_group_comparison(predictions, race)
    """
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    rates = [np.mean(y_pred[sensitive_attr == g]) for g in groups]

    if group_names:
        labels = group_names
    else:
        labels = [f"Group {g}" for g in groups]

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(labels, rates, alpha=0.7, edgecolor='black')

    # Color bars based on disparity
    if len(rates) == 2:
        diff = abs(rates[1] - rates[0])
        color = 'red' if diff > 0.1 else 'green'
        for bar in bars:
            bar.set_color(color)

    ax.set_ylabel('Positive Prediction Rate', fontsize=12)
    ax.set_title('Prediction Rates by Group', fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, rate) in enumerate(zip(bars, rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.3f}',
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_confusion_matrices(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series],
    save_path: Optional[str] = None
) -> None:
    """Plot confusion matrices for each group.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute
        save_path: Optional path to save figure

    Example:
        >>> plot_confusion_matrices(y_true, y_pred, race)
    """
    from sklearn.metrics import confusion_matrix

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    n_groups = len(groups)

    fig, axes = plt.subplots(1, n_groups, figsize=(6*n_groups, 5))
    if n_groups == 1:
        axes = [axes]

    fig.suptitle('Confusion Matrices by Group', fontsize=14, fontweight='bold')

    for i, (ax, group) in enumerate(zip(axes, groups)):
        mask = sensitive_attr == group
        cm = confusion_matrix(y_true[mask], y_pred[mask])

        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=['Negative', 'Positive'],
                   yticklabels=['Negative', 'Positive'])

        ax.set_title(f'Group: {group}')
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_roc_curves_by_group(
    y_true: Union[np.ndarray, pd.Series],
    y_score: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series],
    save_path: Optional[str] = None
) -> None:
    """Plot ROC curves for each group.

    Args:
        y_true: True labels
        y_score: Prediction scores (probabilities)
        sensitive_attr: Sensitive attribute
        save_path: Optional path to save figure

    Example:
        >>> plot_roc_curves_by_group(y_true, y_proba, race)
    """
    from sklearn.metrics import roc_curve, auc

    y_true = np.array(y_true)
    y_score = np.array(y_score)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)

    fig, ax = plt.subplots(figsize=(8, 6))

    for group in groups:
        mask = sensitive_attr == group
        fpr, tpr, _ = roc_curve(y_true[mask], y_score[mask])
        roc_auc = auc(fpr, tpr)

        ax.plot(fpr, tpr, label=f'Group {group} (AUC = {roc_auc:.3f})',
                linewidth=2)

    ax.plot([0, 1], [0, 1], 'k--', label='Random')
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('ROC Curves by Group', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def plot_metric_distribution(
    metric_values: List[float],
    metric_name: str = "Metric",
    threshold: float = 0.1,
    save_path: Optional[str] = None
) -> None:
    """Plot distribution of metric values (e.g., from bootstrap).

    Args:
        metric_values: List of metric values
        metric_name: Name of the metric
        threshold: Fairness threshold
        save_path: Optional path to save figure

    Example:
        >>> # After bootstrap
        >>> plot_metric_distribution(bootstrap_values, "Demographic Parity")
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(metric_values, bins=30, alpha=0.7, edgecolor='black')

    ax.axvline(x=threshold, color='red', linestyle='--', label=f'Threshold (+{threshold})')
    ax.axvline(x=-threshold, color='red', linestyle='--', label=f'Threshold (-{threshold})')
    ax.axvline(x=np.mean(metric_values), color='blue', linestyle='-',
              linewidth=2, label=f'Mean: {np.mean(metric_values):.3f}')

    ax.set_xlabel(metric_name, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(f'{metric_name} Distribution', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


def create_fairness_dashboard(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series],
    metrics: Dict[str, float],
    save_path: Optional[str] = None
) -> None:
    """Create comprehensive fairness dashboard.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute
        metrics: Dictionary of metric values
        save_path: Optional path to save figure

    Example:
        >>> metrics = compute_all_metrics(y_true, y_pred, sensitive)
        >>> create_fairness_dashboard(y_true, y_pred, sensitive, metrics)
    """
    from sklearn.metrics import confusion_matrix

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    fig.suptitle('Fairness Analysis Dashboard', fontsize=16, fontweight='bold')

    # 1. Metrics comparison
    ax1 = fig.add_subplot(gs[0, :2])
    names = list(metrics.keys())
    values = list(metrics.values())
    colors = ['red' if abs(v) > 0.1 else 'green' for v in values]
    ax1.barh(names, values, color=colors, alpha=0.7)
    ax1.axvline(x=0.1, color='red', linestyle='--', alpha=0.5)
    ax1.axvline(x=-0.1, color='red', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Metric Value')
    ax1.set_title('Fairness Metrics')
    ax1.grid(axis='x', alpha=0.3)

    # 2. Group comparison
    ax2 = fig.add_subplot(gs[0, 2])
    groups = np.unique(sensitive_attr)
    rates = [np.mean(y_pred[sensitive_attr == g]) for g in groups]
    ax2.bar(range(len(groups)), rates, alpha=0.7)
    ax2.set_xticks(range(len(groups)))
    ax2.set_xticklabels([f'G{g}' for g in groups])
    ax2.set_ylabel('Positive Rate')
    ax2.set_title('Rates by Group')
    ax2.set_ylim([0, 1])

    # 3 & 4. Confusion matrices
    for i, group in enumerate(groups[:2]):
        ax = fig.add_subplot(gs[1, i])
        mask = sensitive_attr == group
        cm = confusion_matrix(y_true[mask], y_pred[mask])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, cbar=False)
        ax.set_title(f'Group {group}')
        ax.set_ylabel('True')
        ax.set_xlabel('Predicted')

    # 5. Summary stats
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    summary_text = f"Total Samples: {len(y_true)}\n"
    summary_text += f"Groups: {len(groups)}\n\n"
    summary_text += "Metrics Summary:\n"
    for name, value in metrics.items():
        status = "✓" if abs(value) <= 0.1 else "✗"
        summary_text += f"{status} {name[:15]}: {value:.3f}\n"
    ax5.text(0.1, 0.9, summary_text, fontsize=9, verticalalignment='top',
            fontfamily='monospace')

    # 6. Distribution
    ax6 = fig.add_subplot(gs[2, :])
    df = pd.DataFrame({
        'Prediction': y_pred,
        'Group': sensitive_attr
    })
    for group in groups:
        group_data = df[df['Group'] == group]['Prediction']
        ax6.hist(group_data, alpha=0.5, label=f'Group {group}', bins=20)
    ax6.set_xlabel('Prediction Value')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Prediction Distribution by Group')
    ax6.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()
