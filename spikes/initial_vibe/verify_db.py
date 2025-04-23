from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Listing

engine = create_engine('postgresql://justin@localhost:5432/jlistings')
Session = sessionmaker(bind=engine)
session = Session()

print('Total listings:', session.query(Listing).count())
for listing in session.query(Listing).limit(10):
    print(listing.id, listing.title, listing.url)
