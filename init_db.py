from sqlalchemy import create_engine
from models import Base

if __name__ == '__main__':
    engine = create_engine('postgresql://justin@localhost:5432/jlistings')
    Base.metadata.create_all(engine)
    print('Database schema created!')
