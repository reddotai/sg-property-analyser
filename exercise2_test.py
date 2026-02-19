#!/usr/bin/env python3
"""Exercise 2: BSD Manual Calculation Verification"""

print("="*60)
print("EXERCISE 2: BSD MANUAL CALCULATION")
print("="*60)

price = 1200000

print(f"\nCalculating BSD for ${price:,.0f} property:\n")

# Step 1: First $180,000
step1 = 180000 * 0.01
print(f"Step 1: First $180,000")
print(f"        $180,000 × 1% = ${step1:,.0f}")

# Step 2: Next $460,000 ($180K to $640K)
step2 = 460000 * 0.02
print(f"\nStep 2: Next $460,000 ($180K to $640K)")
print(f"        $460,000 × 2% = ${step2:,.0f}")

# Step 3: Next $360,000 ($640K to $1M)
step3 = 360000 * 0.03
print(f"\nStep 3: Next $360,000 ($640K to $1M)")
print(f"        $360,000 × 3% = ${step3:,.0f}")

# Step 4: Remaining $200,000 ($1M to $1.2M)
remaining = price - 1000000
step4 = remaining * 0.04
print(f"\nStep 4: Remaining ${remaining:,.0f} ($1M to $1.2M)")
print(f"        ${remaining:,.0f} × 4% = ${step4:,.0f}")

# Total
total_bsd = step1 + step2 + step3 + step4
print(f"\n{'='*40}")
print(f"Total BSD: ${total_bsd:,.0f}")
print(f"{'='*40}")

# Common misconception
print("\n" + "-"*60)
print("COMMON MISCONCEPTION")
print("-"*60)
wrong_calc = price * 0.04
print(f"WRONG: BSD is 4% of $1.2M = ${wrong_calc:,.0f}")
print(f"RIGHT: BSD is tiered. Actual BSD = ${total_bsd:,.0f}")
print(f"Savings from understanding tiers: ${wrong_calc - total_bsd:,.0f}")

# Verify with code
print("\n" + "-"*60)
print("VERIFICATION WITH CODE")
print("-"*60)

import sys
sys.path.insert(0, '/root/.openclaw/workspace/sg-property-analyser')
from calculations import calculate_bsd

code_bsd, breakdown = calculate_bsd(price)
print(f"Code calculation: ${code_bsd:,.0f}")
print(f"Match: {'✅ YES' if code_bsd == total_bsd else '❌ NO'}")

print("\nBreakdown from code:")
for line in breakdown:
    print(f"  {line}")

# Challenge: Build a BSD calculator
print("\n" + "="*60)
print("CHALLENGE: BSD CALCULATOR")
print("="*60)

def calculate_bsd_challenge(price):
    """Calculate BSD for any price."""
    total = 0
    tiers = [
        (0, 180000, 0.01),
        (180000, 640000, 0.02),
        (640000, 1000000, 0.03),
        (1000000, 1500000, 0.04),
        (1500000, 3000000, 0.05),
        (3000000, float('inf'), 0.06),
    ]
    
    for min_price, max_price, rate in tiers:
        if price > min_price:
            taxable = min(price, max_price) - min_price
            total += taxable * rate
    return total

# Test cases
print("\nTest cases:")
test_cases = [
    (500000, 8200),
    (1000000, 21800),
    (1500000, 41800),
    (1200000, 29800),
]

all_passed = True
for price, expected in test_cases:
    result = calculate_bsd_challenge(price)
    passed = abs(result - expected) < 0.01
    status = "✅" if passed else "❌"
    print(f"  {status} ${price:,.0f}: ${result:,.0f} (expected ${expected:,.0f})")
    if not passed:
        all_passed = False

print(f"\nAll tests passed: {'✅ YES' if all_passed else '❌ NO'}")

# Question about min(price, max_price)
print("\n" + "="*60)
print("CODE DEEP DIVE QUESTION")
print("="*60)
print("""
Question: Why do we use min(price, max_price)?

Answer: Because BSD is progressive. If the property is $900K,
we don't want to tax the full $360K in the $640K-$1M tier.

Example: Property = $900,000
- Tier $640K-$1M has max_price = $1,000,000
- min($900,000, $1,000,000) = $900,000
- Taxable = $900,000 - $640,000 = $260,000 (not $360,000!)

This ensures we only tax the portion that falls within each tier.
""")
