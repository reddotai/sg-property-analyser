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

### Step 1: Verify calculations.py has the functions

Open `calculations.py` and check that these functions exist:

```python
def calculate_tdsr(monthly_mortgage: float, other_debts: float, monthly_income: float) -> float:
def can_qualify_for_loan(tdsr: float, max_tdsr: float = 55.0) -> bool:
```

If they don't exist, add them:

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

### Step 2: Update imports in analyze_property.py

Find the imports at the top of `analyze_property.py`. Look for:

```python
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield
)
```

Add the new functions:

```python
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield, calculate_tdsr, can_qualify_for_loan
)
```

---

### Step 3: Add user inputs

Find the section in `analyze_property.py` where the buyer type is selected.

**Find it with:** `grep -n "BUYER TYPE" analyze_property.py`

After the buyer type selection (after the `choice = get_input(...)` line), add:

```python
    # NEW: Get income and debt information for TDSR
    print("\n" + "="*60)
    print("INCOME & DEBTS (for TDSR calculation)")
    print("="*60)
    
    monthly_income = get_input(
        "Monthly income",
        float,
        validator=validate_price,
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

### Step 4: Calculate TDSR

Find where `analyze_deal()` is called. 

**Find it with:** `grep -n "analyze_deal" analyze_property.py`

After the analysis is returned, add TDSR calculation:

```python
    # Run analysis
    analysis = analyze_deal(listing, buyer_type, is_hdb)
    
    # NEW: Calculate TDSR
    tdsr = calculate_tdsr(
        analysis['monthly_mortgage'],
        other_debts,
        monthly_income
    )
    can_qualify = can_qualify_for_loan(tdsr)
```

---

### Step 5: Display the result

Find the `print_analysis()` function.

**Find it with:** `grep -n "def print_analysis" analyze_property.py`

Inside `print_analysis`, find the "INVESTMENT ANALYSIS" section.

**Find it with:** `grep -n "INVESTMENT ANALYSIS" analyze_property.py`

After that section, add:

```python
    # NEW: TDSR section
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
        max_payment = monthly_income * 0.55 - other_debts
        print(f"   Maximum monthly payment: {format_currency(max_payment)}")
```

**Note:** You'll need to pass `monthly_income`, `other_debts`, `tdsr`, and `can_qualify` to `print_analysis()`. Update the function signature:

```python
def print_analysis(listing, analysis, monthly_income=0, other_debts=0, tdsr=0, can_qualify=True):
```

And update the call:

```python
print_analysis(listing, analysis, monthly_income, other_debts, tdsr, can_qualify)
```

---

## Testing Your Changes

Run the analyzer:
```bash
python3 analyze_property.py --manual
```

Test with these scenarios:

| Monthly Income | Mortgage | Other Debts | Expected TDSR | Can Qualify? |
|----------------|----------|-------------|---------------|--------------|
| $10,000 | $4,000 | $1,000 | 50% | ✅ Yes |
| $8,000 | $5,000 | $1,000 | 75% | ❌ No |
| $15,000 | $6,000 | $2,000 | 53.3% | ✅ Yes |

---

## Stuck?

<details>
<summary><strong>Error: "calculate_tdsr is not defined"</strong></summary>

You forgot to import the function. In `analyze_property.py`, find the line:
```python
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield
)
```

Add the new functions:
```python
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield, calculate_tdsr, can_qualify_for_loan
)
```
</details>

<details>
<summary><strong>Error: "other_debts is not defined"</strong></summary>

You need to add the input variables before using them. In the main function, after the buyer type selection, add:
```python
monthly_income = get_input(
    "Monthly income",
    float,
    validator=validate_price,
    help_text="Your gross monthly income (e.g., 8000)"
)

other_debts = get_input(
    "Other monthly debt payments",
    float,
    default=0,
    help_text="Car loan, credit cards, etc. (e.g., 1000)"
)
```
</details>

<details>
<summary><strong>Error: "print_analysis() takes 2 positional arguments but 6 were given"</strong></summary>

You need to update the function signature to accept the new parameters. Find:
```python
def print_analysis(listing, analysis):
```

Change to:
```python
def print_analysis(listing, analysis, monthly_income=0, other_debts=0, tdsr=0, can_qualify=True):
```

And update the call to pass these values.
</details>

<details>
<summary><strong>I don't know where to add the TDSR calculation</strong></summary>

Find where `analyze_deal()` is called. After that line, add:
```python
tdsr = calculate_tdsr(
    analysis['monthly_mortgage'],
    other_debts,
    monthly_income
)
can_qualify = can_qualify_for_loan(tdsr)
```

Use this command to find the line:
```bash
grep -n "analyze_deal" analyze_property.py
```
</details>

<details>
<summary><strong>I want to see the full solution</strong></summary>

Only open this if you've tried for at least 30 minutes. The struggle is where learning happens.

[View solution →](../solutions/03_add_feature_solution.md)
</details>

---

## What You Learned

- What TDSR is and why banks care
- How to add features to an existing codebase
- Working with multiple files
- Updating function signatures

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
