#!/usr/bin/env python
"""
Quick Demo Script

A simple command-line demo of the Fairness Framework.

Usage:
    python scripts/demo_quick.py
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fairness_detector import FairnessDetector
from src.metrics import compute_all_metrics


def create_demo_data():
    """Create simple demo dataset with intentional bias."""
    print("Creating demo dataset with intentional bias...")

    np.random.seed(42)
    n_samples = 500

    # Features
    feature_1 = np.random.randn(n_samples)
    feature_2 = np.random.randn(n_samples)

    # Sensitive attribute
    sensitive_attr = np.random.choice(['Group_A', 'Group_B'], size=n_samples)

    # Target with bias: Group A has 70% positive rate, Group B has 40%
    target = []
    for i in range(n_samples):
        prob = 0.7 if sensitive_attr[i] == 'Group_A' else 0.4
        prob += 0.1 * feature_1[i] + 0.05 * feature_2[i]
        prob = np.clip(prob, 0, 1)
        target.append(1 if np.random.rand() < prob else 0)

    df = pd.DataFrame({
        'feature_1': feature_1,
        'feature_2': feature_2,
        'sensitive_attr': sensitive_attr,
        'target': target
    })

    print(f"✓ Created {len(df)} samples")
    print(f"\nGroup distribution:")
    print(df.groupby('sensitive_attr')['target'].agg(['count', 'mean']))

    return df


def run_demo():
    """Run the demo."""
    print("=" * 60)
    print("FAIRNESS FRAMEWORK - QUICK DEMO")
    print("=" * 60)
    print()

    # Create data
    df = create_demo_data()
    print()

    # Initialize detector
    print("Initializing FairnessDetector...")
    detector = FairnessDetector(threshold=0.1, verbose=False)
    detector.set_sensitive_attributes(['sensitive_attr'])
    detector.set_target('target')
    print("✓ Detector initialized")
    print()

    # Detect bias
    print("Running bias detection...")
    results = detector.detect_bias(df)
    print()

    # Print results
    print(results.summary())
    print()

    # Compute all metrics
    print("Computing all fairness metrics...")
    all_metrics = compute_all_metrics(
        y_true=df['target'],
        y_pred=df['target'],
        sensitive_attr=df['sensitive_attr']
    )

    print("\nDetailed Metrics:")
    print("-" * 60)
    for metric_name, value in all_metrics.items():
        status = "✓ FAIR" if abs(value) <= 0.1 else "✗ BIASED"
        print(f"  {metric_name:25s}: {value:7.4f}  [{status}]")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("  • Try the Jupyter notebook: experiments/notebooks/01_quick_demo.ipynb")
    print("  • Read the docs: docs/quickstart.md")
    print("  • Load real data from: data/case_studies/")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
