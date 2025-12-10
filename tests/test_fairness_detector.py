"""
Unit tests for FairnessDetector class.

Run tests:
    pytest tests/test_fairness_detector.py -v
"""

import pytest
import numpy as np
import pandas as pd
from src.fairness_detector import FairnessDetector, BiasDetectionResult


class TestFairnessDetectorInit:
    """Tests for FairnessDetector initialization."""

    def test_default_initialization(self):
        """Test default initialization."""
        detector = FairnessDetector()
        assert detector.threshold == 0.1
        assert detector.verbose == False
        assert detector.sensitive_attributes == []
        assert detector.target is None

    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        detector = FairnessDetector(threshold=0.05, verbose=True)
        assert detector.threshold == 0.05
        assert detector.verbose == True

    def test_invalid_threshold(self):
        """Test that invalid threshold raises error."""
        detector = FairnessDetector()
        with pytest.raises(ValueError, match="between 0 and 1"):
            detector.set_threshold(1.5)


class TestFairnessDetectorConfiguration:
    """Tests for detector configuration."""

    def test_set_sensitive_attributes(self):
        """Test setting sensitive attributes."""
        detector = FairnessDetector()
        detector.set_sensitive_attributes(['race', 'sex'])
        assert detector.sensitive_attributes == ['race', 'sex']

    def test_set_target(self):
        """Test setting target column."""
        detector = FairnessDetector()
        detector.set_target('income')
        assert detector.target == 'income'

    def test_set_threshold(self):
        """Test setting threshold."""
        detector = FairnessDetector()
        detector.set_threshold(0.05)
        assert detector.threshold == 0.05

    def test_set_verbose(self):
        """Test setting verbose mode."""
        detector = FairnessDetector()
        detector.set_verbose(True)
        assert detector.verbose == True


class TestLoadData:
    """Tests for loading data."""

    def test_load_dataframe(self):
        """Test loading pandas DataFrame."""
        df = pd.DataFrame({
            'feature': [1, 2, 3, 4],
            'sensitive': ['A', 'B', 'A', 'B'],
            'target': [0, 1, 0, 1]
        })

        detector = FairnessDetector()
        detector.load_data(df, target='target', sensitive_attrs=['sensitive'])

        assert detector.target == 'target'
        assert detector.sensitive_attributes == ['sensitive']

    def test_load_missing_target(self):
        """Test that loading data with missing target raises error."""
        df = pd.DataFrame({
            'feature': [1, 2, 3],
            'sensitive': ['A', 'B', 'A']
        })

        detector = FairnessDetector()
        detector.set_target('missing_column')

        with pytest.raises(ValueError, match="not found in data"):
            detector.load_data(df)

    def test_load_missing_sensitive(self):
        """Test that loading data with missing sensitive attr raises error."""
        df = pd.DataFrame({
            'feature': [1, 2, 3],
            'target': [0, 1, 0]
        })

        detector = FairnessDetector()
        detector.set_sensitive_attributes(['missing_column'])

        with pytest.raises(ValueError, match="not found in data"):
            detector.load_data(df)


class TestBiasDetection:
    """Tests for bias detection."""

    def test_detect_no_bias(self):
        """Test detection when no bias is present."""
        df = pd.DataFrame({
            'feature': range(10),
            'sensitive': ['A', 'B'] * 5,
            'target': [1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
        })

        detector = FairnessDetector(threshold=0.1)
        detector.load_data(df, target='target', sensitive_attrs=['sensitive'])
        results = detector.detect_bias()

        assert isinstance(results, BiasDetectionResult)
        assert results.has_bias == False or abs(results.metrics.get('demographic_parity', 0)) < 0.1

    def test_detect_bias_present(self):
        """Test detection when bias is present."""
        # Create data with clear bias
        df = pd.DataFrame({
            'feature': range(10),
            'sensitive': ['A'] * 5 + ['B'] * 5,
            'target': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]  # All A=1, all B=0
        })

        detector = FairnessDetector(threshold=0.1)
        detector.load_data(df, target='target', sensitive_attrs=['sensitive'])
        results = detector.detect_bias()

        assert results.has_bias == True
        assert results.bias_type is not None
        assert len(results.recommendations) > 0

    def test_detect_without_configuration(self):
        """Test that detection without configuration raises error."""
        df = pd.DataFrame({
            'feature': [1, 2, 3],
            'sensitive': ['A', 'B', 'A'],
            'target': [0, 1, 0]
        })

        detector = FairnessDetector()

        with pytest.raises(ValueError):
            detector.detect_bias(df)

    def test_metrics_in_results(self):
        """Test that results contain metrics."""
        df = pd.DataFrame({
            'feature': range(10),
            'sensitive': ['A', 'B'] * 5,
            'target': [1, 0] * 5
        })

        detector = FairnessDetector()
        detector.load_data(df, target='target', sensitive_attrs=['sensitive'])
        results = detector.detect_bias()

        assert 'demographic_parity' in results.metrics
        assert 'equalized_odds' in results.metrics
        assert 'equal_opportunity' in results.metrics


class TestEEOCCompliance:
    """Tests for EEOC compliance checking."""

    def test_eeoc_compliant(self):
        """Test case that is EEOC compliant."""
        # Group A: 90% selection rate
        # Group B: 80% selection rate
        # Ratio: 80/90 = 0.889 > 0.8 ✓
        df = pd.DataFrame({
            'sensitive': ['A'] * 10 + ['B'] * 10,
            'hired': [1] * 9 + [0] * 1 + [1] * 8 + [0] * 2
        })

        detector = FairnessDetector()
        detector.load_data(df, target='hired', sensitive_attrs=['sensitive'])
        compliance = detector.check_eeoc_compliance()

        assert compliance['compliant'] == True
        assert compliance['impact_ratio'] >= 0.8
        assert compliance['regulation'] == 'EEOC 80% Rule'

    def test_eeoc_non_compliant(self):
        """Test case that is not EEOC compliant."""
        # Group A: 100% selection rate
        # Group B: 50% selection rate
        # Ratio: 50/100 = 0.5 < 0.8 ✗
        df = pd.DataFrame({
            'sensitive': ['A'] * 10 + ['B'] * 10,
            'hired': [1] * 10 + [1] * 5 + [0] * 5
        })

        detector = FairnessDetector()
        detector.load_data(df, target='hired', sensitive_attrs=['sensitive'])
        compliance = detector.check_eeoc_compliance()

        assert compliance['compliant'] == False
        assert compliance['impact_ratio'] < 0.8
        assert len(compliance['failing_groups']) > 0

    def test_eeoc_edge_case_no_selection(self):
        """Test EEOC with no selection for any group."""
        df = pd.DataFrame({
            'sensitive': ['A'] * 5 + ['B'] * 5,
            'hired': [0] * 10
        })

        detector = FairnessDetector()
        detector.load_data(df, target='hired', sensitive_attrs=['sensitive'])
        compliance = detector.check_eeoc_compliance()

        assert compliance['compliant'] == True  # No disparate impact if no selection


class TestECOACompliance:
    """Tests for ECOA compliance checking."""

    def test_ecoa_compliant(self):
        """Test case that is ECOA compliant."""
        # Similar to EEOC but for credit decisions
        df = pd.DataFrame({
            'sensitive': ['A'] * 10 + ['B'] * 10,
            'approved': [1] * 9 + [0] * 1 + [1] * 8 + [0] * 2
        })

        detector = FairnessDetector()
        detector.load_data(df, target='approved', sensitive_attrs=['sensitive'])
        compliance = detector.check_ecoa_compliance()

        assert compliance['compliant'] == True
        assert compliance['disparate_impact'] >= 0.8

    def test_ecoa_non_compliant(self):
        """Test case that is not ECOA compliant."""
        df = pd.DataFrame({
            'sensitive': ['A'] * 10 + ['B'] * 10,
            'approved': [1] * 10 + [1] * 5 + [0] * 5
        })

        detector = FairnessDetector()
        detector.load_data(df, target='approved', sensitive_attrs=['sensitive'])
        compliance = detector.check_ecoa_compliance()

        assert compliance['compliant'] == False
        assert len(compliance['disadvantaged_groups']) > 0
        assert 'rate_differences' in compliance


class TestBiasDetectionResult:
    """Tests for BiasDetectionResult dataclass."""

    def test_result_initialization(self):
        """Test BiasDetectionResult initialization."""
        result = BiasDetectionResult(
            has_bias=True,
            bias_type='demographic_parity',
            metrics={'dp': 0.15},
            sensitive_attrs=['race'],
            recommendations=['Fix bias']
        )

        assert result.has_bias == True
        assert result.bias_type == 'demographic_parity'
        assert len(result.recommendations) == 1

    def test_result_summary(self):
        """Test summary generation."""
        result = BiasDetectionResult(
            has_bias=True,
            bias_type='demographic_parity',
            metrics={'demographic_parity': 0.15},
            sensitive_attrs=['race']
        )

        summary = result.summary()
        assert 'BIAS DETECTED' in summary
        assert 'demographic_parity' in summary
        assert '0.15' in summary


class TestAnalyzeMethod:
    """Tests for comprehensive analyze method."""

    def test_analyze_returns_results(self):
        """Test that analyze returns BiasDetectionResult."""
        df = pd.DataFrame({
            'feature': range(10),
            'sensitive': ['A', 'B'] * 5,
            'target': [1, 0] * 5
        })

        detector = FairnessDetector()
        detector.load_data(df, target='target', sensitive_attrs=['sensitive'])
        results = detector.analyze()

        assert isinstance(results, BiasDetectionResult)
        assert results.metrics is not None


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
