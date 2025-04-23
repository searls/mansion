from bs4 import BeautifulSoup
import os
import json
from typing import Literal

class SuumoScraper:
    def __init__(self):
        # Load the region lookup table once
        lookup_path = os.path.join(os.path.dirname(__file__), '../research/suumo_areas.json')
        with open(lookup_path, encoding='utf-8') as f:
            self.region_lookup = json.load(f)

    def find_region_code(self, keyword):
        # Try direct match first
        for code, entry in self.region_lookup.items():
            if keyword in entry['keywords']:
                return code
        # Try to match by stripping common place suffixes
        import re
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

    def scrape(self, keyword, region=None, source: Literal['suumo'] = 'suumo'):
        if source != 'suumo':
            raise ValueError('source must be "suumo" for SuumoScraper')
        import requests
        from urllib.parse import quote
        if not keyword:
            raise ValueError('A keyword is required to scrape Suumo listings.')
        region_code = region
        if not region_code:
            region_code = self.find_region_code(keyword)
        results = []
        for bs_code, new_or_used in [('010', 'new'), ('011', 'used')]:
            url = f"https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar={region_code}&bs={bs_code}&fw={quote(keyword)}"
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            if bs_code == '010':
                # New listings: .cassette_list-item
                for li in soup.select('.cassette_list-item'):
                    data = {}
                    title_tag = li.select_one('.cassette_header-title')
                    data['title'] = title_tag.get_text(strip=True) if title_tag else None
                    data['url'] = 'https://suumo.jp' + title_tag['href'] if title_tag and title_tag.has_attr('href') else None
                    suumo_id = None
                    if data['url']:
                        import re
                        m = re.search(r'/nc_(\d+)/', data['url'])
                        if m:
                            suumo_id = m.group(1)
                    data['suumo_id'] = suumo_id
                    # Address
                    addr = li.select_one('.cassette_basic-title:contains("所在地") + .cassette_basic-value')
                    data['address'] = addr.get_text(strip=True) if addr else None
                    # Station
                    station = li.select_one('.cassette_basic-title:contains("交通") + .cassette_basic-value')
                    data['station'] = station.get_text(strip=True) if station else None
                    # Price (may be undecided)
                    price = li.select_one('.cassette_price-accent')
                    data['price'] = price.get_text(strip=True) if price else None
                    # Layout and area (in price description)
                    desc = li.select_one('.cassette_price-description')
                    if desc:
                        import re
                        desc_text = desc.get_text(strip=True)
                        m = re.match(r'(.+?)/(.+)', desc_text)
                        if m:
                            data['layout'] = m.group(1).strip()
                            data['area'] = m.group(2).strip()
                        else:
                            data['layout'] = desc_text
                            data['area'] = None
                    else:
                        data['layout'] = None
                        data['area'] = None
                    # Built (引渡時期)
                    built = li.select_one('.cassette_basic-title:contains("引渡時期") + .cassette_basic-value')
                    data['built'] = built.get_text(strip=True) if built else None
                    data['new_or_used'] = new_or_used
                    results.append(data)
            else:
                # Used listings: .property_unit (existing logic)
                for card in soup.select('.property_unit'):
                    data = {}
                    title_tag = card.select_one('.property_unit-title a')
                    data['title'] = title_tag.get_text(strip=True) if title_tag else None
                    data['url'] = 'https://suumo.jp' + title_tag['href'] if title_tag and title_tag.has_attr('href') else None
                    suumo_id = None
                    if data['url']:
                        import re
                        m = re.search(r'/nc_(\d+)/', data['url'])
                        if m:
                            suumo_id = m.group(1)
                    data['suumo_id'] = suumo_id
                    for dl in card.select('.property_unit-info .dottable-line'):
                        for pair in dl.select('dl'):
                            dt = pair.select_one('dt')
                            dd = pair.select_one('dd')
                            if not dt or not dd:
                                continue
                            label = dt.get_text(strip=True)
                            value = dd.get_text(strip=True)
                            if label == '販売価格':
                                data['price'] = value
                            elif label == '所在地':
                                data['address'] = value
                            elif label == '沿線・駅':
                                data['station'] = value
                            elif label == '専有面積':
                                data['area'] = value
                            elif label == '間取り':
                                data['layout'] = value
                            elif label == 'バルコニー':
                                data['balcony'] = value
                            elif label == '築年月':
                                data['built'] = value
                            else:
                                data[label] = value
                    data['new_or_used'] = new_or_used
                    results.append(data)
        return results
