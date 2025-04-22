# tools/test_supporter.py
"""
TestSupporter: Memoizes scrape_listings results for (source, query, region) tuples
across a process lifespan to avoid redundant scrapes in tests.
"""
from tools.scrape_tool import scrape_listings

class TestSupporter:
    _cache = {}

    @classmethod
    def get_listings(cls, source, query, region=None):
        key = (source, query, region)
        if key not in cls._cache:
            cls._cache[key] = scrape_listings(source, query, region)
        return cls._cache[key]
