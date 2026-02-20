# Exercise 4: Connect Real URA Data

## Goal
Replace simulated market data with real URA transaction data.

---

## Why Real Data Matters

Our current analyzer uses **simulated** market data:
- Good for learning
- Good for testing
- **Not accurate** for real decisions

Real URA data shows:
- Actual recent transactions
- Real PSF prices
- Genuine market trends

---

## Prerequisites

**⚠️ Important:** This exercise requires:
1. A URA API key (free, but takes 1-3 days to approve)
2. Basic understanding of APIs

If you don't have an API key yet, **read through this exercise** to understand what's involved, then come back after you get approved.

---

## Step 1: Apply for URA API Access

1. Go to [Singapore Government Developer Portal](https://www.developer.tech.gov.sg/products/categories/data-and-apis/ura-apis/overview)
2. Create an account
3. Apply for URA API access
4. Wait for approval (usually 1-3 business days)

**Note:** This is free for developers, but requires approval.

---

## Step 2: Get Your API Key

Once approved:
1. Log in to the developer portal
2. Go to your dashboard
3. Generate an API key for URA
4. Copy the key

---

## Step 3: Set Up Environment Variable

**What is an environment variable?**

Think of it as a secret note that programs can read. We store the API key here so we don't have to type it every time (and so we don't accidentally share it).

**Temporary (for this session only):**
```bash
export URA_API_KEY="your_actual_api_key_here"
```

**Permanent (recommended):**
```bash
# Add to your shell profile
echo 'export URA_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

**On Windows:**
```cmd
setx URA_API_KEY "your_key"
```

---

## Step 4: Modify the Code

### Step 4a: Add imports

Open `market_data.py` and add at the top:

```python
import os
import requests
```

---

### Step 4b: Add the real data function

Find the `get_simulated_transactions()` function.

**Find it with:** `grep -n "def get_simulated_transactions" market_data.py`

Add this new function after it:

```python
def get_ura_transactions_real(district: int, property_type: str) -> List[Transaction]:
    """
    Fetch real transaction data from URA API.
    
    Falls back to simulated data if API is unavailable.
    """
    api_key = os.environ.get('URA_API_KEY')
    
    if not api_key:
        print("⚠️  No URA_API_KEY found. Using simulated data.")
        return get_simulated_transactions(district, property_type)
    
    try:
        # Call URA API
        headers = {
            'AccessKey': api_key,
            'User-Agent': 'sg-property-analyser/1.0'
        }
        
        url = f"https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_ResiTransaction&district={district}"
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse response
        transactions = []
        for item in data.get('Result', []):
            # Only include matching property types
            if item.get('propertyType', '').lower() == property_type.lower():
                transactions.append(Transaction(
                    address=item.get('streetName', 'Unknown'),
                    property_type=property_type,
                    size_sqft=float(item.get('floorArea', 0)),
                    price=float(item.get('transactionPrice', 0)),
                    date=item.get('transactionDate', ''),
                    is_simulated=False
                ))
        
        if transactions:
            print(f"✅ Loaded {len(transactions)} real transactions from URA")
            return transactions
        else:
            print("⚠️  No transactions found. Using simulated data.")
            return get_simulated_transactions(district, property_type)
            
    except Exception as e:
        print(f"⚠️  Could not fetch real data: {e}")
        print("Using simulated data instead.")
        return get_simulated_transactions(district, property_type)
```

---

### Step 4c: Update analyze_market to use real data

Find the `analyze_market()` function.

**Find it with:** `grep -n "def analyze_market" market_data.py`

Find this line inside the function:

```python
transactions = get_simulated_transactions(district, property_type)
```

Change it to:

```python
transactions = get_ura_transactions_real(district, property_type)
```

---

## Step 5: Test It

```bash
export URA_API_KEY="your_key"
python3 analyze_property.py --manual
```

You should see:
```
✅ Loaded 15 real transactions from URA
```

Instead of:
```
⚠️  ⚠️  ⚠️  USING SIMULATED DATA - NOT REAL PRICES  ⚠️  ⚠️  ⚠️
```

---

## Stuck?

<details>
<summary><strong>"No URA_API_KEY found" error</strong></summary>

Make sure you exported the key in the **same terminal session**:
```bash
export URA_API_KEY="your_actual_key"
```

To check if it's set:
```bash
echo $URA_API_KEY
```

If empty, you need to export it again.
</details>

<details>
<summary><strong>"API error: 401" or "Unauthorized"</strong></summary>

Your API key might be:
- Wrong (copy-paste error)
- Expired (check the developer portal)
- Not yet activated (wait 1-3 days after applying)

Double-check in the [URA developer portal](https://www.developer.tech.gov.sg).
</details>

<details>
<summary><strong>"ModuleNotFoundError: No module named 'requests'"</strong></summary>

Install the requests library:
```bash
pip install requests
```

Or if using the virtual environment:
```bash
source venv/bin/activate
pip install requests
```
</details>

<details>
<summary><strong>The API returns different field names</strong></summary>

URA sometimes changes their API response format. Print the actual response to see what fields are available:

```python
response = requests.get(url, headers=headers)
data = response.json()
print(json.dumps(data, indent=2))  # See the actual structure
```

Then adjust your code to match the real field names.
</details>

<details>
<summary><strong>I want to see the complete working code</strong></strong></summary>

Only look if you've been stuck for 30+ minutes. Figuring this out is the learning.

[View solution →](../solutions/04_ura_integration_solution.py)
</details>

---

## What You Learned

- How to work with government APIs
- API authentication with headers
- JSON parsing and data transformation
- Error handling and fallbacks
- Caching strategies
- Environment variables for secrets

---

## Show Off Your Work

This is a serious portfolio piece:

> "Integrated Singapore URA API for real-time property transaction data, with caching and fallback mechanisms."

That's resume-worthy.

Commit your changes:
```bash
git add market_data.py
git commit -m "Add URA API integration with real transaction data"
git push
```

---

## Continue Learning

Ideas for further improvement:

1. **Add more data sources** — Combine URA with PropertyGuru scraping
2. **Historical trends** — Track price changes over 12 months
3. **Price alerts** — Notify when properties in an area drop below target PSF
4. **Web interface** — Build a simple website with Streamlit or Flask

---

**You've completed all exercises!** 🎉

You now understand:
- Singapore property regulations (BSD, ABSD, TDSR)
- Financial modeling in Python
- API integration
- Building useful tools

**Better than any SkillsFuture course.**
