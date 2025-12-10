"""
Unit tests for fairness metrics module.

Run tests:
    pytest tests/test_metrics.py -v
    pytest tests/test_metrics.py::test_demographic_parity -v
"""

import pytest
import numpy as np
from src.metrics import (
    demographic_parity_difference,
    equalized_odds_difference,
    equal_opportunity_difference,
    disparate_impact_ratio,
    statistical_parity_difference,
    average_odds_difference,
    compute_all_metrics,
    is_fair,
)


class TestDemographicParity:
    """Tests for demographic parity metric."""

    def test_perfect_parity(self):
        """Test case where groups have equal positive rates."""
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        assert abs(dp) < 0.001, "Perfect parity should give ~0 difference"

    def test_bias_present(self):
        """Test case with clear bias."""
        y_pred = np.array([1, 1, 1, 0, 0, 0])
        sensitive = np.array(['A', 'A', 'A', 'B', 'B', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        assert abs(dp - 1.0) < 0.001, "Should detect 100% difference"

    def test_partial_bias(self):
        """Test case with partial bias."""
        # Group A: 2/3 positive (0.667)
        # Group B: 1/3 positive (0.333)
        y_pred = np.array([1, 1, 0, 1, 0, 0])
        sensitive = np.array(['A', 'A', 'A', 'B', 'B', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        expected = 0.333 - 0.667  # B - A
        assert abs(dp - expected) < 0.01, f"Expected {expected}, got {dp}"


class TestEqualizedOdds:
    """Tests for equalized odds metric."""

    def test_perfect_equalized_odds(self):
        """Test case with perfect equalized odds."""
        y_true = np.array([1, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        eo = equalized_odds_difference(y_true, y_pred, sensitive)
        assert eo == 0.0, "Perfect predictions should give 0 difference"

    def test_bias_in_tpr(self):
        """Test case with different TPR across groups."""
        # Group A: TPR = 1.0, Group B: TPR = 0.0
        y_true = np.array([1, 1, 1, 1, 0, 0])
        y_pred = np.array([1, 1, 0, 0, 0, 0])
        sensitive = np.array(['A', 'A', 'B', 'B', 'A', 'B'])

        eo = equalized_odds_difference(y_true, y_pred, sensitive)
        assert eo > 0.5, "Should detect significant TPR difference"


class TestEqualOpportunity:
    """Tests for equal opportunity metric."""

    def test_equal_tpr(self):
        """Test case with equal TPR across groups."""
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 1, 1])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        eop = equal_opportunity_difference(y_true, y_pred, sensitive)
        assert eop == 0.0, "Equal TPR should give 0"

    def test_different_tpr(self):
        """Test case with different TPR."""
        # Group A: TPR = 1.0 (2/2)
        # Group B: TPR = 0.5 (1/2)
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 1, 0])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        eop = equal_opportunity_difference(y_true, y_pred, sensitive)
        expected = 0.5 - 1.0  # B - A
        assert abs(eop - expected) < 0.01


class TestDisparateImpact:
    """Tests for disparate impact ratio."""

    def test_no_disparate_impact(self):
        """Test case with no disparate impact."""
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        di = disparate_impact_ratio(y_pred, sensitive)
        assert abs(di - 1.0) < 0.001, "Equal rates should give ratio ~1.0"

    def test_disparate_impact_present(self):
        """Test case with disparate impact."""
        # Group A: 100% positive
        # Group B: 50% positive
        # Ratio = 0.5
        y_pred = np.array([1, 1, 1, 1, 0, 0])
        sensitive = np.array(['A', 'A', 'B', 'B', 'B', 'B'])

        di = disparate_impact_ratio(y_pred, sensitive)
        # B/A = 0.5/1.0 = 0.5
        assert abs(di - 0.5) < 0.01

    def test_80_percent_rule_pass(self):
        """Test case that passes 80% rule."""
        # Group A: 100% (1.0)
        # Group B: 85% (0.85)
        # Ratio = 0.85 > 0.8 ✓
        y_pred = np.array([1]*10 + [1]*8 + [0]*2)
        sensitive = np.array(['A']*10 + ['B']*10)

        di = disparate_impact_ratio(y_pred, sensitive)
        assert di >= 0.8, "Should pass 80% rule"

    def test_80_percent_rule_fail(self):
        """Test case that fails 80% rule."""
        # Group A: 100% (1.0)
        # Group B: 70% (0.70)
        # Ratio = 0.70 < 0.8 ✗
        y_pred = np.array([1]*10 + [1]*7 + [0]*3)
        sensitive = np.array(['A']*10 + ['B']*10)

        di = disparate_impact_ratio(y_pred, sensitive)
        assert di < 0.8, "Should fail 80% rule"


class TestComputeAllMetrics:
    """Tests for compute_all_metrics function."""

    def test_all_metrics_returned(self):
        """Test that all metrics are computed."""
        y_true = np.array([1, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        metrics = compute_all_metrics(y_true, y_pred, sensitive)

        expected_keys = [
            'demographic_parity',
            'equalized_odds',
            'equal_opportunity',
            'disparate_impact',
            'average_odds'
        ]

        for key in expected_keys:
            assert key in metrics, f"Missing metric: {key}"

    def test_metric_values_reasonable(self):
        """Test that metric values are in reasonable ranges."""
        y_true = np.array([1, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        metrics = compute_all_metrics(y_true, y_pred, sensitive)

        # Check ranges
        for key, value in metrics.items():
            assert isinstance(value, (int, float)), f"{key} should be numeric"
            if key == 'disparate_impact':
                assert value >= 0, f"{key} should be non-negative"
            # Other metrics can be negative (differences)


class TestIsFair:
    """Tests for is_fair function."""

    def test_fair_demographic_parity(self):
        """Test fair classification for demographic parity."""
        assert is_fair(0.05, 'demographic_parity') == True
        assert is_fair(-0.05, 'demographic_parity') == True
        assert is_fair(0.15, 'demographic_parity') == False
        assert is_fair(-0.15, 'demographic_parity') == False

    def test_fair_disparate_impact(self):
        """Test fair classification for disparate impact."""
        assert is_fair(0.85, 'disparate_impact') == True
        assert is_fair(1.0, 'disparate_impact') == True
        assert is_fair(1.15, 'disparate_impact') == True
        assert is_fair(0.75, 'disparate_impact') == False
        assert is_fair(0.5, 'disparate_impact') == False

    def test_boundary_cases(self):
        """Test boundary cases."""
        # Exactly at threshold
        assert is_fair(0.1, 'demographic_parity') == True
        assert is_fair(-0.1, 'demographic_parity') == True
        assert is_fair(0.8, 'disparate_impact') == True


class TestStatisticalParity:
    """Tests for statistical parity (alias of demographic parity)."""

    def test_same_as_demographic_parity(self):
        """Test that statistical parity equals demographic parity."""
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        sp = statistical_parity_difference(y_pred, sensitive)

        assert dp == sp, "Statistical parity should equal demographic parity"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_arrays(self):
        """Test with empty arrays."""
        y_pred = np.array([])
        sensitive = np.array([])

        with pytest.raises(Exception):
            demographic_parity_difference(y_pred, sensitive)

    def test_single_group(self):
        """Test with only one group."""
        y_pred = np.array([1, 0, 1, 0])
        sensitive = np.array(['A', 'A', 'A', 'A'])

        with pytest.raises(ValueError, match="at least 2 groups"):
            demographic_parity_difference(y_pred, sensitive)

    def test_all_zeros(self):
        """Test with all zero predictions."""
        y_pred = np.array([0, 0, 0, 0])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        assert dp == 0.0, "All zeros should give 0 difference"

    def test_all_ones(self):
        """Test with all one predictions."""
        y_pred = np.array([1, 1, 1, 1])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        dp = demographic_parity_difference(y_pred, sensitive)
        assert dp == 0.0, "All ones should give 0 difference"


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
