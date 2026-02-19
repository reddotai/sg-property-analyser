#!/usr/bin/env python3
"""
Property Deal Analyzer
Extracts and analyzes PropertyGuru listings for true costs.
"""

import sys
from typing import Optional

from models import PropertyListing
from config import config
from validators import validate_price, validate_size, validate_district, sanitize_input
from market_data import (
    analyze_market, print_market_analysis,
    get_price_history, print_price_history
)
from calculations import (
    calculate_bsd, calculate_absd, calculate_mortgage_monthly,
    calculate_rental_yield
)


def get_input(prompt: str, input_type: type = str, default=None, validator=None, help_text=None):
    """Get validated input from user with helpful error messages."""
    while True:
        try:
            if help_text:
                print(f"  💡 {help_text}")
            
            full_prompt = prompt
            if default is not None:
                full_prompt += f" (default: {default}): "
            else:
                full_prompt += ": "
            
            value = input(full_prompt).strip()
            
            if not value and default is not None:
                return default
            
            if not value:
                print("  ⚠️  This field is required. Please enter a value.")
                continue
            
            # Sanitize input
            value = sanitize_input(value)
            
            # Convert type
            if input_type == int:
                value = int(value.replace(',', ''))
            elif input_type == float:
                value = float(value.replace(',', ''))
            
            # Run custom validator
            if validator:
                if input_type in (int, float):
                    is_valid, error_msg = validator(value)
                else:
                    is_valid = validator(value)
                    error_msg = "Invalid input" if not is_valid else ""
                
                if not is_valid:
                    print(f"  ⚠️  {error_msg}")
                    continue
            
            return value
        except ValueError:
            type_name = "number" if input_type in (int, float) else input_type.__name__.lower()
            example = "1200000" if input_type in (int, float) else "text"
            print(f"  ⚠️  Please enter a valid {type_name} (e.g., {example})")
        except (KeyboardInterrupt, EOFError):
            print("\n\nCancelled.")
            sys.exit(0)


def calculate_bsd(price: float) -> tuple:
    """Calculate Buyer's Stamp Duty with breakdown."""
    total = 0
    breakdown = []
    
    for min_price, max_price, rate, description in config.get_bsd_tiers():
        if price > min_price:
            taxable = min(price, max_price) - min_price
            amount = taxable * rate
            total += amount
            if amount > 0:
                breakdown.append(f"  • {description}: ${amount:,.0f}")
    
    return total, breakdown


def calculate_absd(price: float, buyer_type: str = 'singaporean_first') -> tuple:
    """Calculate Additional Buyer's Stamp Duty."""
    rate, description = config.get_absd_rate(buyer_type)
    return price * rate, description


def calculate_mortgage_monthly(
    loan_amount: float,
    years: int = None,
    interest_rate: float = None
) -> float:
    """Calculate monthly mortgage payment."""
    if years is None:
        years = config.loan_tenure
    if interest_rate is None:
        interest_rate = config.interest_rate
    
    monthly_rate = interest_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return loan_amount / num_payments
    
    payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment


def estimate_maintenance_fee(property_type: str, district: int) -> float:
    """Estimate maintenance fee based on property type and district."""
    premium_districts = {1, 2, 4, 9, 10, 11}
    
    base_fees = {
        'hdb': 80,
        'condo': 400 if district in premium_districts else 300,
        'landed': 0
    }
    
    return base_fees.get(property_type, 300)


def estimate_market_rent(listing: PropertyListing) -> Optional[float]:
    """Rough rental estimate based on property type and size."""
    if not listing.size_sqft or listing.size_sqft <= 0:
        return None
    
    rent_psf = {
        'hdb': 2.5,
        'condo': 4.0 if listing.district in {9, 10, 11} else 3.5,
        'landed': 2.0
    }
    
    rate = rent_psf.get(listing.property_type, 3.0)
    return listing.size_sqft * rate


def estimate_rental_yield(price: float, monthly_rent: float) -> float:
    """Calculate gross rental yield."""
    if price <= 0:
        return 0
    annual_rent = monthly_rent * 12
    return (annual_rent / price) * 100


def get_yield_benchmark(property_type: str) -> str:
    """Get benchmark yield for comparison."""
    benchmarks = {
        'hdb': "3.5-4.5%",
        'condo': "3.0-3.5%",
        'landed': "2.0-2.5%"
    }
    return benchmarks.get(property_type, "3.0-4.0%")


def analyze_deal(listing: PropertyListing, buyer_type: str = 'singaporean_first', is_hdb: bool = False) -> dict:
    """Full financial analysis of a property deal."""
    if not listing.price:
        raise ValueError("Price is required for analysis")
    
    if listing.price <= 0:
        raise ValueError("Price must be positive")
    
    price = listing.price
    
    # Calculate duties
    bsd, bsd_breakdown = calculate_bsd(price)
    absd, absd_desc = calculate_absd(price, buyer_type)
    
    # Estimate other costs
    legal_fees = config.legal_fees
    agent_commission = price * 0.01 if not is_hdb else 0
    
    # Mortgage calculations
    ltv_key = 'first_loan'
    if 'second' in buyer_type:
        ltv_key = 'second_loan'
    elif 'third' in buyer_type:
        ltv_key = 'third_loan'
    
    ltv, ltv_desc = config.get_ltv_limit(ltv_key)
    
    loan_amount = price * ltv
    down_payment = price - loan_amount
    monthly_mortgage = calculate_mortgage_monthly(loan_amount)
    
    # Monthly costs
    maintenance = listing.maintenance_fee or estimate_maintenance_fee(
        listing.property_type, listing.district or 19
    )
    property_tax = price * 0.0004 / 12
    
    total_upfront = down_payment + bsd + absd + legal_fees + agent_commission
    total_monthly = monthly_mortgage + maintenance + property_tax
    
    # HDB grants
    hdb_grants = 0
    if is_hdb and 'singaporean_first' in buyer_type:
        hdb_grants = config.hdb_grants.get('ehg_families', 0)
    
    return {
        'price': price,
        'bsd': bsd,
        'bsd_breakdown': bsd_breakdown,
        'absd': absd,
        'absd_desc': absd_desc,
        'legal_fees': legal_fees,
        'agent_commission': agent_commission,
        'down_payment': down_payment,
        'loan_amount': loan_amount,
        'ltv_desc': ltv_desc,
        'total_upfront': total_upfront,
        'monthly_mortgage': monthly_mortgage,
        'monthly_maintenance': maintenance,
        'monthly_property_tax': property_tax,
        'total_monthly': total_monthly,
        'psf': listing.psf,
        'hdb_grants': hdb_grants,
        'is_hdb': is_hdb
    }


def format_currency(amount: float) -> str:
    """Format as Singapore dollars."""
    return f"${amount:,.0f}"


def print_glossary():
    """Print explanation of terms."""
    print("\n" + "="*60)
    print("📚 QUICK REFERENCE GUIDE")
    print("="*60)
    print("""
BSD (Buyer's Stamp Duty): Tax on property purchase
  • Progressive rate: 1% to 6% based on price
  • Everyone pays this

ABSD (Additional Buyer's Stamp Duty): Extra tax for certain buyers
  • Singaporean 1st property: 0%
  • Singaporean 2nd property: 20%
  • PR 1st property: 5%
  • Foreigner: 60%

PSF (Price Per Square Foot): Price ÷ Size
  • Used to compare properties of different sizes
  • Lower PSF = better value (usually)

LTV (Loan-to-Value): How much bank will lend
  • 1st property: Up to 75%
  • 2nd property: Up to 45%
  • 3rd+ property: Up to 35%

Cashflow: Rental income minus monthly costs
  • Positive = Property pays for itself
  • Negative = You pay the difference

Rental Yield: Annual rent ÷ Purchase price
  • Higher = better investment return
  • HDB: 3.5-4.5%, Condo: 3.0-3.5%
""")
    print("="*60 + "\n")


def print_analysis(listing: PropertyListing, analysis: dict, show_breakdown: bool = False):
    """Print formatted analysis."""
    print("\n" + "="*60)
    print(f"📍  {listing.address or listing.title or 'Property Analysis'}")
    print(f"💰  Asking: {format_currency(analysis['price'])}")
    if listing.size_sqft:
        print(f"📏  {listing.size_sqft:,.0f} sqft | {format_currency(analysis['psf'])} psf")
    if listing.bedrooms:
        print(f"🛏️   {listing.bedrooms} bed, {listing.bathrooms or '?'} bath")
    if listing.lease_years_remaining:
        print(f"⏱️   {listing.lease_years_remaining} years lease remaining")
    
    print("\n" + "-"*60)
    print("BUYER COSTS")
    print("-"*60)
    
    print(f"BSD (Buyer's Stamp Duty): {format_currency(analysis['bsd'])}")
    if show_breakdown and analysis['bsd_breakdown']:
        for line in analysis['bsd_breakdown']:
            print(line)
    
    if analysis['absd'] > 0:
        print(f"ABSD: {format_currency(analysis['absd'])}")
        print(f"      ({analysis['absd_desc']})")
    else:
        print(f"ABSD: $0 (No ABSD for this buyer type)")
    
    print(f"Legal fees: {format_currency(analysis['legal_fees'])}")
    
    if analysis['agent_commission'] > 0:
        print(f"Agent commission: {format_currency(analysis['agent_commission'])}")
    else:
        print(f"Agent commission: $0 (Seller typically pays for HDB)")
    
    print(f"Down payment: {format_currency(analysis['down_payment'])}")
    print(f"              ({analysis['ltv_desc']})")
    
    if analysis['hdb_grants'] > 0:
        print(f"HDB Grants: -{format_currency(analysis['hdb_grants'])}")
    
    net_upfront = analysis['total_upfront'] - analysis['hdb_grants']
    print(f"\nTOTAL UPFRONT: {format_currency(net_upfront)}")
    
    print("\n" + "-"*60)
    print("MONTHLY COSTS")
    print("-"*60)
    print(f"Mortgage: {format_currency(analysis['monthly_mortgage'])}")
    print(f"          ({config.loan_tenure} years @ {config.interest_rate*100:.1f}% interest)")
    print(f"Maintenance: {format_currency(analysis['monthly_maintenance'])}")
    print(f"Property tax: {format_currency(analysis['monthly_property_tax'])}")
    print(f"\nTOTAL MONTHLY: {format_currency(analysis['total_monthly'])}")
    
    # Investment metrics
    estimated_rent = estimate_market_rent(listing)
    if estimated_rent:
        yield_pct = estimate_rental_yield(analysis['price'], estimated_rent)
        cashflow = estimated_rent - analysis['total_monthly']
        benchmark = get_yield_benchmark(listing.property_type or 'condo')
        
        print("\n" + "-"*60)
        print("INVESTMENT ANALYSIS")
        print("-"*60)
        print(f"Est. rental income: {format_currency(estimated_rent)}/month")
        print(f"Rental yield: {yield_pct:.1f}%")
        print(f"              (Benchmark: {benchmark})")
        
        cashflow_status = "POSITIVE ✅" if cashflow > 0 else "NEGATIVE ⚠️"
        print(f"Cashflow: {format_currency(cashflow)}/month ({cashflow_status})")
        
        if cashflow < 0:
            print(f"\n⚠️  You'll need {format_currency(abs(cashflow))}/month from other income")
    
    # Warnings
    print("\n" + "-"*60)
    print("NOTES")
    print("-"*60)
    
    if listing.lease_years_remaining and listing.lease_years_remaining < 60:
        print(f"⚠️  LEASE DECAY: Only {listing.lease_years_remaining} years remaining")
    elif listing.lease_years_remaining and listing.lease_years_remaining < 80:
        print(f"ℹ️  Lease remaining: {listing.lease_years_remaining} years")
    
    if analysis['absd'] > 0:
        absd_pct = (analysis['absd'] / analysis['price']) * 100
        print(f"⚠️  HIGH ABSD: {format_currency(analysis['absd'])} ({absd_pct:.0f}%)")
    
    print("="*60 + "\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h'):
        print("""
Property Deal Analyzer - Singapore Property Financial Calculator

Usage:
  python analyze_property.py --manual     Interactive mode
  python analyze_property.py --glossary   Show term explanations
  python analyze_property.py <URL>        Analyze PropertyGuru listing

Examples:
  python analyze_property.py --manual
  python analyze_property.py --glossary
        """)
        sys.exit(0)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--glossary':
        print_glossary()
        sys.exit(0)
    
    print("="*60)
    print("🏠 PROPERTY DEAL ANALYZER")
    print("Singapore Property Financial Calculator")
    print("="*60)
    
    # Default to manual mode
    print("\nEnter property details below. Press Ctrl+C to cancel.\n")
    
    # Get property details with validation
    price = get_input(
        "Price ($)",
        float,
        validator=validate_price,
        help_text="Asking price (e.g., 1200000)"
    )
    
    size_sqft = get_input(
        "Size (sqft)",
        float,
        validator=validate_size,
        help_text="Floor area in square feet"
    )
    
    bedrooms = get_input(
        "Bedrooms",
        int,
        help_text="Number of bedrooms"
    )
    
    bathrooms = get_input(
        "Bathrooms",
        int,
        help_text="Number of bathrooms"
    )
    
    print("\n  💡 Property types: HDB (public), Condo (private), Landed")
    property_type = get_input(
        "Property type",
        str,
        default='condo',
        validator=lambda x: x.lower() in ['hdb', 'condo', 'landed']
    ).lower()
    
    is_hdb = property_type == 'hdb'
    
    print("\n  💡 Tenure: Freehold (forever), 999-year, or 99-year lease")
    tenure = get_input(
        "Tenure",
        str,
        default='99',
        validator=lambda x: x.lower() in ['freehold', '999', '99']
    ).lower()
    
    lease_years_remaining = None
    if tenure in ['99', '999']:
        lease_years_remaining = get_input(
            "Years remaining on lease",
            int,
            help_text="Years left on lease"
        )
    
    address = get_input(
        "Address",
        str,
        default="Property",
        help_text="Property address or name"
    )
    
    print("\n  💡 Districts 1-28. Check propertyguru.com.sg/district-guides")
    district = get_input(
        "District",
        int,
        default=19,
        validator=validate_district
    )
    
    listing = PropertyListing(
        url="manual",
        price=price,
        size_sqft=size_sqft,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        tenure=tenure,
        lease_years_remaining=lease_years_remaining,
        property_type=property_type,
        district=district,
        address=address
    )
    
    # Validate listing
    errors = listing.validate()
    if errors:
        print("\n❌ Validation errors:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    
    # Determine buyer type
    print("\n" + "="*60)
    print("BUYER TYPE")
    print("="*60)
    print("1. Singaporean - 1st property (0% ABSD)")
    print("2. Singaporean - 2nd property (20% ABSD)")
    print("3. Singaporean - 3rd+ property (30% ABSD)")
    print("4. PR - 1st property (5% ABSD)")
    print("5. Foreigner (60% ABSD)")
    
    choice = get_input("Select", int, default=1, 
                      validator=lambda x: (1 <= x <= 5, "Please enter 1-5"))
    
    buyer_types = {
        1: 'singaporean_first',
        2: 'singaporean_second',
        3: 'singaporean_third',
        4: 'pr_first',
        5: 'foreigner'
    }
    buyer_type = buyer_types.get(choice, 'singaporean_first')
    
    # Run analysis
    try:
        analysis = analyze_deal(listing, buyer_type, is_hdb)
        print_analysis(listing, analysis, show_breakdown=True)
    except ValueError as e:
        print(f"\n❌ Analysis error: {e}")
        sys.exit(1)
    
    # Market analysis
    if listing.district and listing.price and listing.size_sqft:
        print("Fetching market data...")
        try:
            market = analyze_market(
                target_price=listing.price,
                target_size=listing.size_sqft,
                district=listing.district,
                property_type=listing.property_type or 'condo'
            )
            print_market_analysis(market)
            
            history = get_price_history(listing.address or "Property", listing.property_type or 'condo')
            print_price_history(history)
        except Exception as e:
            print(f"⚠️  Could not fetch market data: {e}")
    
    print("\n💡 Tip: Run with --glossary to see explanations of all terms")
    print("="*60)


if __name__ == '__main__':
    main()
