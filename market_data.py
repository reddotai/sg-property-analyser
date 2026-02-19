#!/usr/bin/env python3
"""
Market data module for Property Deal Analyzer.
Fetches nearby transactions and price history.
"""

import json
import re
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests

from models import PropertyListing


@dataclass
class Transaction:
    """A single property transaction record."""
    address: str
    property_type: str
    size_sqft: float
    price: float
    date: str
    tenure: Optional[str] = None
    is_simulated: bool = True  # Flag to indicate if this is simulated data
    
    @property
    def psf(self) -> float:
        if self.size_sqft and self.size_sqft > 0:
            return self.price / self.size_sqft
        return 0


@dataclass
class MarketAnalysis:
    """Analysis of market data for a property."""
    target_psf: float
    avg_nearby_psf: float
    median_nearby_psf: float
    min_nearby_psf: float
    max_nearby_psf: float
    transactions: List[Transaction]
    price_trend: str  # 'rising', 'falling', 'stable'
    is_simulated: bool = True  # Flag to indicate if data is simulated
    data_source: str = "simulated"  # 'ura_api', 'simulated', 'cached'
    generated_at: datetime = None
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()
    
    @property
    def vs_market(self) -> float:
        """Percentage vs market average."""
        if self.avg_nearby_psf > 0:
            return ((self.target_psf - self.avg_nearby_psf) / self.avg_nearby_psf) * 100
        return 0
    
    @property
    def deal_rating(self) -> str:
        """Rate the deal based on market comparison."""
        vs = self.vs_market
        if vs < -10:
            return "🔥 GOOD DEAL"
        elif vs < -5:
            return "✓ Fair Price"
        elif vs < 5:
            return "→ Market Rate"
        elif vs < 15:
            return "⚠️ Above Market"
        else:
            return "❌ Overpriced"


def get_ura_transactions(
    district: int,
    property_type: str,
    months: int = 6
) -> List[Transaction]:
    """
    Fetch transaction data from URA (Urban Redevelopment Authority).
    
    NOTE: This currently returns SIMULATED data for demonstration purposes.
    In production, this should integrate with the actual URA API.
    """
    # District price multipliers (rough approximation)
    district_multipliers = {
        9: 2.0, 10: 1.9, 11: 1.7, 1: 1.6, 2: 1.5, 4: 1.4,
        15: 1.5, 16: 1.3, 18: 1.2, 19: 1.2, 20: 1.3, 21: 1.4,
        22: 1.1, 23: 1.0, 24: 0.9, 25: 0.9, 26: 0.9, 27: 0.9, 28: 1.0,
    }
    
    base_psf = {
        'condo': 1400,
        'hdb': 500,
        'landed': 1200
    }.get(property_type, 1200)
    
    multiplier = district_multipliers.get(district, 1.0)
    avg_psf = base_psf * multiplier
    
    # Generate simulated transactions
    transactions = []
    sizes = [800, 900, 1000, 1100, 1200, 1300, 1500]
    streets = ["Street 1", "Street 2", "Avenue 3", "Road 4", "Drive 5"]
    
    for i in range(10):
        size = sizes[i % len(sizes)]
        variance = (hash(f"{district}{i}") % 20 - 10) / 100
        psf = avg_psf * (1 + variance)
        price = psf * size
        
        days_ago = (i * 15) % (months * 30)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        transactions.append(Transaction(
            address=f"Block {100 + i*10} {streets[i % len(streets)]}, District {district}",
            property_type=property_type,
            size_sqft=size,
            price=price,
            date=date,
            tenure='99' if property_type == 'condo' else 'freehold',
            is_simulated=True
        ))
    
    return sorted(transactions, key=lambda x: x.date, reverse=True)


def analyze_market(
    target_price: float,
    target_size: float,
    district: int,
    property_type: str
) -> MarketAnalysis:
    """Analyze market data and compare target property."""
    
    if target_size <= 0:
        raise ValueError("Target size must be positive")
    
    target_psf = target_price / target_size
    transactions = get_ura_transactions(district, property_type)
    
    if not transactions:
        return MarketAnalysis(
            target_psf=target_psf,
            avg_nearby_psf=0,
            median_nearby_psf=0,
            min_nearby_psf=0,
            max_nearby_psf=0,
            transactions=[],
            price_trend='unknown',
            is_simulated=True,
            data_source='simulated'
        )
    
    psf_values = [t.psf for t in transactions if t.psf > 0]
    
    if not psf_values:
        raise ValueError("No valid PSF data in transactions")
    
    avg_psf = sum(psf_values) / len(psf_values)
    median_psf = sorted(psf_values)[len(psf_values) // 2]
    min_psf = min(psf_values)
    max_psf = max(psf_values)
    
    # Determine trend
    recent = [t for t in transactions 
              if t.date >= (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")]
    older = [t for t in transactions 
             if t.date < (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")]
    
    if recent and older:
        recent_avg = sum(t.psf for t in recent) / len(recent)
        older_avg = sum(t.psf for t in older) / len(older)
        if recent_avg > older_avg * 1.05:
            trend = 'rising'
        elif recent_avg < older_avg * 0.95:
            trend = 'falling'
        else:
            trend = 'stable'
    else:
        trend = 'stable'
    
    return MarketAnalysis(
        target_psf=target_psf,
        avg_nearby_psf=avg_psf,
        median_nearby_psf=median_psf,
        min_nearby_psf=min_psf,
        max_nearby_psf=max_psf,
        transactions=transactions,
        price_trend=trend,
        is_simulated=True,
        data_source='simulated'
    )


def print_market_analysis(analysis: MarketAnalysis):
    """Print formatted market analysis."""
    print("\n" + "="*60)
    print("📊 MARKET ANALYSIS")
    
    # Show simulated data warning
    if analysis.is_simulated:
        print("⚠️  NOTE: Using simulated data for demonstration")
        print("   Connect to URA API for real transaction data")
    
    print("="*60)
    
    print(f"\n{analysis.deal_rating}")
    print(f"Target PSF: ${analysis.target_psf:,.0f}")
    print(f"Market Average: ${analysis.avg_nearby_psf:,.0f}")
    print(f"vs Market: {analysis.vs_market:+.1f}%")
    
    print(f"\nMarket Range:")
    print(f"  Min: ${analysis.min_nearby_psf:,.0f} psf")
    print(f"  Median: ${analysis.median_nearby_psf:,.0f} psf")
    print(f"  Max: ${analysis.max_nearby_psf:,.0f} psf")
    
    trend_emoji = {'rising': '📈', 'falling': '📉', 'stable': '➡️', 'unknown': '❓'}
    print(f"\nMarket Trend: {trend_emoji.get(analysis.price_trend, '❓')} {analysis.price_trend.upper()}")
    
    print(f"\nRecent Transactions (last 6 months):")
    print("-" * 60)
    for t in analysis.transactions[:5]:
        sim_marker = " [SIM]" if t.is_simulated else ""
        print(f"{t.date} | ${t.psf:,.0f}/sqft | ${t.price:,.0f} | {t.size_sqft:,.0f} sqft{sim_marker}")
    
    print("="*60 + "\n")


def get_price_history(
    address: str,
    property_type: str
) -> List[Dict]:
    """
    Get historical price data for a specific property/area.
    Returns simulated data with clear indication.
    """
    history = []
    base_price = 1_000_000
    
    for i in range(12):
        date = (datetime.now() - timedelta(days=i*30)).strftime("%Y-%m")
        variance = (i % 5 - 2) * 0.02
        price = base_price * (1 + variance)
        
        history.append({
            'date': date,
            'price': price,
            'psf': price / 1000,
            'is_simulated': True
        })
    
    return list(reversed(history))


def print_price_history(history: List[Dict]):
    """Print price history chart."""
    print("\n" + "="*60)
    print("📈 PRICE HISTORY (12 months)")
    print("⚠️  NOTE: Simulated data for demonstration")
    print("="*60)
    
    if not history:
        print("No historical data available.")
        return
    
    prices = [h['price'] for h in history]
    min_p = min(prices)
    max_p = max(prices)
    range_p = max_p - min_p if max_p != min_p else 1
    
    for h in history:
        bar_length = int(((h['price'] - min_p) / range_p) * 30) if range_p else 15
        bar = "█" * bar_length
        print(f"{h['date']} | ${h['price']:>10,.0f} | {bar}")
    
    if len(history) >= 12:
        yoy_change = ((history[-1]['price'] - history[0]['price']) / history[0]['price']) * 100
        print(f"\nYoY Change: {yoy_change:+.1f}%")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    print("Market Data Demo")
    print("="*60)
    
    analysis = analyze_market(
        target_price=1_250_000,
        target_size=1000,
        district=19,
        property_type='condo'
    )
    
    print_market_analysis(analysis)
    
    history = get_price_history("Sample Condo", "condo")
    print_price_history(history)
