# Exercise 2: Understand BSD (Buyer's Stamp Duty)

## Goal
Understand how BSD is calculated and why it's progressive.

---

## What is BSD?

**Buyer's Stamp Duty** is a tax everyone pays when buying property in Singapore.

It's **progressive** — like income tax, higher portions of the price are taxed at higher rates.

---

## BSD Tiers (2024)

| Price Range | Rate | Example for $1M property |
|-------------|------|--------------------------|
| First $180,000 | 1% | $1,800 |
| Next $460,000 ($180K-$640K) | 2% | $9,200 |
| Next $360,000 ($640K-$1M) | 3% | $10,800 |
| Next $500,000 ($1M-$1.5M) | 4% | $0 (property is only $1M) |
| Next $1.5M ($1.5M-$3M) | 5% | $0 |
| Above $3M | 6% | $0 |

**Total BSD for $1M property: $21,800**

---

## Manual Calculation Exercise

Calculate BSD for a **$1,200,000** property:

### Step 1: First $180,000
$180,000 × 1% = $________

### Step 2: Next $460,000 ($180K to $640K)
$460,000 × 2% = $________

### Step 3: Next $360,000 ($640K to $1M)
$360,000 × 3% = $________

### Step 4: Remaining $200,000 ($1M to $1.2M)
$200,000 × 4% = $________

### Total BSD
Add them up: $________

---

## Verify with the Tool

Run the analyzer:
```bash
python3 analyze_property.py --manual
```

Enter:
- Price: 1200000
- Any size, bedrooms, etc.

Check the BSD output. Does it match your manual calculation?

---

## Common Misconception

**Wrong:** "BSD is 4% of $1.2M = $48,000"

**Right:** BSD is tiered. Only the amount **above** $1M is taxed at 4%.

For $1.2M:
- First $180K: 1%
- Next $460K: 2%
- Next $360K: 3%
- Last $200K: 4%

**Actual BSD: $________** (calculate it!)

---

## Code Deep Dive

Open `calculations.py` (or `analyze_property.py`) and find the BSD calculation:

```python
def calculate_bsd(price):
    total = 0
    tiers = [
        (0, 180000, 0.01),
        (180000, 640000, 0.02),
        (640000, 1000000, 0.03),
        (1000000, 1500000, 0.04),
        # ... more tiers
    ]
    for min_price, max_price, rate in tiers:
        if price > min_price:
            taxable = min(price, max_price) - min_price
            total += taxable * rate
    return total
```

**Question:** Why do we use `min(price, max_price)`?

<details>
<summary>Answer</summary>
If the property is $900K, we don't want to tax the full $360K in the $640K-$1M tier. We only tax $900K - $640K = $260K.
</details>

---

## Challenge: Build a BSD Calculator

Write a simple Python script that calculates BSD for any price:

```python
def calculate_bsd(price):
    # Your code here
    pass

# Test
print(calculate_bsd(500000))   # Should be $8,200
print(calculate_bsd(1000000))  # Should be $21,800
print(calculate_bsd(1500000))  # Should be $41,800
```

---

## Stuck?

<details>
<summary><strong>My manual calculation doesn't match the tool</strong></summary>

Double-check your tiers:
- First $180K: 1% = $1,800
- Next $460K ($180K to $640K): 2% = $9,200
- Next $360K ($640K to $1M): 3% = $10,800
- Remaining $200K ($1M to $1.2M): 4% = $8,000

**Total: $29,800**

Common mistake: Using the full tier amount instead of just the portion that applies.
</details>

<details>
<summary><strong>I don't understand the code with min()</strong></summary>

`min(price, max_price)` handles properties that don't fill an entire tier.

Example: Property costs $900K
- Tier is $640K to $1M ($360K range)
- But property is only at $900K
- So we only tax $900K - $640K = $260K of that tier

`min(900000, 1000000) - 640000` = `900000 - 640000` = $260K
</details>

<details>
<summary><strong>My BSD calculator gives wrong answers</strong></summary>

Test with these known values:
- $500,000 → $8,200
- $1,000,000 → $21,800
- $1,500,000 → $41,800

If those work but others don't, check your tier boundaries.
</details>

<details>
<summary><strong>I want to see a working BSD calculator</strong></summary>

Only peek if you've tried for 20+ minutes.

[View solution →](../solutions/02_bsd_calculator_solution.py)
</details>

---

## What You Learned

- BSD is progressive, not flat
- How to calculate BSD manually
- Why the code uses `min(price, max_price)`
- How much BSD actually costs (it's less than you might think!)

---

## Next Exercise

[→ Exercise 3: Add a Feature](03_add_feature.md)
