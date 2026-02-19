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

```bash
export URA_API_KEY="your_actual_api_key_here"
```

To make it permanent, add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export URA_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 4: Modify the Code

Open `market_data.py`. Find the `get_ura_transactions()` function.

Currently it returns simulated data. Replace with:

```python
import requests
import os

def get_ura_transactions(district, property_type, months=6):
    api_key = os.environ.get('URA_API_KEY')
    
    if not api_key:
        print("⚠️  No URA_API_KEY found. Using simulated data.")
        return get_simulated_transactions(district, property_type)
    
    # Call real URA API
    headers = {
        'AccessKey': api_key,
        'User-Agent': 'sg-property-analyser/1.0'
    }
    
    # URA API endpoint for private residential transactions
    url = f"https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_ResiTransaction&district={district}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"⚠️  API error: {response.status_code}. Using simulated data.")
        return get_simulated_transactions(district, property_type)
    
    data = response.json()
    
    # Parse the response and convert to Transaction objects
    transactions = []
    for item in data.get('Result', []):
        transactions.append(Transaction(
            address=item.get('streetName', 'Unknown'),
            property_type=property_type,
            size_sqft=float(item.get('floorArea', 0)),
            price=float(item.get('transactionPrice', 0)),
            date=item.get('transactionDate', ''),
            is_simulated=False
        ))
    
    return transactions
```

---

## Step 5: Test It

```bash
export URA_API_KEY="your_key"
python3 analyze_property.py --manual
```

You should see:
```
📊 MARKET ANALYSIS
Using real URA data ✅
```

Instead of:
```
⚠️  NOTE: Using simulated data for demonstration
```

---

## Understanding the API Response

URA API returns JSON like:
```json
{
  "Result": [
    {
      "streetName": "ANCHORVALE LANE",
      "floorArea": 904,
      "transactionPrice": 1468888,
      "transactionDate": "Jan 2024",
      "propertyType": "Condominium",
      "district": 19
    }
  ]
}
```

**Challenge:** The API might return different field names. Check the actual response and adjust your code.

---

## Error Handling

What if the API is down? Add fallback:

```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except (requests.RequestException, ValueError) as e:
    print(f"⚠️  Could not fetch real data: {e}")
    print("Using simulated data instead.")
    return get_simulated_transactions(district, property_type)
```

---

## Bonus: Cache the Data

Don't hit the API every time. Cache results:

```python
import json
from datetime import datetime, timedelta

def get_cached_transactions(district, property_type):
    cache_file = f"cache_{district}_{property_type}.json"
    
    # Check if cache exists and is fresh (< 24 hours)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            if datetime.now() - cache_time < timedelta(hours=24):
                return [Transaction(**t) for t in cache['transactions']]
    
    # Fetch fresh data
    transactions = get_ura_transactions(district, property_type)
    
    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'transactions': [t.__dict__ for t in transactions]
        }, f)
    
    return transactions
```

---

## What You Learned

- How to work with government APIs
- API authentication with headers
- JSON parsing and data transformation
- Error handling and fallbacks
- Caching strategies

---

## Show Off Your Work

This is a serious portfolio piece:

> "Integrated Singapore URA API for real-time property transaction data, with caching and fallback mechanisms."

That's resume-worthy.

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
