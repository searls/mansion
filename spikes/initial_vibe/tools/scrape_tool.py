"""
Scrape Tool: Fetches raw listings from a specified source.
Input: source (str: 'suumo', 'athome', 'homes'), keyword (str), region (str or None)
Output: List[dict] (raw listings)
"""

def scrape_listings(source, keyword, region=None):
    if source == 'suumo':
        from lib.adapters.suumo.scrape import SuumoScraper
        scraper = SuumoScraper()
        return scraper.scrape(keyword, region)
    elif source == 'athome':
        from scrapers.athome import AthomeScraper
        scraper = AthomeScraper()
        return scraper.scrape(keyword, region)
    elif source == 'homes':
        from scrapers.lifeful import LifefulScraper
        scraper = LifefulScraper()
        return scraper.scrape(keyword, region)
    else:
        raise ValueError(f"Unknown source: {source}")
