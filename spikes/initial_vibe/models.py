from sqlalchemy import Column, Integer, String, Float, Date, Boolean, UniqueConstraint, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def normalize_listing_keys(address, property_name, area, layout):
    # Normalize by stripping whitespace, fixing encoding, and lowercasing
    def norm(val):
        if val is None:
            return None
        return str(val).strip().replace('\u3000', ' ').replace('\xa0', ' ').lower()
    return (
        norm(address),
        norm(property_name),
        norm(area),
        norm(layout)
    )

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
    homes_id = Column(String, unique=True, index=True)  # Unique code from Lifeful/Homes
    athome_id = Column(String, unique=True, index=True) # Unique code from AtHome
    new_or_used = Column(String)  # 'new' or 'used'
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint('address', 'property_name', 'area', 'layout', name='uq_listing_composite_key'),
    )
    # legacy/extra fields for future-proofing
    # prefecture, city, ward, neighborhood, building_number, latitude, longitude, is_new, construction_date, tax_amount, time_on_market
    # can be added as needed
