#!/usr/bin/env python3
"""
Core calculation functions for Property Deal Analyzer.
Separated for easy testing and reuse.
"""

from config import config


def calculate_bsd(price: float) -> tuple:
    """
    Calculate Buyer's Stamp Duty with breakdown.
    
    BSD is progressive:
    - 1% on first $180,000
    - 2% on next $460,000 (up to $640,000)
    - 3% on next $360,000 (up to $1,000,000)
    - 4% on next $500,000 (up to $1,500,000)
    - 5% on next $1,500,000 (up to $3,000,000)
    - 6% on remaining amount
    
    Returns:
        (total_bsd, breakdown_list)
    """
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
    """
    Calculate Additional Buyer's Stamp Duty.
    
    Rates (2024):
    - Singaporean 1st property: 0%
    - Singaporean 2nd property: 20%
    - Singaporean 3rd+ property: 30%
    - PR 1st property: 5%
    - PR 2nd property: 30%
    - Foreigner: 60%
    - Entity (company/trust): 65%
    
    Returns:
        (absd_amount, description)
    """
    rate, description = config.get_absd_rate(buyer_type)
    return price * rate, description


def calculate_mortgage_monthly(
    loan_amount: float,
    years: int = None,
    interest_rate: float = None
) -> float:
    """
    Calculate monthly mortgage payment using standard amortization formula.
    
    Formula: M = P * (r(1+r)^n) / ((1+r)^n - 1)
    Where:
        M = monthly payment
        P = principal (loan amount)
        r = monthly interest rate (annual / 12)
        n = number of payments (years * 12)
    
    Args:
        loan_amount: Total loan amount
        years: Loan tenure in years (default from config)
        interest_rate: Annual interest rate as decimal (default from config)
    
    Returns:
        Monthly payment amount
    """
    if years is None:
        years = config.loan_tenure
    if interest_rate is None:
        interest_rate = config.interest_rate
    
    monthly_rate = interest_rate / 12
    num_payments = years * 12
    
    # Handle zero interest edge case
    if monthly_rate == 0:
        return loan_amount / num_payments
    
    # Standard amortization formula
    payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    
    return payment


def calculate_rental_yield(price: float, monthly_rent: float) -> float:
    """
    Calculate gross rental yield.
    
    Formula: (Annual Rent / Purchase Price) × 100
    
    Benchmarks:
    - HDB: 3.5-4.5%
    - Condo: 3.0-3.5%
    - Landed: 2.0-2.5%
    """
    if price <= 0:
        return 0
    annual_rent = monthly_rent * 12
    return (annual_rent / price) * 100


def calculate_tdsr(monthly_mortgage: float, other_debts: float, monthly_income: float) -> float:
    """
    Calculate Total Debt Servicing Ratio.
    
    Singapore limit: 55%
    
    Formula: (Total Monthly Debt / Monthly Income) × 100
    """
    if monthly_income <= 0:
        return float('inf')
    total_debt = monthly_mortgage + other_debts
    return (total_debt / monthly_income) * 100


def can_qualify_for_loan(tdsr: float, max_tdsr: float = 55.0) -> bool:
    """
    Check if buyer can qualify for loan based on TDSR.
    
    Args:
        tdsr: Total Debt Servicing Ratio percentage
        max_tdsr: Maximum allowed TDSR (default 55% for Singapore)
    
    Returns:
        True if can qualify, False otherwise
    """
    # Round to 2 decimal places to avoid floating point precision issues
    return round(tdsr, 2) <= max_tdsr


# Example usage and verification
if __name__ == '__main__':
    print("Calculation Examples")
    print("=" * 50)
    
    # BSD example
    price = 1_200_000
    bsd, breakdown = calculate_bsd(price)
    print(f"\nBSD for ${price:,.0f} property:")
    for line in breakdown:
        print(line)
    print(f"Total BSD: ${bsd:,.0f}")
    
    # ABSD example
    absd, desc = calculate_absd(price, 'singaporean_second')
    print(f"\nABSD (2nd property): ${absd:,.0f} ({desc})")
    
    # Mortgage example
    loan = 900_000
    monthly = calculate_mortgage_monthly(loan, 25, 0.035)
    print(f"\nMortgage for ${loan:,.0f} loan:")
    print(f"Monthly payment: ${monthly:,.0f}")
    
    # Rental yield example
    yield_pct = calculate_rental_yield(1_200_000, 3_500)
    print(f"\nRental yield: {yield_pct:.1f}%")
    
    # TDSR example
    tdsr = calculate_tdsr(5_000, 1_000, 10_000)
    can_qualify = can_qualify_for_loan(tdsr)
    print(f"\nTDSR: {tdsr:.1f}%")
    print(f"Can qualify: {'Yes' if can_qualify else 'No'}")
