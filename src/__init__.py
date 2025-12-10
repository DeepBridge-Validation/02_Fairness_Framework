"""
Fairness Framework for Machine Learning

An automated framework for fairness detection and bias mitigation in machine
learning systems with regulatory compliance (EEOC/ECOA).

Modules:
    - fairness_detector: Main detector class for bias detection
    - metrics: Fairness metrics and calculations
    - visualization: Plotting and reporting utilities
    - utils: General utility functions

Example:
    >>> from src.fairness_detector import FairnessDetector
    >>> detector = FairnessDetector()
    >>> results = detector.detect_bias(data)
"""

__version__ = "1.0.0"
__author__ = "Gustavo Haase"
__license__ = "MIT"

# Core imports
from .fairness_detector import FairnessDetector, BiasDetectionResult
from .metrics import (
    demographic_parity_difference,
    equalized_odds_difference,
    equal_opportunity_difference,
    disparate_impact_ratio,
    compute_all_metrics,
    is_fair,
)
from .visualization import (
    plot_fairness_report,
    plot_metric_comparison,
    plot_group_comparison,
    create_fairness_dashboard,
)
from .utils import (
    load_dataset,
    save_results,
    group_statistics,
)

__all__ = [
    # Main classes
    "FairnessDetector",
    "BiasDetectionResult",
    # Metrics
    "demographic_parity_difference",
    "equalized_odds_difference",
    "equal_opportunity_difference",
    "disparate_impact_ratio",
    "compute_all_metrics",
    "is_fair",
    # Visualization
    "plot_fairness_report",
    "plot_metric_comparison",
    "plot_group_comparison",
    "create_fairness_dashboard",
    # Utils
    "load_dataset",
    "save_results",
    "group_statistics",
]
