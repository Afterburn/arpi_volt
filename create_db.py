from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sql.stats_schema import Stats

Base   = declarative_base()

class Stats(Base):
    __tablename__ = "stats"
    id       = Column(Integer, primary_key=True)
    voltage  = Column(Float)
    lv_warn  = Column(Integer)
    time = Column(DateTime)

engine = create_engine('mysql+mysqldb://root:password@localhost')
engine.execute("CREATE DATABASE stats")
engine.execute("USE stats")

Base.metadata.create_all(engine)
