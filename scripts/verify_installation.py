#!/usr/bin/env python
"""
Verify Installation Script

This script verifies that the Fairness Framework is correctly installed
and all dependencies are available.

Usage:
    python scripts/verify_installation.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_python_version():
    """Check Python version."""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro}")
        print("  ERROR: Python 3.8+ required")
        return False


def check_dependencies():
    """Check required dependencies."""
    print("\nChecking dependencies...")

    required = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
    }

    all_good = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_good = False

    return all_good


def check_framework_modules():
    """Check framework modules."""
    print("\nChecking framework modules...")

    modules = {
        'src.fairness_detector': 'FairnessDetector',
        'src.metrics': 'Fairness Metrics',
        'src.visualization': 'Visualization',
        'src.utils': 'Utilities',
    }

    all_good = True
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name} - IMPORT ERROR")
            print(f"     {str(e)}")
            all_good = False

    return all_good


def check_data_directories():
    """Check data directories."""
    print("\nChecking data directories...")

    dirs = {
        'data': 'Data directory',
        'data/synthetic': 'Synthetic datasets',
        'data/case_studies': 'Case studies',
        'data/ground_truth': 'Ground truth',
    }

    root = Path(__file__).parent.parent
    for path, name in dirs.items():
        full_path = root / path
        if full_path.exists():
            print(f"  ✓ {name}")
        else:
            print(f"  ⚠ {name} - NOT FOUND (will be created when needed)")

    return True


def quick_functionality_test():
    """Run a quick functionality test."""
    print("\nRunning quick functionality test...")

    try:
        import numpy as np
        from src.fairness_detector import FairnessDetector
        from src.metrics import demographic_parity_difference

        # Create dummy data
        y_pred = np.array([1, 0, 1, 0, 1, 0])
        sensitive = np.array(['A', 'B', 'A', 'B', 'A', 'B'])

        # Test metric
        dp = demographic_parity_difference(y_pred, sensitive)
        print(f"  ✓ Metric computation works (DP = {dp:.3f})")

        # Test detector
        detector = FairnessDetector()
        print(f"  ✓ FairnessDetector instantiation works")

        return True

    except Exception as e:
        print(f"  ✗ Functionality test FAILED")
        print(f"     {str(e)}")
        return False


def main():
    """Main verification function."""
    print("=" * 60)
    print("Fairness Framework - Installation Verification")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Framework Modules", check_framework_modules),
        ("Data Directories", check_data_directories),
        ("Functionality", quick_functionality_test),
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8s} {name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 Installation verified successfully!")
        print("\nNext steps:")
        print("  1. Try the quick demo: jupyter notebook experiments/notebooks/01_quick_demo.ipynb")
        print("  2. Read the docs: docs/quickstart.md")
        print("  3. Run experiments: cd experiments/scripts && ./run_all.sh")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
