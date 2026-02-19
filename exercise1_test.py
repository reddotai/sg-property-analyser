#!/usr/bin/env python3
"""Test script for Exercise 1"""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/sg-property-analyser')

from models import PropertyListing
from calculations import calculate_bsd, calculate_absd, calculate_mortgage_monthly, calculate_rental_yield
from analyze_property import analyze_deal, estimate_market_rent, format_currency

# Sample property: $1.2M condo in District 9
listing = PropertyListing(
    url="manual",
    price=1200000,
    size_sqft=900,
    bedrooms=3,
    bathrooms=2,
    tenure="99",
    lease_years_remaining=85,
    property_type="condo",
    district=9,
    address="Orchard Condo"
)

print("="*60)
print("EXERCISE 1: FIRST PROPERTY ANALYSIS")
print("="*60)
print(f"\nProperty: {listing.address}")
print(f"Price: {format_currency(listing.price)}")
print(f"Size: {listing.size_sqft} sqft")
print(f"District: {listing.district}")
print(f"Type: {listing.property_type}")

# Run analysis
analysis = analyze_deal(listing, 'singaporean_first', is_hdb=False)

print("\n" + "-"*60)
print("COSTS ANALYSIS")
print("-"*60)
print(f"1. Total upfront: {format_currency(analysis['total_upfront'])}")
print(f"   - Down payment: {format_currency(analysis['down_payment'])}")
print(f"   - BSD: {format_currency(analysis['bsd'])}")
print(f"   - ABSD: {format_currency(analysis['absd'])}")
print(f"   - Legal fees: {format_currency(analysis['legal_fees'])}")
print(f"   - Agent commission: {format_currency(analysis['agent_commission'])}")

print(f"\n2. BSD amount: {format_currency(analysis['bsd'])}")
print("   BSD breakdown:")
for line in analysis['bsd_breakdown']:
    print(f"   {line}")

print(f"\n3. Monthly mortgage: {format_currency(analysis['monthly_mortgage'])}")
print(f"   Total monthly: {format_currency(analysis['total_monthly'])}")

# Investment analysis
estimated_rent = estimate_market_rent(listing)
yield_pct = calculate_rental_yield(listing.price, estimated_rent)
cashflow = estimated_rent - analysis['total_monthly']

print("\n" + "-"*60)
print("INVESTMENT ANALYSIS")
print("-"*60)
print(f"4. Rental yield: {yield_pct:.1f}%")
print(f"   (Benchmark for condo: 3.0-3.5%)")
print(f"   Yield is {'ABOVE' if yield_pct >= 3.0 else 'BELOW'} benchmark")

print(f"\n5. Cashflow: {format_currency(cashflow)}/month")
print(f"   Status: {'POSITIVE ✅' if cashflow > 0 else 'NEGATIVE ⚠️'}")

print(f"\n6. If negative, need to cover: {format_currency(abs(cashflow))}/month")

# Market analysis
psf = listing.price / listing.size_sqft
print("\n" + "-"*60)
print("MARKET ANALYSIS")
print("-"*60)
print(f"7. PSF: ${psf:.0f}")
print(f"   District 9 average: ~$1,400-1,600 psf")
print(f"   This property is: {'Fair value' if 1400 <= psf <= 1600 else 'Above' if psf > 1600 else 'Below'} average")

print(f"\n8. Deal rating: {'Good deal' if yield_pct >= 3.5 else 'Fair' if yield_pct >= 3.0 else 'Overpriced'}")

print("\n" + "="*60)
print("REFLECTION")
print("="*60)
print("""
Would I buy this property?

Pros:
- Prime District 9 location
- 3-bedroom good for families
- BSD is reasonable at ~2.8% of price

Cons:
- Cashflow negative (need to cover monthly)
- Rental yield at 3.6% is borderline
- 85 years lease remaining (will decay)

Verdict: Probably NOT for pure investment, but might be okay 
for own stay if location is important.
""")
