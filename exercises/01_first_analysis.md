# Exercise 1: Your First Property Analysis

## Goal
Run the Property Deal Analyzer on a real listing and understand the output.

---

## Step 1: Find a Listing

Go to one of these sites:
- [PropertyGuru](https://www.propertyguru.com.sg)
- [99.co](https://www.99.co)
- [SRX](https://www.srx.com.sg)

Pick any condo or HDB listing. Note down:

| Field | Value |
|-------|-------|
| Price | $________ |
| Size (sqft) | ________ |
| Bedrooms | ________ |
| Bathrooms | ________ |
| Property Type | HDB / Condo / Landed |
| District | ________ |
| Tenure | Freehold / 99-year / 999-year |
| Years Remaining | ________ |

---

## Step 2: Run the Analyzer

```bash
cd sg-property-analyser
source venv/bin/activate
python3 analyze_property.py --manual
```

Enter the details from your listing.

---

## Step 3: Answer These Questions

### Costs
1. What's the **total upfront** cost? (Down payment + BSD + fees)
2. How much is **BSD**? Is it more or less than you expected?
3. What's the **monthly mortgage** payment?

### Investment
4. What's the **rental yield**? (Is it above or below 3%?)
5. Is the **cashflow positive or negative**?
6. If negative, how much would you need to cover each month?

### Market
7. Is the PSF **above or below** market average?
8. What's the **deal rating**? (Good deal / Fair / Overpriced?)

---

## Step 4: Reflection

**Would you buy this property? Why or why not?**

Consider:
- Can you afford the upfront costs?
- Can you handle the monthly payments?
- Is the rental yield acceptable for investment?
- Is the location worth the price?

---

## Bonus: Compare Two Properties

Run the analyzer on a second property. Compare:

| | Property 1 | Property 2 |
|---|---|---|
| Price | | |
| PSF | | |
| Monthly Cost | | |
| Rental Yield | | |
| Cashflow | | |
| Deal Rating | | |

**Which is the better deal? Why?**

---

## What You Learned

- How to use the Property Deal Analyzer
- How to read property listings critically
- The difference between asking price and true cost
- Why rental yield matters for investors

---

## Next Exercise

[→ Exercise 2: Understand BSD](02_understand_bsd.md)
