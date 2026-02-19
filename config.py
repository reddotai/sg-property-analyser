#!/usr/bin/env python3
"""
Configuration and constants for Property Deal Analyzer.
"""

import os
from typing import List, Tuple

# BSD Tiers: (min, max, rate, description)
DEFAULT_BSD_TIERS: List[Tuple[float, float, float, str]] = [
    (0, 180000, 0.01, "1% on first $180,000"),
    (180000, 640000, 0.02, "2% on next $460,000"),
    (640000, 1000000, 0.03, "3% on next $360,000"),
    (1000000, 1500000, 0.04, "4% on next $500,000"),
    (1500000, 3000000, 0.05, "5% on next $1.5M"),
    (3000000, float('inf'), 0.06, "6% on remaining"),
]

# ABSD Rates: (rate, description)
DEFAULT_ABSD_RATES = {
    'singaporean_first': (0, "0% - No ABSD for first property"),
    'singaporean_second': (0.20, "20% - Second property"),
    'singaporean_third': (0.30, "30% - Third property onwards"),
    'pr_first': (0.05, "5% - PR buying first property"),
    'pr_second': (0.30, "30% - PR buying second property"),
    'foreigner': (0.60, "60% - Foreigner"),
    'entity': (0.65, "65% - Company/Trust"),
}

# LTV Limits: (rate, description)
DEFAULT_LTV_LIMITS = {
    'first_loan': (0.75, "75% - First property loan"),
    'second_loan': (0.45, "45% - Second property loan"),
    'third_loan': (0.35, "35% - Third property loan"),
}

# HDB Grants (2024)
DEFAULT_HDB_GRANTS = {
    'ehg_singles': 40000,
    'ehg_families': 80000,
    'phg': 30000,
    'fg': 50000,
}

# Default interest rate for mortgage calculations
DEFAULT_INTEREST_RATE = 0.035  # 3.5%

# Default loan tenure in years
DEFAULT_LOAN_TENURE = 25

# Legal fees estimate
DEFAULT_LEGAL_FEES = 3000

# Scraper timeout in milliseconds
DEFAULT_SCRAPE_TIMEOUT = 30000

# URA API Configuration
# Set URA_API_KEY environment variable to use real URA data
# Get your API key from: https://www.developer.tech.gov.sg/products/categories/data-and-apis/ura-apis/overview
URA_API_KEY = os.environ.get('URA_API_KEY', None)
URA_API_BASE_URL = "https://www.ura.gov.sg/uraDataService/invokeUraDS"


class Config:
    """Configuration class that reads from environment variables."""
    
    def __init__(self):
        self.interest_rate = float(os.environ.get('INTEREST_RATE', DEFAULT_INTEREST_RATE))
        self.loan_tenure = int(os.environ.get('LOAN_TENURE', DEFAULT_LOAN_TENURE))
        self.legal_fees = int(os.environ.get('LEGAL_FEES', DEFAULT_LEGAL_FEES))
        self.scrape_timeout = int(os.environ.get('SCRAPE_TIMEOUT', DEFAULT_SCRAPE_TIMEOUT))
        
        # URA API
        self.ura_api_key = URA_API_KEY
        self.ura_api_base_url = URA_API_BASE_URL
        
        # Allow overriding rates via environment (for testing or rate changes)
        self.bsd_tiers = DEFAULT_BSD_TIERS
        self.absd_rates = DEFAULT_ABSD_RATES
        self.ltv_limits = DEFAULT_LTV_LIMITS
        self.hdb_grants = DEFAULT_HDB_GRANTS
    
    def get_bsd_tiers(self):
        return self.bsd_tiers
    
    def get_absd_rate(self, buyer_type: str) -> tuple:
        return self.absd_rates.get(buyer_type, (0, ""))
    
    def get_ltv_limit(self, loan_type: str) -> tuple:
        return self.ltv_limits.get(loan_type, (0.75, ""))


# Global config instance
config = Config()
