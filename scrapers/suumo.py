from bs4 import BeautifulSoup
import os

class SuumoScraper:
    def scrape(self, query=None):
        import requests
        from urllib.parse import quote
        # Always fetch live data from Suumo using the query
        if not query:
            raise ValueError('A query is required to scrape Suumo listings.')
        url = f"https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&fw={quote(query)}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
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
