import os
from concurrent.futures import ThreadPoolExecutor
from scrapers.suumo import SuumoScraper
from scrapers.lifeful import LifefulScraper
from scrapers.athome import AtHomeScraper
from models import Listing, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def main(query, region=None):
    engine = create_engine('postgresql://justin@localhost:5432/jlistings')
    Session = sessionmaker(bind=engine)
    session = Session()
    scrapers = [
        ('Suumo', SuumoScraper()),
        ('Lifeful', LifefulScraper()),
        ('AtHome', AtHomeScraper())
    ]
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for name, scraper in scrapers:
            if name == 'Suumo':
                futures[executor.submit(scraper.scrape, query, region)] = name
            else:
                futures[executor.submit(scraper.scrape, query)] = name
        for future in futures:
            name = futures[future]
            try:
                listings = future.result()
                print(f'[{name}] Found {len(listings)} listings')
                if listings:
                    for listing in listings:
                        print(listing)
                        if name == 'Suumo':
                            session.add(Listing(
                                source='suumo',
                                title=listing.get('title'),
                                url=listing.get('url'),
                                price=listing.get('price'),
                                address=listing.get('address'),
                                station=listing.get('station'),
                                area=listing.get('area'),
                                layout=listing.get('layout'),
                                balcony=listing.get('balcony'),
                                built=listing.get('built'),
                                property_name=listing.get('物件名'),
                                suumo_id=listing.get('suumo_id'),
                                new_or_used=listing.get('new_or_used')
                            ))
                        # ...existing code for other scrapers...
                    session.commit()
                else:
                    print(f'[{name}] No listings found.')
            except Exception as e:
                print(f'[{name}] Error: {e}')
    print('Done!')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python main.py <keyword> [region_code]')
        exit(1)
    query = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else None
    main(query, region)
