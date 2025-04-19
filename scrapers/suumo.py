from bs4 import BeautifulSoup
import os

class SuumoScraper:
    def scrape(self, query=None):
        # Parse the local fixture file for used manshon listings
        path = os.path.join(os.path.dirname(__file__), '../research/suumo-used-manshon-results.html')
        with open(path, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        results = []
        for card in soup.select('.property_unit'):
            data = {}
            # Title and link
            title_tag = card.select_one('.property_unit-title a')
            data['title'] = title_tag.get_text(strip=True) if title_tag else None
            data['url'] = 'https://suumo.jp' + title_tag['href'] if title_tag and title_tag.has_attr('href') else None
            # Extract suumo_id from the URL (e.g., nc_76757999)
            suumo_id = None
            if data['url']:
                import re
                m = re.search(r'/nc_(\d+)/', data['url'])
                if m:
                    suumo_id = m.group(1)
            data['suumo_id'] = suumo_id
            # Extract all <dt>/<dd> pairs in .property_unit-info
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
                        # Store any other fields for future reference
                        data[label] = value
            results.append(data)
        return results
