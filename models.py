from sqlalchemy import Column, Integer, String, Float, Date, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    suumo_id = Column(String, unique=True, index=True)  # Unique code from Suumo URL
    source = Column(String, nullable=False)  # suumo, lifeful, athome
    title = Column(String)
    url = Column(String)
    price = Column(String)
    address = Column(String)
    station = Column(String)
    area = Column(String)
    layout = Column(String)
    balcony = Column(String)
    built = Column(String)
    property_name = Column(String)
    # legacy/extra fields for future-proofing
    # prefecture, city, ward, neighborhood, building_number, latitude, longitude, is_new, construction_date, tax_amount, time_on_market
    # can be added as needed
