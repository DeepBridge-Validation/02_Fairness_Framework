"""
Utility Functions

This module provides utility functions for data processing, validation,
and common operations used throughout the fairness framework.
"""

from typing import List, Union, Tuple, Optional
import numpy as np
import pandas as pd
from pathlib import Path


def validate_binary_labels(y: Union[np.ndarray, pd.Series]) -> None:
    """Validate that labels are binary (0 or 1).

    Args:
        y: Labels to validate

    Raises:
        ValueError: If labels are not binary
    """
    unique_values = np.unique(y)
    if not np.array_equal(unique_values, [0, 1]) and not np.array_equal(unique_values, [0]) and not np.array_equal(unique_values, [1]):
        raise ValueError(f"Labels must be binary (0 or 1). Found: {unique_values}")


def validate_sensitive_attribute(
    sensitive_attr: Union[np.ndarray, pd.Series],
    allow_multiclass: bool = False
) -> None:
    """Validate sensitive attribute.

    Args:
        sensitive_attr: Sensitive attribute to validate
        allow_multiclass: Whether to allow more than 2 groups

    Raises:
        ValueError: If validation fails
    """
    unique_groups = np.unique(sensitive_attr)

    if len(unique_groups) < 2:
        raise ValueError("Sensitive attribute must have at least 2 groups")

    if not allow_multiclass and len(unique_groups) > 2:
        raise ValueError(f"Binary sensitive attribute required. Found {len(unique_groups)} groups.")


def check_data_compatibility(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> None:
    """Check that all arrays have compatible shapes.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute

    Raises:
        ValueError: If shapes don't match
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    if not (y_true.shape[0] == y_pred.shape[0] == sensitive_attr.shape[0]):
        raise ValueError(
            f"Array lengths don't match: "
            f"y_true={y_true.shape[0]}, "
            f"y_pred={y_pred.shape[0]}, "
            f"sensitive_attr={sensitive_attr.shape[0]}"
        )


def load_dataset(filepath: Union[str, Path]) -> pd.DataFrame:
    """Load dataset from file.

    Supports CSV, Parquet, and other formats via pandas.

    Args:
        filepath: Path to dataset file

    Returns:
        pd.DataFrame: Loaded dataset

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format not supported
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Determine format from extension
    suffix = filepath.suffix.lower()

    if suffix == '.csv':
        return pd.read_csv(filepath)
    elif suffix == '.parquet':
        return pd.read_parquet(filepath)
    elif suffix in ['.json', '.jsonl']:
        return pd.read_json(filepath)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def save_results(results: dict, filepath: Union[str, Path]) -> None:
    """Save results to file.

    Args:
        results: Dictionary of results to save
        filepath: Output filepath

    Example:
        >>> results = {'metric1': 0.5, 'metric2': 0.3}
        >>> save_results(results, 'results.json')
    """
    import json

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)


def group_statistics(
    y: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> pd.DataFrame:
    """Compute statistics by group.

    Args:
        y: Values to compute statistics for
        sensitive_attr: Grouping attribute

    Returns:
        pd.DataFrame: Statistics by group

    Example:
        >>> stats = group_statistics(predictions, race)
        >>> print(stats)
    """
    df = pd.DataFrame({
        'value': y,
        'group': sensitive_attr
    })

    stats = df.groupby('group')['value'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).reset_index()

    return stats


def confusion_matrix_by_group(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> dict:
    """Compute confusion matrix for each group.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Grouping attribute

    Returns:
        dict: Confusion matrices by group

    Example:
        >>> cm = confusion_matrix_by_group(y_true, y_pred, race)
        >>> print(cm['group_a'])
    """
    from sklearn.metrics import confusion_matrix

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    results = {}
    for group in np.unique(sensitive_attr):
        mask = sensitive_attr == group
        cm = confusion_matrix(y_true[mask], y_pred[mask])
        results[str(group)] = cm

    return results


def bootstrap_metric(
    metric_func,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    sensitive_attr: np.ndarray,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95
) -> Tuple[float, float, float]:
    """Compute metric with bootstrap confidence intervals.

    Args:
        metric_func: Metric function to compute
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute
        n_bootstrap: Number of bootstrap samples
        confidence_level: Confidence level (default: 0.95 for 95% CI)

    Returns:
        tuple: (metric_value, lower_bound, upper_bound)

    Example:
        >>> from src.metrics import demographic_parity_difference
        >>> val, lower, upper = bootstrap_metric(
        >>>     demographic_parity_difference,
        >>>     y_true, y_pred, sensitive_attr
        >>> )
        >>> print(f"Metric: {val:.3f} [{lower:.3f}, {upper:.3f}]")
    """
    n = len(y_true)
    bootstrap_values = []

    for _ in range(n_bootstrap):
        # Sample with replacement
        indices = np.random.choice(n, size=n, replace=True)
        y_true_sample = y_true[indices]
        y_pred_sample = y_pred[indices]
        sensitive_sample = sensitive_attr[indices]

        # Compute metric
        try:
            value = metric_func(y_true_sample, y_pred_sample, sensitive_sample)
            bootstrap_values.append(value)
        except:
            # Skip if metric computation fails
            pass

    bootstrap_values = np.array(bootstrap_values)

    # Compute confidence interval
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100

    lower = np.percentile(bootstrap_values, lower_percentile)
    upper = np.percentile(bootstrap_values, upper_percentile)

    # Compute original metric
    original_value = metric_func(y_true, y_pred, sensitive_attr)

    return original_value, lower, upper


def format_metric(value: float, name: str = None) -> str:
    """Format metric value for display.

    Args:
        value: Metric value
        name: Optional metric name for context

    Returns:
        str: Formatted string

    Example:
        >>> print(format_metric(0.15432, "Demographic Parity"))
        Demographic Parity: 0.154
    """
    if name:
        return f"{name}: {value:.3f}"
    else:
        return f"{value:.3f}"


def generate_summary_report(
    metrics: dict,
    thresholds: dict = None
) -> str:
    """Generate human-readable summary report.

    Args:
        metrics: Dictionary of metric values
        thresholds: Optional dictionary of thresholds for each metric

    Returns:
        str: Formatted report

    Example:
        >>> metrics = {'demographic_parity': 0.15, 'equalized_odds': 0.08}
        >>> print(generate_summary_report(metrics))
    """
    from src.metrics import FAIRNESS_THRESHOLDS, is_fair

    if thresholds is None:
        thresholds = FAIRNESS_THRESHOLDS

    lines = [
        "=" * 60,
        "FAIRNESS METRICS SUMMARY",
        "=" * 60,
        ""
    ]

    for metric_name, value in metrics.items():
        fair = is_fair(value, metric_name)
        status = "✓ PASS" if fair else "✗ FAIL"
        threshold = thresholds.get(metric_name, 0.1)

        lines.append(f"{metric_name}:")
        lines.append(f"  Value: {value:.4f}")
        lines.append(f"  Threshold: {threshold:.4f}")
        lines.append(f"  Status: {status}")
        lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path: Path to project root
    """
    # Assuming this file is in src/
    return Path(__file__).parent.parent


def ensure_dir(directory: Union[str, Path]) -> Path:
    """Ensure directory exists, create if needed.

    Args:
        directory: Directory path

    Returns:
        Path: Path object for the directory
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
