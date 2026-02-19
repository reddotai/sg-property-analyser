"""
Test suite for Property Deal Analyzer.

Run with: python3 -m pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations import calculate_bsd, calculate_absd, calculate_mortgage_monthly


def test_calculate_bsd():
    """Test BSD calculation for various prices."""
    # $500K property
    bsd, _ = calculate_bsd(500000)
    expected = 180000 * 0.01 + (500000 - 180000) * 0.02
    assert bsd == expected, f"BSD for $500K should be ${expected}, got ${bsd}"
    
    # $1M property
    bsd, _ = calculate_bsd(1000000)
    expected = 180000 * 0.01 + 460000 * 0.02 + 360000 * 0.03
    assert bsd == expected, f"BSD for $1M should be ${expected}, got ${bsd}"
    
    # $1.5M property
    bsd, _ = calculate_bsd(1500000)
    expected = 180000 * 0.01 + 460000 * 0.02 + 360000 * 0.03 + 500000 * 0.04
    assert bsd == expected, f"BSD for $1.5M should be ${expected}, got ${bsd}"


def test_calculate_absd():
    """Test ABSD for different buyer types."""
    price = 1000000
    
    # Singaporean first property
    absd, _ = calculate_absd(price, 'singaporean_first')
    assert absd == 0, "First property should have 0% ABSD"
    
    # Singaporean second property
    absd, _ = calculate_absd(price, 'singaporean_second')
    assert absd == 200000, "Second property should have 20% ABSD"
    
    # Foreigner
    absd, _ = calculate_absd(price, 'foreigner')
    assert absd == 600000, "Foreigner should have 60% ABSD"


def test_calculate_mortgage_monthly():
    """Test mortgage calculation."""
    # $750K loan, 25 years, 3.5% interest
    monthly = calculate_mortgage_monthly(750000, 25, 0.035)
    
    # Expected: approximately $3,753 (can verify with mortgage calculator)
    assert 3700 < monthly < 3800, f"Monthly payment should be ~$3,753, got ${monthly}"
    
    # Zero interest edge case
    monthly = calculate_mortgage_monthly(600000, 25, 0)
    expected = 600000 / (25 * 12)
    assert monthly == expected, "Zero interest should be simple division"


if __name__ == '__main__':
    print("Running tests...")
    test_calculate_bsd()
    print("✅ BSD tests passed")
    
    test_calculate_absd()
    print("✅ ABSD tests passed")
    
    test_calculate_mortgage_monthly()
    print("✅ Mortgage tests passed")
    
    print("\nAll tests passed! 🎉")
