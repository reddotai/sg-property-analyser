#!/usr/bin/env python3
"""
Scraper for PropertyGuru Singapore listings.
Uses Playwright to extract property details.
"""

import re
from typing import Optional
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from models import PropertyListing
from validators import validate_url


# Allowed domains for scraping
ALLOWED_DOMAINS = ['propertyguru.com.sg', 'www.propertyguru.com.sg']


def parse_price(price_text: str) -> Optional[float]:
    """Extract numeric price from text like '$1,250,000' or 'S$ 1.25M'."""
    if not price_text:
        return None
    
    price_text = price_text.replace('S$', '').replace('$', '').replace(',', '').strip()
    
    if 'M' in price_text.upper():
        num_match = re.search(r'[\d.]+', price_text)
        if num_match:
            return float(num_match.group()) * 1000000
    
    if 'K' in price_text.upper():
        num_match = re.search(r'[\d.]+', price_text)
        if num_match:
            return float(num_match.group()) * 1000
    
    num_match = re.search(r'[\d.]+', price_text)
    if num_match:
        try:
            return float(num_match.group())
        except ValueError:
            return None
    
    return None


def parse_size(size_text: str) -> Optional[float]:
    """Extract size in sqft from text."""
    if not size_text:
        return None
    
    sqft_match = re.search(r'(\d[,\d]*)\s*sqft', size_text, re.IGNORECASE)
    if sqft_match:
        return float(sqft_match.group(1).replace(',', ''))
    
    sqm_match = re.search(r'(\d[,\d]*)\s*sqm', size_text, re.IGNORECASE)
    if sqm_match:
        sqm = float(sqm_match.group(1).replace(',', ''))
        return sqm * 10.764
    
    return None


def parse_bedrooms_bathrooms(text: str) -> tuple:
    """Extract bedroom and bathroom counts."""
    beds = None
    baths = None
    
    bed_match = re.search(r'(\d+)\s*bed', text, re.IGNORECASE)
    if bed_match:
        beds = int(bed_match.group(1))
    
    bath_match = re.search(r'(\d+)\s*bath', text, re.IGNORECASE)
    if bath_match:
        baths = int(bath_match.group(1))
    
    return beds, baths


def parse_tenure(text: str) -> tuple:
    """Extract tenure type and remaining years."""
    text = text.lower()
    
    if 'freehold' in text:
        return 'freehold', None
    
    if '999' in text:
        return '999', None
    
    lease_match = re.search(r'(\d+)[\s-]*year', text)
    if lease_match:
        total_years = int(lease_match.group(1))
        
        remaining_match = re.search(r'(\d+)\s*years?\s*(remaining|left)', text)
        if remaining_match:
            return str(total_years), int(remaining_match.group(1))
        
        return str(total_years), None
    
    return None, None


def scrape_propertyguru(url: str, headless: bool = True, timeout_ms: int = 30000) -> PropertyListing:
    """
    Scrape a PropertyGuru listing using Playwright.
    
    Args:
        url: PropertyGuru listing URL
        headless: Run browser in headless mode
        timeout_ms: Page load timeout in milliseconds
    
    Returns:
        PropertyListing with extracted data
    
    Raises:
        ValueError: If URL is invalid
        PlaywrightTimeout: If page fails to load
    """
    # Validate URL
    is_valid, error_msg = validate_url(url, ALLOWED_DOMAINS)
    if not is_valid:
        raise ValueError(f"Invalid URL: {error_msg}")
    
    listing = PropertyListing(url=url)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"Loading: {url}")
            page.goto(url, wait_until='networkidle', timeout=timeout_ms)
            
            # Wait for key elements
            page.wait_for_selector('h1, .listing-title, [data-testid="listing-title"]', timeout=10000)
            
            # Extract title
            try:
                title_elem = page.query_selector('h1, .listing-title, [data-testid="listing-title"]')
                if title_elem:
                    listing.title = title_elem.inner_text().strip()
            except Exception:
                pass
            
            # Extract price
            try:
                price_selectors = [
                    '[data-testid="listing-price"]',
                    '.listing-price',
                    '.price',
                    '[class*="price"]'
                ]
                for selector in price_selectors:
                    price_elem = page.query_selector(selector)
                    if price_elem:
                        price_text = price_elem.inner_text()
                        listing.price = parse_price(price_text)
                        if listing.price:
                            break
            except Exception:
                pass
            
            # Extract all text once for parsing
            try:
                page_text = page.inner_text('body')
                page_text_lower = page_text.lower()
                
                # Extract size
                listing.size_sqft = parse_size(page_text)
                
                # Extract bedrooms/bathrooms
                listing.bedrooms, listing.bathrooms = parse_bedrooms_bathrooms(page_text)
                
                # Extract tenure
                listing.tenure, listing.lease_years_remaining = parse_tenure(page_text)
                
                # Determine property type
                if 'condo' in page_text_lower or 'condominium' in page_text_lower:
                    listing.property_type = 'condo'
                elif 'hdb' in page_text_lower:
                    listing.property_type = 'hdb'
                elif 'landed' in page_text_lower or 'bungalow' in page_text_lower or 'terrace' in page_text_lower:
                    listing.property_type = 'landed'
                
                # Extract maintenance fee
                maint_match = re.search(r'\$([\d,]+)\s*(monthly|maintenance)', page_text_lower)
                if maint_match:
                    listing.maintenance_fee = float(maint_match.group(1).replace(',', ''))
                    
            except Exception:
                pass
            
            # Extract address
            try:
                address_selectors = [
                    '[data-testid="listing-address"]',
                    '.listing-address',
                    '.address'
                ]
                for selector in address_selectors:
                    addr_elem = page.query_selector(selector)
                    if addr_elem:
                        listing.address = addr_elem.inner_text().strip()
                        break
            except Exception:
                pass
            
        except PlaywrightTimeout:
            raise PlaywrightTimeout(f"Page failed to load within {timeout_ms}ms")
        except Exception as e:
            raise RuntimeError(f"Error scraping page: {str(e)}")
        finally:
            browser.close()
    
    return listing


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <propertyguru_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        listing = scrape_propertyguru(url, headless=True)
        
        print("\n" + "="*50)
        print("SCRAPED LISTING DETAILS")
        print("="*50)
        print(f"Title: {listing.title}")
        print(f"Price: ${listing.price:,.0f}" if listing.price else "Price: Not found")
        print(f"Size: {listing.size_sqft:,.0f} sqft" if listing.size_sqft else "Size: Not found")
        print(f"Bedrooms: {listing.bedrooms}")
        print(f"Bathrooms: {listing.bathrooms}")
        print(f"Tenure: {listing.tenure}")
        print(f"Lease remaining: {listing.lease_years_remaining}")
        print(f"Type: {listing.property_type}")
        print(f"Address: {listing.address}")
        print(f"PSF: ${listing.psf:,.0f}" if listing.psf else "PSF: N/A")
        print("="*50)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PlaywrightTimeout:
        print("Error: Page took too long to load. Try again later.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
