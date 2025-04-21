import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
from models import Base

if __name__ == '__main__':
    engine = create_engine('postgresql://justin@localhost:5432/jlistings')
    # Drop all tables to ensure schema is rebuilt
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Database dropped and schema created!')
