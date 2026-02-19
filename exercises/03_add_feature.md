# Exercise 3: Add TDSR Calculation

## Goal
Add a feature that checks if the buyer can actually afford the property.

---

## What is TDSR?

**Total Debt Servicing Ratio** — The percentage of your income that goes to debt.

In Singapore, banks won't lend if your TDSR exceeds **55%**.

**Formula:**
```
TDSR = (Monthly Debt Payments / Monthly Income) × 100
```

---

## The Problem

Our analyzer calculates monthly costs, but doesn't check if the buyer can **qualify** for the loan.

**Example:**
- Monthly income: $8,000
- Monthly mortgage: $5,000
- Other debts: $1,000 (car loan, credit cards)
- TDSR = ($5,000 + $1,000) / $8,000 = 75%

**Result:** Bank won't approve the loan! ❌

---

## Your Task

Add TDSR checking to the analyzer.

---

## Step-by-Step Guide

### Step 1: Add the calculation function (Line ~15 in calculations.py)

Open `calculations.py` and add this function after `calculate_rental_yield`:

```python
def calculate_tdsr(monthly_mortgage: float, other_debts: float, monthly_income: float) -> float:
    """
    Calculate Total Debt Servicing Ratio.
    
    Singapore limit: 55%
    
    Formula: (Total Monthly Debt / Monthly Income) × 100
    """
    if monthly_income <= 0:
        return float('inf')
    total_debt = monthly_mortgage + other_debts
    return (total_debt / monthly_income) * 100


def can_qualify_for_loan(tdsr: float, max_tdsr: float = 55.0) -> bool:
    """Check if buyer can qualify for loan based on TDSR."""
    return tdsr <= max_tdsr
```

---

### Step 2: Add user inputs (Line ~140 in analyze_property.py)

Find the section where the buyer type is selected (around line 140). After the buyer type selection, add:

```python
    # NEW: Get income and debt information for TDSR
    print("\n" + "="*60)
    print("INCOME & DEBTS (for TDSR calculation)")
    print("="*60)
    
    monthly_income = get_input(
        "Monthly income",
        float,
        validator=validate_price,  # Reuse price validator (checks positive)
        help_text="Your gross monthly income (e.g., 8000)"
    )
    
    other_debts = get_input(
        "Other monthly debt payments",
        float,
        default=0,
        help_text="Car loan, credit cards, etc. (e.g., 1000)"
    )
```

---

### Step 3: Calculate and display TDSR (Line ~220 in analyze_property.py)

Find the `print_analysis` function call. Before that, calculate TDSR:

```python
    # Calculate TDSR
    tdsr = calculate_tdsr(
        analysis['monthly_mortgage'],
        other_debts,
        monthly_income
    )
    can_qualify = can_qualify_for_loan(tdsr)
```

---

### Step 4: Display the result

In the `print_analysis` function (around line 260), add this section:

```python
    # Add this after the "INVESTMENT ANALYSIS" section
    print("\n" + "-"*60)
    print("LOAN QUALIFICATION (TDSR)")
    print("-"*60)
    print(f"Monthly income: {format_currency(monthly_income)}")
    print(f"Monthly debts: {format_currency(analysis['monthly_mortgage'] + other_debts)}")
    print(f"TDSR: {tdsr:.1f}%")
    
    if can_qualify:
        print("✅ Can qualify for loan (TDSR ≤ 55%)")
    else:
        print("❌ Cannot qualify — TDSR exceeds 55% limit")
        print(f"   Maximum monthly payment: {format_currency(monthly_income * 0.55 - other_debts)}")
```

---

## Hints

### Finding the right lines

Use these commands to find the exact locations:

```bash
# Find where buyer type is selected
grep -n "Buyer type" analyze_property.py

# Find the print_analysis function
grep -n "def print_analysis" analyze_property.py
```

### Testing your changes

Run the analyzer and test with these scenarios:

| Monthly Income | Mortgage | Other Debts | Expected TDSR | Can Qualify? |
|----------------|----------|-------------|---------------|--------------|
| $10,000 | $4,000 | $1,000 | 50% | ✅ Yes |
| $8,000 | $5,000 | $1,000 | 75% | ❌ No |
| $15,000 | $6,000 | $2,000 | 53.3% | ✅ Yes |

---

## Troubleshooting

**Error: "calculate_tdsr is not defined"**
→ Make sure you added the import in `analyze_property.py`:
```python
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield, calculate_tdsr, can_qualify_for_loan  # Add these
)
```

**Error: "other_debts is not defined"**
→ Make sure you added the `other_debts` variable in the main function.

---

## What You Learned

- What TDSR is and why banks care
- How to add features to an existing codebase
- Input validation and error handling
- Working with multiple files (calculations.py + analyze_property.py)

---

## Show Off Your Work

Commit your changes:
```bash
git add calculations.py analyze_property.py
git commit -m "Add TDSR calculation feature"
git push
```

Now you have a portfolio piece that shows you can:
- Understand financial regulations
- Write clean Python code
- Add features to existing projects

---

## Next Exercise

[→ Exercise 4: Connect Real URA Data](04_real_data.md)
