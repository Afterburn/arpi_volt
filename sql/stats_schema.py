from . import *

class Stats(Base):
    __tablename__ = "stats"
    id      = Column(Integer, primary_key=True)
    voltage = Column(Float)
    time    = Column(Datetime)
    lv_warn = Column(Integer)


