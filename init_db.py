from sqlalchemy import create_engine
from models import Base

engine = create_engine('postgresql://justin@localhost:5432/jlistings')
Base.metadata.create_all(engine)
