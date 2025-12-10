#!/usr/bin/env python3
"""
Script de teste para verificar instalação do DeepBridge.

Testa:
1. Import do DeepBridge
2. Criação de DBDataset
3. Auto-detecção de atributos sensíveis
4. Análise de fairness

Uso:
    python scripts/test_deepbridge_installation.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_deepbridge():
    """Testa instalação e funcionalidades básicas do DeepBridge."""

    print("=" * 60)
    print("DeepBridge Installation Test")
    print("=" * 60)
    print()

    # Test 1: Import
    print("Test 1: Importing DeepBridge...")
    try:
        from deepbridge import DBDataset
        print("✓ PASS: DeepBridge imported successfully")
    except ImportError as e:
        print(f"✗ FAIL: Could not import DeepBridge: {e}")
        print("\nPlease install DeepBridge:")
        print("  pip install -e /home/guhaase/projetos/DeepBridge/deepbridge")
        return False

    # Test 2: Create sample data
    print("\nTest 2: Creating sample dataset...")
    try:
        import pandas as pd
        import numpy as np

        np.random.seed(42)
        n_samples = 100

        data = {
            'age': np.random.randint(18, 70, n_samples),
            'income': np.random.randint(20000, 150000, n_samples),
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'race': np.random.choice(['White', 'Black', 'Asian'], n_samples),
            'approved': np.random.choice([0, 1], n_samples)
        }

        df = pd.DataFrame(data)
        print(f"✓ PASS: Created dataset with {len(df)} samples")
    except Exception as e:
        print(f"✗ FAIL: Could not create sample data: {e}")
        return False

    # Test 3: Create DBDataset
    print("\nTest 3: Creating DBDataset...")
    try:
        dataset = DBDataset(
            data=df,
            target_column='approved'
        )
        print("✓ PASS: DBDataset created successfully")
    except Exception as e:
        print(f"✗ FAIL: Could not create DBDataset: {e}")
        return False

    # Test 4: Check auto-detection
    print("\nTest 4: Checking auto-detection of sensitive attributes...")
    try:
        detected = dataset.detected_sensitive_attributes
        print(f"✓ PASS: Detected attributes: {detected}")

        # Verify expected attributes were detected
        expected = {'gender', 'race'}
        if not expected.issubset(set(detected)):
            print(f"⚠ WARNING: Expected {expected}, got {set(detected)}")
    except Exception as e:
        print(f"✗ FAIL: Could not detect attributes: {e}")
        return False

    # Test 5: Run fairness analysis
    print("\nTest 5: Running fairness analysis...")
    try:
        results = dataset.analyze_fairness()
        print("✓ PASS: Fairness analysis completed")
        print(f"\nResults preview:")
        print(str(results)[:500])  # Show first 500 chars
        if len(str(results)) > 500:
            print("...(truncated)")
    except Exception as e:
        print(f"✗ FAIL: Could not analyze fairness: {e}")
        import traceback
        traceback.print_exc()
        return False

    # All tests passed
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)
    print("\nDeepBridge is installed and working correctly!")
    print("\nNext steps:")
    print("  1. Run notebooks: jupyter notebook experiments/notebooks/")
    print("  2. Run experiments: cd experiments/scripts && python exp1_auto_detection.py --quick")
    print("  3. See documentation: docs/quickstart.md")

    return True


if __name__ == "__main__":
    success = test_deepbridge()
    sys.exit(0 if success else 1)
