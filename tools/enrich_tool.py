"""
Enrich Tool: Parses/structures address fields in listings.
Input: List[dict] (raw listings)
Output: List[dict] (enriched listings with structured address fields)
"""
import re

def parse_address(address):
    # Simple regex-based parser for Japanese addresses (prefecture, city, ward, chome)
    # This is a naive implementation and can be improved
    result = {
        'prefecture': None,
        'city': None,
        'ward': None,
        'chome': None
    }
    if not address:
        return result
    # Prefecture: ends with '県', '都', '府', or '道'
    m = re.match(r'^(.*?[都道府県])', address)
    if m:
        result['prefecture'] = m.group(1)
        rest = address[m.end():]
    else:
        rest = address
    # City: ends with '市', '区', '町', or '村' (first occurrence)
    m = re.match(r'^(.*?[市区町村])', rest)
    if m:
        result['city'] = m.group(1)
        rest = rest[m.end():]
    # Ward: ends with '区' (if not already captured as city)
    m = re.match(r'^(.*?区)', rest)
    if m and not result['city']:
        result['ward'] = m.group(1)
        rest = rest[m.end():]
    # Chome: e.g., '1丁目', '2丁目', etc.
    m = re.search(r'(\d+丁目)', rest)
    if m:
        result['chome'] = m.group(1)
    return result

def enrich_listings(raw_listings):
    enriched = []
    for listing in raw_listings:
        address = listing.get('address')
        structured = parse_address(address)
        enriched.append({**listing, **structured})
    return enriched
