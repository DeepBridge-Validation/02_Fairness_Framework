"""
Fairness Detector - Main class for automated bias detection

This module provides the main FairnessDetector class for detecting and
analyzing fairness violations in machine learning models.

Example:
    >>> from src.fairness_detector import FairnessDetector
    >>> import pandas as pd
    >>>
    >>> # Load data
    >>> df = pd.read_csv("data.csv")
    >>>
    >>> # Initialize detector
    >>> detector = FairnessDetector()
    >>> detector.set_sensitive_attributes(['race', 'sex'])
    >>> detector.set_target('target')
    >>>
    >>> # Detect bias
    >>> results = detector.detect_bias(df)
    >>> print(results.summary())
"""

from typing import List, Optional, Dict, Any, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class BiasDetectionResult:
    """Results from bias detection analysis.

    Attributes:
        has_bias: Whether bias was detected
        bias_type: Type of bias detected (demographic_parity, equalized_odds, etc.)
        metrics: Dictionary of fairness metric values
        sensitive_attrs: List of sensitive attributes analyzed
        recommendations: List of recommendations for mitigation
    """
    has_bias: bool
    bias_type: Optional[str] = None
    metrics: Dict[str, float] = None
    sensitive_attrs: List[str] = None
    recommendations: List[str] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}
        if self.sensitive_attrs is None:
            self.sensitive_attrs = []
        if self.recommendations is None:
            self.recommendations = []

    def summary(self) -> str:
        """Generate a human-readable summary of results.

        Returns:
            str: Formatted summary string
        """
        lines = [
            "=" * 60,
            "FAIRNESS ANALYSIS RESULTS",
            "=" * 60,
        ]

        # Bias status
        status = "BIAS DETECTED ⚠️" if self.has_bias else "NO BIAS DETECTED ✓"
        lines.append(f"\nStatus: {status}")

        # Bias type
        if self.bias_type:
            lines.append(f"Bias Type: {self.bias_type}")

        # Metrics
        if self.metrics:
            lines.append("\nFairness Metrics:")
            for metric, value in self.metrics.items():
                lines.append(f"  - {metric}: {value:.4f}")

        # Sensitive attributes
        if self.sensitive_attrs:
            lines.append(f"\nSensitive Attributes: {', '.join(self.sensitive_attrs)}")

        # Recommendations
        if self.recommendations:
            lines.append("\nRecommendations:")
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"  {i}. {rec}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def plot(self):
        """Generate visualization of results.

        Note:
            This will create matplotlib plots showing fairness metrics
            and group comparisons.
        """
        # TODO: Implement visualization
        from src.visualization import plot_fairness_report
        plot_fairness_report(self)


class FairnessDetector:
    """Main class for automated fairness detection.

    This class provides methods to detect various types of bias in datasets
    and machine learning predictions, including:
    - Demographic parity violations
    - Equalized odds violations
    - Equal opportunity violations
    - EEOC/ECOA compliance checking

    Attributes:
        sensitive_attributes: List of column names for protected attributes
        target: Name of the target/label column
        threshold: Threshold for bias detection (default: 0.1)
        verbose: Whether to print detailed information

    Example:
        >>> detector = FairnessDetector()
        >>> detector.set_sensitive_attributes(['race'])
        >>> detector.set_target('income')
        >>> results = detector.detect_bias(data)
    """

    def __init__(self, threshold: float = 0.1, verbose: bool = False):
        """Initialize FairnessDetector.

        Args:
            threshold: Threshold for bias detection (0.0 to 1.0)
            verbose: Whether to print detailed information during analysis
        """
        self.sensitive_attributes: List[str] = []
        self.target: Optional[str] = None
        self.threshold = threshold
        self.verbose = verbose
        self._data: Optional[pd.DataFrame] = None

    def set_sensitive_attributes(self, attributes: List[str]) -> None:
        """Set the sensitive/protected attributes to analyze.

        Args:
            attributes: List of column names for protected attributes
                       (e.g., ['race', 'sex', 'age'])
        """
        self.sensitive_attributes = attributes
        if self.verbose:
            print(f"Set sensitive attributes: {attributes}")

    def set_target(self, target: str) -> None:
        """Set the target/label column.

        Args:
            target: Name of the target column
        """
        self.target = target
        if self.verbose:
            print(f"Set target: {target}")

    def set_threshold(self, threshold: float) -> None:
        """Set the threshold for bias detection.

        Args:
            threshold: Threshold value (typically 0.1 for 10% difference)

        Raises:
            ValueError: If threshold is not between 0 and 1
        """
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")
        self.threshold = threshold

    def set_verbose(self, verbose: bool) -> None:
        """Enable or disable verbose output.

        Args:
            verbose: Whether to print detailed information
        """
        self.verbose = verbose

    def load_data(self,
                  data: Union[pd.DataFrame, str],
                  target: Optional[str] = None,
                  sensitive_attrs: Optional[List[str]] = None) -> None:
        """Load data for analysis.

        Args:
            data: DataFrame or path to CSV file
            target: Name of target column (optional if already set)
            sensitive_attrs: List of sensitive attributes (optional if already set)

        Raises:
            ValueError: If data is invalid or required columns are missing
        """
        # Load data
        if isinstance(data, str):
            self._data = pd.read_csv(data)
        else:
            self._data = data.copy()

        # Set target and sensitive attributes if provided
        if target:
            self.set_target(target)
        if sensitive_attrs:
            self.set_sensitive_attributes(sensitive_attrs)

        # Validate
        if self.target and self.target not in self._data.columns:
            raise ValueError(f"Target column '{self.target}' not found in data")

        for attr in self.sensitive_attributes:
            if attr not in self._data.columns:
                raise ValueError(f"Sensitive attribute '{attr}' not found in data")

        if self.verbose:
            print(f"Loaded data: {self._data.shape[0]} rows, {self._data.shape[1]} columns")

    def detect_bias(self,
                   data: Optional[pd.DataFrame] = None,
                   y_pred: Optional[np.ndarray] = None) -> BiasDetectionResult:
        """Detect bias in data or predictions.

        Args:
            data: DataFrame to analyze (uses loaded data if None)
            y_pred: Predictions to analyze (uses target column if None)

        Returns:
            BiasDetectionResult: Object containing detection results

        Raises:
            ValueError: If no data is available or configuration is incomplete
        """
        # Use provided data or loaded data
        if data is not None:
            df = data
        elif self._data is not None:
            df = self._data
        else:
            raise ValueError("No data provided. Call load_data() or pass data parameter.")

        # Validate configuration
        if not self.sensitive_attributes:
            raise ValueError("No sensitive attributes set. Call set_sensitive_attributes().")
        if not self.target and y_pred is None:
            raise ValueError("No target set and no predictions provided.")

        # Get predictions
        if y_pred is None:
            y = df[self.target].values
        else:
            y = y_pred

        # Perform bias detection
        from src.metrics import (
            demographic_parity_difference,
            equalized_odds_difference,
            equal_opportunity_difference
        )

        results = {
            'demographic_parity': demographic_parity_difference(
                y, df[self.sensitive_attributes[0]]
            ),
            'equalized_odds': equalized_odds_difference(
                df[self.target], y, df[self.sensitive_attributes[0]]
            ),
            'equal_opportunity': equal_opportunity_difference(
                df[self.target], y, df[self.sensitive_attributes[0]]
            )
        }

        # Determine if bias exists
        has_bias = any(abs(v) > self.threshold for v in results.values())

        # Identify bias type
        bias_type = None
        if has_bias:
            max_metric = max(results.items(), key=lambda x: abs(x[1]))
            bias_type = max_metric[0]

        # Generate recommendations
        recommendations = []
        if has_bias:
            recommendations.append("Review data collection process for potential bias")
            recommendations.append("Consider bias mitigation techniques (reweighting, resampling)")
            recommendations.append("Evaluate model fairness across all protected groups")
            recommendations.append("Consult fairness documentation for mitigation strategies")

        return BiasDetectionResult(
            has_bias=has_bias,
            bias_type=bias_type,
            metrics=results,
            sensitive_attrs=self.sensitive_attributes,
            recommendations=recommendations
        )

    def check_eeoc_compliance(self, data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Check EEOC (Equal Employment Opportunity Commission) compliance.

        Implements the 80% rule: selection rate for any group should be at least
        80% of the rate for the group with the highest selection rate.

        Args:
            data: DataFrame to check (uses loaded data if None)

        Returns:
            dict: Compliance results including pass/fail and rates by group
        """
        # TODO: Implement EEOC compliance checking
        # This should implement the 80% rule
        raise NotImplementedError("EEOC compliance checking coming soon")

    def check_ecoa_compliance(self, data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Check ECOA (Equal Credit Opportunity Act) compliance.

        Args:
            data: DataFrame to check (uses loaded data if None)

        Returns:
            dict: Compliance results
        """
        # TODO: Implement ECOA compliance checking
        raise NotImplementedError("ECOA compliance checking coming soon")

    def analyze(self, data: Optional[pd.DataFrame] = None) -> BiasDetectionResult:
        """Perform comprehensive fairness analysis.

        This method runs all available fairness checks and generates
        a complete report.

        Args:
            data: DataFrame to analyze (uses loaded data if None)

        Returns:
            BiasDetectionResult: Comprehensive analysis results
        """
        return self.detect_bias(data)
