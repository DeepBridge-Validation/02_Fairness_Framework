"""
Fairness Metrics

This module implements various fairness metrics for bias detection,
including:
- Demographic Parity
- Equalized Odds
- Equal Opportunity
- Disparate Impact
- And more...

All metrics follow standard definitions from fairness literature.
"""

from typing import Union, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def demographic_parity_difference(
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate demographic parity difference.

    Demographic parity is satisfied when P(Y_pred=1|A=0) = P(Y_pred=1|A=1)
    The difference measures the violation of this condition.

    Args:
        y_pred: Predicted labels (0 or 1)
        sensitive_attr: Sensitive attribute values

    Returns:
        float: Demographic parity difference (0 = perfect parity)

    Example:
        >>> y_pred = [1, 0, 1, 1, 0]
        >>> sensitive = ['A', 'B', 'A', 'B', 'A']
        >>> dp = demographic_parity_difference(y_pred, sensitive)
        >>> print(f"DP Difference: {dp:.3f}")
    """
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    # Get unique groups
    groups = np.unique(sensitive_attr)
    if len(groups) != 2:
        raise ValueError("Currently only supports binary sensitive attributes")

    # Calculate positive rates for each group
    rate_0 = np.mean(y_pred[sensitive_attr == groups[0]])
    rate_1 = np.mean(y_pred[sensitive_attr == groups[1]])

    return rate_1 - rate_0


def equalized_odds_difference(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate equalized odds difference.

    Equalized odds requires:
    - P(Y_pred=1|Y=1,A=0) = P(Y_pred=1|Y=1,A=1) (equal TPR)
    - P(Y_pred=1|Y=0,A=0) = P(Y_pred=1|Y=0,A=1) (equal FPR)

    This returns the maximum difference between groups.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        float: Maximum equalized odds difference

    Example:
        >>> y_true = [1, 0, 1, 0, 1]
        >>> y_pred = [1, 0, 1, 1, 0]
        >>> sensitive = ['A', 'B', 'A', 'B', 'A']
        >>> eo = equalized_odds_difference(y_true, y_pred, sensitive)
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    if len(groups) != 2:
        raise ValueError("Currently only supports binary sensitive attributes")

    # Calculate TPR and FPR for each group
    tpr_diff = _tpr_difference(y_true, y_pred, sensitive_attr, groups)
    fpr_diff = _fpr_difference(y_true, y_pred, sensitive_attr, groups)

    # Return maximum difference
    return max(abs(tpr_diff), abs(fpr_diff))


def equal_opportunity_difference(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate equal opportunity difference.

    Equal opportunity requires equal true positive rates:
    P(Y_pred=1|Y=1,A=0) = P(Y_pred=1|Y=1,A=1)

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        float: True positive rate difference

    Example:
        >>> y_true = [1, 0, 1, 0, 1]
        >>> y_pred = [1, 0, 1, 1, 0]
        >>> sensitive = ['A', 'B', 'A', 'B', 'A']
        >>> eop = equal_opportunity_difference(y_true, y_pred, sensitive)
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    if len(groups) != 2:
        raise ValueError("Currently only supports binary sensitive attributes")

    return _tpr_difference(y_true, y_pred, sensitive_attr, groups)


def disparate_impact_ratio(
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate disparate impact ratio.

    Disparate impact is the ratio of positive prediction rates:
    DI = P(Y_pred=1|A=1) / P(Y_pred=1|A=0)

    A ratio < 0.8 often indicates bias (80% rule).

    Args:
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        float: Disparate impact ratio (1.0 = perfect fairness)

    Example:
        >>> y_pred = [1, 0, 1, 1, 0]
        >>> sensitive = ['A', 'B', 'A', 'B', 'A']
        >>> di = disparate_impact_ratio(y_pred, sensitive)
        >>> print(f"DI Ratio: {di:.3f}")
        >>> if di < 0.8:
        >>>     print("Warning: Potential disparate impact")
    """
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    if len(groups) != 2:
        raise ValueError("Currently only supports binary sensitive attributes")

    rate_0 = np.mean(y_pred[sensitive_attr == groups[0]])
    rate_1 = np.mean(y_pred[sensitive_attr == groups[1]])

    # Avoid division by zero
    if rate_0 == 0:
        return 0.0 if rate_1 == 0 else float('inf')

    return rate_1 / rate_0


def statistical_parity_difference(
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate statistical parity difference.

    This is an alias for demographic_parity_difference.

    Args:
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        float: Statistical parity difference
    """
    return demographic_parity_difference(y_pred, sensitive_attr)


def average_odds_difference(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> float:
    """Calculate average odds difference.

    This is the average of TPR and FPR differences.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        float: Average odds difference
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    sensitive_attr = np.array(sensitive_attr)

    groups = np.unique(sensitive_attr)
    if len(groups) != 2:
        raise ValueError("Currently only supports binary sensitive attributes")

    tpr_diff = _tpr_difference(y_true, y_pred, sensitive_attr, groups)
    fpr_diff = _fpr_difference(y_true, y_pred, sensitive_attr, groups)

    return (abs(tpr_diff) + abs(fpr_diff)) / 2


def compute_all_metrics(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series],
    sensitive_attr: Union[np.ndarray, pd.Series]
) -> dict:
    """Compute all fairness metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        sensitive_attr: Sensitive attribute values

    Returns:
        dict: Dictionary with all metric values

    Example:
        >>> metrics = compute_all_metrics(y_true, y_pred, sensitive)
        >>> for name, value in metrics.items():
        >>>     print(f"{name}: {value:.4f}")
    """
    return {
        'demographic_parity': demographic_parity_difference(y_pred, sensitive_attr),
        'equalized_odds': equalized_odds_difference(y_true, y_pred, sensitive_attr),
        'equal_opportunity': equal_opportunity_difference(y_true, y_pred, sensitive_attr),
        'disparate_impact': disparate_impact_ratio(y_pred, sensitive_attr),
        'average_odds': average_odds_difference(y_true, y_pred, sensitive_attr),
    }


# ============================================================================
# Helper Functions
# ============================================================================

def _tpr_difference(y_true, y_pred, sensitive_attr, groups):
    """Calculate true positive rate difference between groups."""
    # Group 0
    mask_0_pos = (sensitive_attr == groups[0]) & (y_true == 1)
    if mask_0_pos.sum() == 0:
        tpr_0 = 0.0
    else:
        tpr_0 = np.mean(y_pred[mask_0_pos])

    # Group 1
    mask_1_pos = (sensitive_attr == groups[1]) & (y_true == 1)
    if mask_1_pos.sum() == 0:
        tpr_1 = 0.0
    else:
        tpr_1 = np.mean(y_pred[mask_1_pos])

    return tpr_1 - tpr_0


def _fpr_difference(y_true, y_pred, sensitive_attr, groups):
    """Calculate false positive rate difference between groups."""
    # Group 0
    mask_0_neg = (sensitive_attr == groups[0]) & (y_true == 0)
    if mask_0_neg.sum() == 0:
        fpr_0 = 0.0
    else:
        fpr_0 = np.mean(y_pred[mask_0_neg])

    # Group 1
    mask_1_neg = (sensitive_attr == groups[1]) & (y_true == 0)
    if mask_1_neg.sum() == 0:
        fpr_1 = 0.0
    else:
        fpr_1 = np.mean(y_pred[mask_1_neg])

    return fpr_1 - fpr_0


def _tnr_difference(y_true, y_pred, sensitive_attr, groups):
    """Calculate true negative rate difference between groups."""
    # Group 0
    mask_0_neg = (sensitive_attr == groups[0]) & (y_true == 0)
    if mask_0_neg.sum() == 0:
        tnr_0 = 0.0
    else:
        tnr_0 = 1 - np.mean(y_pred[mask_0_neg])

    # Group 1
    mask_1_neg = (sensitive_attr == groups[1]) & (y_true == 0)
    if mask_1_neg.sum() == 0:
        tnr_1 = 0.0
    else:
        tnr_1 = 1 - np.mean(y_pred[mask_1_neg])

    return tnr_1 - tnr_0


# ============================================================================
# Metric Thresholds (commonly used in literature)
# ============================================================================

FAIRNESS_THRESHOLDS = {
    'demographic_parity': 0.1,      # 10% difference
    'equalized_odds': 0.1,           # 10% difference
    'equal_opportunity': 0.1,        # 10% difference
    'disparate_impact': 0.8,         # 80% rule (ratio)
    'average_odds': 0.1,             # 10% difference
}


def is_fair(metric_value: float, metric_name: str) -> bool:
    """Check if a metric value indicates fairness.

    Args:
        metric_value: The computed metric value
        metric_name: Name of the metric

    Returns:
        bool: True if fair, False if biased

    Example:
        >>> dp = demographic_parity_difference(y_pred, sensitive)
        >>> if is_fair(dp, 'demographic_parity'):
        >>>     print("Fair!")
        >>> else:
        >>>     print("Biased!")
    """
    threshold = FAIRNESS_THRESHOLDS.get(metric_name, 0.1)

    if metric_name == 'disparate_impact':
        # For disparate impact, check if ratio is close to 1.0
        return threshold <= metric_value <= (2 - threshold)
    else:
        # For differences, check if absolute value is below threshold
        return abs(metric_value) <= threshold
