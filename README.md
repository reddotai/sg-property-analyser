# Property Deal Analyzer

Paste a PropertyGuru listing URL → Get full financial breakdown including hidden costs.

## What It Does

- Extracts listing details (price, size, tenure, etc.)
- Calculates true costs: ABSD, stamp duty, legal fees, agent commission
- Estimates rental yield (if investment)
- Shows monthly mortgage breakdown
- Flags potential issues (lease decay, maintenance, etc.)
- Compares against market data (simulated or real URA data)

## Quick Start

```bash
# Interactive mode (recommended)
python analyze_property.py --manual

# Or with a PropertyGuru URL
python analyze_property.py "https://www.propertyguru.com.sg/..."

# See term explanations
python analyze_property.py --glossary
```

## Output Example

```
📍 123 Bukit Timah Road
💰 Asking: $1,250,000
📏 1,200 sqft | $1,042 psf
⏱️  82 years lease remaining

--- BUYER COSTS ---
BSD (Buyer's Stamp Duty): $32,600
  • 1% on first $180,000: $1,800
  • 2% on next $460,000: $9,200
  • 3% on next $360,000: $10,800
  • 4% on next $500,000: $10,800
ABSD: $0 (No ABSD for this buyer type)
Legal fees: $3,000
Agent commission: $12,500
Down payment: $312,500 (75% - First property loan)
TOTAL UPFRONT: $360,600

--- MONTHLY ---
Mortgage: $4,690 (25 years @ 3.5% interest)
Maintenance: $350
Property tax: $42
TOTAL MONTHLY: $5,082

--- INVESTMENT ANALYSIS ---
Est. rental income: $4,200/month
Rental yield: 4.0% (Benchmark: 3.0-3.5%)
Cashflow: -$882/month (NEGATIVE ⚠️)

⚠️  You'll need $882/month from other income

--- NOTES ---
⚠️  Lease decay: Only 82 years remaining

--- MARKET ANALYSIS ---
⚠️  NOTE: Using simulated data for demonstration
   Connect to URA API for real transaction data

🔥 GOOD DEAL
Target PSF: $1,042 vs Market Average: $1,636 (-33.6%)
```

## Using Real URA Data (Optional)

By default, the tool uses **simulated market data** for demonstration. To use real URA transaction data:

1. **Get a URA API key** from [Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/data-and-apis/ura-apis/overview)

2. **Set your API key:**
   ```bash
   export URA_API_KEY="your_api_key_here"
   ```

3. **Run the analyzer** — it will automatically use real URA data when available

> **Note:** URA API access may require registration and approval. The tool works great with simulated data for learning purposes.

## What You Learn

- Web scraping with Playwright
- Financial modeling in Python
- Singapore property regulations (ABSD, BSD, LTV limits)
- Data extraction from unstructured HTML
- Input validation and security best practices

## Project Structure

```
property-deal-analyzer/
├── analyze_property.py    # Main analysis engine
├── market_data.py         # Market data and transactions
├── scraper.py            # PropertyGuru scraper
├── models.py             # Shared data models
├── config.py             # Configuration and constants
├── validators.py         # Input validation
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Requirements

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

## Configuration

You can customize behavior via environment variables:

```bash
# Interest rate (default: 3.5%)
export INTEREST_RATE=0.04

# Loan tenure in years (default: 25)
export LOAN_TENURE=30

# Legal fees estimate (default: $3,000)
export LEGAL_FEES=3500

# URA API key for real data
export URA_API_KEY="your_key_here"
```

## Safety & Disclaimer

⚠️ **This tool is for educational purposes.** Always verify calculations with:
- Your bank for actual mortgage rates and loan eligibility
- IRAS for official stamp duty calculations
- A qualified property agent or lawyer for legal advice

The market data shown (unless using URA API) is **simulated** and should not be used for actual investment decisions.

---

Built in 3 hours. No certificate required.
