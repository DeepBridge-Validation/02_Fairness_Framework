"""
Unit tests for utility functions.

Run tests:
    pytest tests/test_utils.py -v
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import json

from src.utils import (
    validate_binary_labels,
    validate_sensitive_attribute,
    check_data_compatibility,
    load_dataset,
    save_results,
    group_statistics,
    confusion_matrix_by_group,
    format_metric,
    generate_summary_report,
    ensure_dir,
)


class TestValidation:
    """Tests for validation functions."""

    def test_validate_binary_labels_valid(self):
        """Test validation with valid binary labels."""
        y = np.array([0, 1, 0, 1, 1, 0])
        validate_binary_labels(y)  # Should not raise

    def test_validate_binary_labels_invalid(self):
        """Test validation with invalid labels."""
        y = np.array([0, 1, 2, 1])  # Contains 2
        with pytest.raises(ValueError, match="binary"):
            validate_binary_labels(y)

    def test_validate_binary_labels_all_zeros(self):
        """Test validation with all zeros."""
        y = np.array([0, 0, 0])
        validate_binary_labels(y)  # Should not raise

    def test_validate_binary_labels_all_ones(self):
        """Test validation with all ones."""
        y = np.array([1, 1, 1])
        validate_binary_labels(y)  # Should not raise

    def test_validate_sensitive_binary(self):
        """Test validation of binary sensitive attribute."""
        sensitive = np.array(['A', 'B', 'A', 'B'])
        validate_sensitive_attribute(sensitive)  # Should not raise

    def test_validate_sensitive_multiclass(self):
        """Test validation of multiclass sensitive attribute."""
        sensitive = np.array(['A', 'B', 'C', 'A'])

        # Should raise if multiclass not allowed
        with pytest.raises(ValueError, match="Binary sensitive attribute required"):
            validate_sensitive_attribute(sensitive, allow_multiclass=False)

        # Should not raise if multiclass allowed
        validate_sensitive_attribute(sensitive, allow_multiclass=True)

    def test_validate_sensitive_single_group(self):
        """Test validation with only one group."""
        sensitive = np.array(['A', 'A', 'A'])
        with pytest.raises(ValueError, match="at least 2 groups"):
            validate_sensitive_attribute(sensitive)


class TestDataCompatibility:
    """Tests for data compatibility checking."""

    def test_compatible_data(self):
        """Test with compatible arrays."""
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 1])
        sensitive = np.array(['A', 'B', 'A', 'B'])

        check_data_compatibility(y_true, y_pred, sensitive)  # Should not raise

    def test_incompatible_lengths(self):
        """Test with incompatible array lengths."""
        y_true = np.array([0, 1, 0])
        y_pred = np.array([0, 1, 1, 1])  # Different length
        sensitive = np.array(['A', 'B', 'A'])

        with pytest.raises(ValueError, match="don't match"):
            check_data_compatibility(y_true, y_pred, sensitive)


class TestLoadDataset:
    """Tests for dataset loading."""

    def test_load_csv(self):
        """Test loading CSV file."""
        # Create temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1,col2\n1,2\n3,4\n")
            temp_path = f.name

        try:
            df = load_dataset(temp_path)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert 'col1' in df.columns
        finally:
            Path(temp_path).unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file."""
        with pytest.raises(FileNotFoundError):
            load_dataset('/nonexistent/file.csv')

    def test_load_unsupported_format(self):
        """Test loading unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                load_dataset(temp_path)
        finally:
            Path(temp_path).unlink()


class TestSaveResults:
    """Tests for saving results."""

    def test_save_results(self):
        """Test saving results to JSON."""
        results = {
            'metric1': 0.5,
            'metric2': 0.8,
            'status': 'completed'
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / 'results.json'
            save_results(results, filepath)

            # Verify file was created and content is correct
            assert filepath.exists()
            with open(filepath) as f:
                loaded = json.load(f)
            assert loaded == results


class TestGroupStatistics:
    """Tests for group statistics computation."""

    def test_group_statistics(self):
        """Test computing statistics by group."""
        y = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'A', 'B', 'B', 'A', 'B'])

        stats = group_statistics(y, sensitive)

        assert isinstance(stats, pd.DataFrame)
        assert len(stats) == 2  # Two groups
        assert 'group' in stats.columns
        assert 'mean' in stats.columns
        assert 'count' in stats.columns

    def test_group_statistics_values(self):
        """Test that statistics values are correct."""
        y = np.array([1, 1, 0, 0])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        stats = group_statistics(y, sensitive)

        # Group A: mean = 1.0, count = 2
        # Group B: mean = 0.0, count = 2
        group_a = stats[stats['group'] == 'A'].iloc[0]
        group_b = stats[stats['group'] == 'B'].iloc[0]

        assert group_a['mean'] == 1.0
        assert group_a['count'] == 2
        assert group_b['mean'] == 0.0
        assert group_b['count'] == 2


class TestConfusionMatrixByGroup:
    """Tests for confusion matrix computation by group."""

    def test_confusion_matrix_basic(self):
        """Test basic confusion matrix computation."""
        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 1])
        sensitive = np.array(['A', 'A', 'B', 'B'])

        cm_dict = confusion_matrix_by_group(y_true, y_pred, sensitive)

        assert 'A' in cm_dict
        assert 'B' in cm_dict
        assert cm_dict['A'].shape == (2, 2)
        assert cm_dict['B'].shape == (2, 2)


class TestFormatMetric:
    """Tests for metric formatting."""

    def test_format_metric_with_name(self):
        """Test formatting with metric name."""
        formatted = format_metric(0.15432, "Demographic Parity")
        assert "Demographic Parity" in formatted
        assert "0.154" in formatted

    def test_format_metric_without_name(self):
        """Test formatting without metric name."""
        formatted = format_metric(0.15432)
        assert "0.154" in formatted


class TestGenerateSummaryReport:
    """Tests for summary report generation."""

    def test_generate_report(self):
        """Test generating summary report."""
        metrics = {
            'demographic_parity': 0.05,
            'equalized_odds': 0.15,
            'equal_opportunity': 0.08
        }

        report = generate_summary_report(metrics)

        assert 'FAIRNESS METRICS SUMMARY' in report
        assert 'demographic_parity' in report
        assert '0.05' in report
        assert 'PASS' in report or 'FAIL' in report


class TestEnsureDir:
    """Tests for directory creation."""

    def test_ensure_dir_creates(self):
        """Test that directory is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / 'new_directory'
            result = ensure_dir(new_dir)

            assert result.exists()
            assert result.is_dir()

    def test_ensure_dir_exists(self):
        """Test with existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            result = ensure_dir(tmpdir_path)

            assert result.exists()
            assert result.is_dir()


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_arrays(self):
        """Test with empty arrays."""
        y = np.array([])
        sensitive = np.array([])

        # Should handle gracefully or raise appropriate error
        with pytest.raises(Exception):
            group_statistics(y, sensitive)


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
