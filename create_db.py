from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sql.stats_schema import Stats

Base   = declarative_base()

class Stats(Base):
    __tablename__ = "stats"
    id      = Column(Integer, primary_key=True)
    voltage = Column(Float)
    read_time = Column(DateTime)


engine = create_engine('sqlite:///stats.db')

#stats_schema.create_engine('sqlite:///stats.db')

Base.metadata.create_all(engine)
