# Singapore Property Deal Analyzer

> **Built in 3 hours. No certificate required.**
> 
> Learn how AI and code can replace expensive property agent calculations — and understand Singapore property regulations better than any course teaches.

---

## What You'll Learn

This isn't just a calculator. It's a **learning project** that teaches you:

### 💰 Financial Modeling
- How BSD (Buyer's Stamp Duty) actually works — tier by tier
- Why ABSD kills investment returns for 2nd properties
- How banks calculate mortgage payments (the formula!)
- What "rental yield" really means and why 3% matters

### 🏠 Singapore Property Market
- Why District 9-11 commands premium prices
- How lease decay affects resale value
- HDB vs Condo vs Landed — the real cost differences
- CPF grants most first-time buyers don't know about

### 💻 Practical Coding Skills
- Building a CLI tool from scratch
- Input validation and error handling
- Web scraping with Playwright
- Working with real (and simulated) data APIs

---

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/reddotai/sg-property-analyser.git
cd sg-property-analyser
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Run your first analysis
python3 analyze_property.py --manual
```

---

## Learning Path

### Level 1: Use the Tool (15 minutes)
Run the analyzer on a real listing. See how much that "dream condo" actually costs.

**Exercise:** Find a listing on PropertyGuru. Input the details. What's the real monthly cost?

### Level 2: Understand the Math (30 minutes)
Read `calculations.py`. See how BSD tiers work. Understand why your mortgage payment is what it is.

**Exercise:** Modify the interest rate in `config.py`. How does monthly payment change?

### Level 3: Build Your Own Feature (1 hour)
Add a new feature:
- Calculate TDSR (Total Debt Servicing Ratio)
- Add a "compare two properties" function
- Build a simple web interface

**Exercise:** Add a feature that flags properties with <60 years lease remaining.

### Level 4: Connect Real Data (2 hours)
Apply for URA API access. Replace simulated data with real transaction data.

---

## Why This Beats SkillsFuture

| SkillsFuture Course | This Project |
|---------------------|--------------|
| $500-1,000 | Free |
| 2-3 days classroom | 3 hours hands-on |
| Theory-heavy | Build something real |
| Generic certificate | GitHub portfolio piece |
| Forget in 3 months | Use every time you house-hunt |

---

## The "Aha" Moments

Most people don't understand:

1. **BSD is progressive** — You don't pay 4% on the whole amount, just the portion above $1M
2. **ABSD is brutal** — 20% on your 2nd property means $300K extra on a $1.5M condo
3. **Cashflow matters more than appreciation** — Negative $2K/month adds up to $24K/year
4. **Lease decay is real** — Properties under 60 years can't use full CPF

This tool makes all of this **visible and calculable**.

---

## Project Structure

```
sg-property-analyser/
├── analyze_property.py      # Main CLI — start here
├── calculations.py          # BSD, ABSD, mortgage math
├── config.py                # Constants and configuration
├── models.py                # Data structures
├── scraper.py               # PropertyGuru scraping
├── market_data.py           # URA API integration
├── validators.py            # Input validation
├── tests/                   # Test your understanding
│   ├── test_calculations.py
│   └── test_scraper.py
├── exercises/               # Hands-on challenges
│   ├── 01_first_analysis.md
│   ├── 02_understand_bsd.md
│   ├── 03_add_feature.md
│   └── 04_real_data.md
└── README.md               # This file
```

---

## Exercises

### Exercise 1: Your First Analysis
Find a property listing. Run the analyzer. Document:
- What's the biggest cost? (BSD? Down payment?)
- Is the rental yield above or below benchmark?
- Would you buy this? Why or why not?

[→ Start Exercise 1](exercises/01_first_analysis.md)

### Exercise 2: BSD Breakdown
Manually calculate BSD for a $1.2M property. Verify with the tool.

[→ Start Exercise 2](exercises/02_understand_bsd.md)

### Exercise 3: Add TDSR Calculation
TDSR = (Monthly Debt / Monthly Income) × 100

Add a feature that checks if buyer can afford the property.

[→ Start Exercise 3](exercises/03_add_feature.md)

### Exercise 4: Real URA Data
Apply for URA API. Replace simulated data.

[→ Start Exercise 4](exercises/04_real_data.md)

---

## Common Questions

**Q: Do I need to know Python?**
A: Basic Python helps, but you can learn as you go. The code is commented and simple.

**Q: Is this legal?**
A: Yes. Calculating stamp duties and mortgages is math, not legal advice. Always verify with a professional before buying.

**Q: Can I use this for commercial properties?**
A: Not yet. This is for residential. But you could extend it!

**Q: What's the catch?**
A: No catch. This is what learning should look like — free, practical, and immediately useful.

---

## Built With

- Python 3.12
- Playwright (for scraping)
- Zero AI — just code and math

---

## About This Project

This is part of the **"Better Than SkillsFuture"** series — practical projects that teach real skills through building useful tools.

**Other projects in the series:**
- [expense-parser](https://github.com/reddotai/expense-parser) — AI receipt processing
- [meeting-minutes-ai](https://github.com/reddotai/meeting-minutes-ai) — Automated meeting notes

---

**Built in 3 hours. No certificate required.**

If this helped you, star the repo and share it.
