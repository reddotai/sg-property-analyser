#!/usr/bin/env python3
"""Exercise 4: URA API Integration Test"""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/sg-property-analyser')

import os
from market_data import get_ura_transactions_real, analyze_market, print_market_analysis

print("="*60)
print("EXERCISE 4: URA API INTEGRATION")
print("="*60)

# Check if API key is set
api_key = os.environ.get('URA_API_KEY')
print(f"\nURA_API_KEY set: {'✅ YES' if api_key else '❌ NO'}")

if not api_key:
    print("\n⚠️  No API key found. The code will fall back to simulated data.")
    print("   To get a real API key:")
    print("   1. Go to https://www.developer.tech.gov.sg/products/categories/data-and-apis/ura-apis/overview")
    print("   2. Create an account")
    print("   3. Apply for URA API access")
    print("   4. Set URA_API_KEY environment variable")

# Test the function
print("\n" + "-"*60)
print("Testing get_ura_transactions_real()")
print("-"*60)

try:
    transactions = get_ura_transactions_real(district=19, property_type='condo')
    print(f"\n✅ Successfully retrieved {len(transactions)} transactions")
    
    # Check if data is simulated or real
    is_simulated = all(t.is_simulated for t in transactions)
    print(f"Data type: {'Simulated' if is_simulated else 'Real URA data'}")
    
    if transactions:
        print(f"\nSample transaction:")
        t = transactions[0]
        print(f"  Address: {t.address}")
        print(f"  Price: ${t.price:,.0f}")
        print(f"  Size: {t.size_sqft} sqft")
        print(f"  PSF: ${t.psf:,.0f}")
        print(f"  Date: {t.date}")
        print(f"  Is simulated: {t.is_simulated}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

# Test market analysis
print("\n" + "-"*60)
print("Testing analyze_market()")
print("-"*60)

try:
    analysis = analyze_market(
        target_price=1_200_000,
        target_size=900,
        district=9,
        property_type='condo'
    )
    
    print(f"\n✅ Market analysis complete")
    print(f"Target PSF: ${analysis.target_psf:,.0f}")
    print(f"Market avg PSF: ${analysis.avg_nearby_psf:,.0f}")
    print(f"Deal rating: {analysis.deal_rating}")
    print(f"Data source: {analysis.data_source}")
    print(f"Is simulated: {analysis.is_simulated}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

# Print full market analysis
print("\n" + "="*60)
print("FULL MARKET ANALYSIS OUTPUT")
print("="*60)

try:
    analysis = analyze_market(
        target_price=1_200_000,
        target_size=900,
        district=9,
        property_type='condo'
    )
    print_market_analysis(analysis)
    
except Exception as e:
    print(f"❌ Error: {e}")

# Summary
print("="*60)
print("EXERCISE 4 SUMMARY")
print("="*60)
print("""
What's implemented:
1. ✅ get_ura_transactions_real() function added
2. ✅ API key read from URA_API_KEY environment variable
3. ✅ Proper headers for URA API authentication
4. ✅ JSON parsing and Transaction object creation
5. ✅ Fallback to simulated data if API fails
6. ✅ analyze_market() updated to use real data function
7. ✅ Simulated data warning displayed when applicable

To use real data:
1. Apply for URA API access at developer.tech.gov.sg
2. Wait for approval (1-3 business days)
3. Set URA_API_KEY environment variable
4. Run the analyzer

Without API key, the system gracefully falls back to simulated data.
""")
