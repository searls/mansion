from models import Listing
from sqlalchemy.orm import Session
from datetime import datetime

def upsert_listings(session: Session, listings):
    count_new = 0
    count_updated = 0
    for listing in listings:
        existing = session.query(Listing).filter_by(suumo_id=listing.get('suumo_id'), source='suumo').first()
        if existing:
            for field in ['title', 'url', 'price', 'address', 'station', 'area', 'layout', 'balcony', 'built', 'new_or_used']:
                setattr(existing, field, listing.get(field))
            existing.updated_at = datetime.utcnow()
            count_updated += 1
        else:
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
                suumo_id=listing.get('suumo_id'),
                new_or_used=listing.get('new_or_used')
            ))
            count_new += 1
    session.commit()
    return {'inserted': count_new, 'updated': count_updated}
