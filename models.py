#!/usr/bin/env python3
"""
Shared models for Property Deal Analyzer.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PropertyListing:
    """Represents a property listing with all relevant details."""
    url: str
    title: Optional[str] = None
    price: Optional[float] = None
    size_sqft: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    tenure: Optional[str] = None  # 'freehold', '999', '99', etc.
    lease_years_remaining: Optional[int] = None
    property_type: Optional[str] = None  # 'condo', 'hdb', 'landed'
    district: Optional[int] = None
    address: Optional[str] = None
    maintenance_fee: Optional[float] = None
    
    @property
    def psf(self) -> Optional[float]:
        """Price per square foot."""
        if self.price and self.size_sqft and self.size_sqft > 0:
            return self.price / self.size_sqft
        return None
    
    def validate(self) -> list[str]:
        """Return list of validation errors."""
        errors = []
        
        if self.price is not None and self.price <= 0:
            errors.append("Price must be positive")
        
        if self.size_sqft is not None and self.size_sqft <= 0:
            errors.append("Size must be positive")
        
        if self.bedrooms is not None and self.bedrooms < 0:
            errors.append("Bedrooms cannot be negative")
        
        if self.bathrooms is not None and self.bathrooms < 0:
            errors.append("Bathrooms cannot be negative")
        
        if self.district is not None and not (1 <= self.district <= 28):
            errors.append("District must be between 1 and 28")
        
        if self.lease_years_remaining is not None and self.lease_years_remaining < 0:
            errors.append("Lease years remaining cannot be negative")
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if listing is valid."""
        return len(self.validate()) == 0
