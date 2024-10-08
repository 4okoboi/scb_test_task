from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Warehouse(Base):
    __tablename__ = "warehouse"
    
    id_ = Column("id", Integer, primary_key=True)
    city = Column("city", String, nullable=False)
    address = Column("address", String, nullable=False)
    geo_lat = Column("geo_lat", Float, nullable=False)
    geo_lon = Column("geo_lon", Float, nullable=False)

