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

### Step 1: Add Input

In `analyze_property.py`, add prompts for:
- Monthly income
- Other monthly debt payments

### Step 2: Calculate TDSR

```python
def calculate_tdsr(monthly_mortgage, other_debts, monthly_income):
    total_debt = monthly_mortgage + other_debts
    tdsr = (total_debt / monthly_income) * 100
    return tdsr
```

### Step 3: Check Qualification

```python
def can_qualify(tdsr):
    return tdsr <= 55  # 55% is the limit
```

### Step 4: Display Result

Add to the output:
```
TDSR: 48% ✅ (Can qualify for loan)
```

Or:
```
TDSR: 62% ❌ (Cannot qualify — exceeds 55% limit)
```

---

## Hints

### Where to add the code

Find the section in `analyze_property.py` where buyer type is selected. Add your new inputs there.

### Input validation

```python
monthly_income = float(input("Monthly income: "))
if monthly_income <= 0:
    print("Income must be positive")
```

### Display formatting

```python
tdsr = calculate_tdsr(monthly_mortgage, other_debts, monthly_income)
status = "✅ Can qualify" if can_qualify(tdsr) else "❌ Cannot qualify"
print(f"TDSR: {tdsr:.1f}% {status}")
```

---

## Test Cases

| Monthly Income | Mortgage | Other Debts | TDSR | Can Qualify? |
|----------------|----------|-------------|------|--------------|
| $10,000 | $4,000 | $1,000 | 50% | ✅ Yes |
| $8,000 | $5,000 | $1,000 | 75% | ❌ No |
| $15,000 | $6,000 | $2,000 | 53.3% | ✅ Yes |

---

## Bonus: Suggest Maximum Property Price

If TDSR is too high, suggest a lower price:

```python
def max_affordable_price(monthly_income, other_debts, interest_rate, years):
    max_monthly = (monthly_income * 0.55) - other_debts
    # Reverse mortgage formula to get max loan amount
    # ... your code here
    return max_property_price
```

---

## What You Learned

- What TDSR is and why banks care
- How to add features to an existing codebase
- Input validation and error handling
- Reverse calculations (from monthly payment to max price)

---

## Show Off Your Work

Commit your changes:
```bash
git add analyze_property.py
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
