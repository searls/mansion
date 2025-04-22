from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .suumo.scrape import SuumoScraper
from .suumo.persist import upsert_listings

def fetch_listings(query, region=None, db_url='postgresql://justin@localhost:5432/jlistings'):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    scraper = SuumoScraper()
    listings = scraper.scrape(query, region)
    stats = upsert_listings(session, listings)
    return {'listings': listings, 'db_stats': stats}
