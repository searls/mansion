from bs4 import BeautifulSoup
import os
import json
import requests
import re
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

class SuumoScraper:
    def __init__(self):
        # Load the region lookup table once
        # Adjusted path relative to this file's new location
        lookup_path = os.path.join(os.path.dirname(__file__), '../../../research/suumo_areas.json')
        with open(lookup_path, encoding='utf-8') as f:
            self.region_lookup = json.load(f)

    def find_region_code(self, keyword):
        # Try direct match first
        for code, entry in self.region_lookup.items():
            if keyword in entry['keywords']:
                return code
        # Try to match by stripping common place suffixes
        base = re.sub(r'[市県町区村郡]$', '', keyword)
        candidates = []
        for code, entry in self.region_lookup.items():
            for k in entry['keywords']:
                if base and base in k:
                    candidates.append(code)
                    break
        if len(set(candidates)) == 1:
            return candidates[0]
        raise ValueError(f'Could not find region for keyword: {keyword}')

    def scrape(self, keyword, region=None):
        if not keyword:
            raise ValueError('A keyword is required to scrape Suumo listings.')
        region_code = region
        if not region_code:
            region_code = self.find_region_code(keyword)
        results = []
        for bs_code, new_or_used in [('010', 'new'), ('011', 'used')]:
            # ---
            # Mystery meat query params:
            # For used listings (bs=011):
            #   po=16 (sort by newest), pj=2 (descending), pc=100 (100 results per page), et=10 (10 min walk to station), md=2,3,4,5 (2-5+ LDK only)
            #   cnb=0&cn=10 (built in the last 10 years)
            # For new listings (bs=010):
            #   bknlistmodeflg=1 (required for new listings), pc=100 (100 results), po=5 (sort by price), pj=1 (ascending/cheapest first), md=2,3,4,5 (2-5+ LDK only)
            # ---
            if bs_code == '011':  # Used listings
                url = f"https://suumo.jp/jj/bukken/ichiran/JJ012FC001/?ar={region_code}&bs=011&md=2&md=3&md=4&md=5&et=10&fw={quote(keyword)}&po=16&pj=2&pc=100&cnb=0&cn=10"
            else:  # New listings
                url = f"https://suumo.jp/jj/bukken/ichiran/JJ011FC001/?ar={region_code}&bs=010&tj=0&po=5&pj=1&pc=100&fw={quote(keyword)}&md=2&md=3&md=4&md=5&bknlistmodeflg=1"
            logger.info(f"Scraping URL: {url}")
            try:
                resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                logger.warning(f"Error fetching {url}: {e}")
                continue # Skip this source if fetch fails

            if bs_code == '010': # New listings
                items = soup.select('.cassette_list-item')
                logger.info(f"Found {len(items)} new listing items for {keyword} in region {region_code}") # Debugging
                for li in items:
                    data = {}
                    title_tag = li.select_one('.cassette_header-title')
                    # Use English keys matching models.py
                    data['title'] = title_tag.get_text(strip=True) if title_tag else None
                    data['url'] = 'https://suumo.jp' + title_tag['href'] if title_tag and title_tag.has_attr('href') else None
                    suumo_id = None
                    if data['url']:
                        m = re.search(r'/(?:nc|jj)_(\d+)/', data['url']) # Handle nc_ and jj_
                        if m:
                            suumo_id = m.group(1)
                    data['suumo_id'] = suumo_id
                    addr = li.select_one('.cassette_basic-title:-soup-contains("所在地") + .cassette_basic-value')
                    data['address'] = addr.get_text(strip=True) if addr else None # Use English key
                    station = li.select_one('.cassette_basic-title:-soup-contains("交通") + .cassette_basic-value')
                    data['station'] = station.get_text(strip=True) if station else None # Use English key
                    price = li.select_one('.cassette_price-accent')
                    data['price'] = price.get_text(strip=True) if price else None # Use English key
                    desc = li.select_one('.cassette_price-description')
                    if desc:
                        desc_text = desc.get_text(strip=True)
                        m = re.match(r'(.+?)/(.+)', desc_text)
                        if m:
                            data['layout'] = m.group(1).strip() # Use English key
                            data['area'] = m.group(2).strip() # Use English key
                        else:
                            data['layout'] = desc_text
                            data['area'] = None
                    else:
                        data['layout'] = None
                        data['area'] = None
                    built = li.select_one('.cassette_basic-title:-soup-contains("引渡時期") + .cassette_basic-value') # Often completion date for new
                    data['built'] = built.get_text(strip=True) if built else None # Use English key
                    data['new_or_used'] = new_or_used
                    data['source'] = 'suumo' # Add source
                    if data.get('title'): # Basic validation using English key
                        results.append(data)

            else: # Used listings
                items = soup.select('.property_unit')
                logger.info(f"Found {len(items)} used listing items for {keyword} in region {region_code}") # Debugging
                for card in items:
                    data = {}
                    title_tag = card.select_one('.property_unit-title a')
                    # Use English keys matching models.py
                    data['title'] = title_tag.get_text(strip=True) if title_tag else None
                    data['url'] = 'https://suumo.jp' + title_tag['href'] if title_tag and title_tag.has_attr('href') else None
                    suumo_id = None
                    if data['url']:
                        m = re.search(r'/(?:nc|jj)_(\d+)/', data['url']) # Handle nc_ and jj_
                        if m:
                            suumo_id = m.group(1)
                    data['suumo_id'] = suumo_id
                    for dl in card.select('.property_unit-info .dottable-line'):
                        for pair in dl.select('dl'):
                            dt = pair.select_one('dt')
                            dd = pair.select_one('dd')
                            if not dt or not dd: continue
                            label = dt.get_text(strip=True)
                            value = dd.get_text(strip=True)
                            # Map labels directly to English keys
                            if label == '販売価格': data['price'] = value
                            elif label == '所在地': data['address'] = value
                            elif label == '沿線・駅': data['station'] = value
                            elif label == '専有面積': data['area'] = value
                            elif label == '間取り': data['layout'] = value
                            elif label == 'バルコニー': data['balcony'] = value # Use English key
                            elif label == '築年月': data['built'] = value
                            # else: data[label] = value # Avoid adding arbitrary keys
                    data['new_or_used'] = new_or_used
                    data['source'] = 'suumo' # Add source
                    if data.get('title'): # Basic validation using English key
                        results.append(data)
        logger.info(f"Scraping finished for {keyword}. Found {len(results)} total listings.") # Debugging
        return results
