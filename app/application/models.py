from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime, event


class PackageType(Base):
    __tablename__ = "package_type"
    
    id_ = Column("id", Integer, primary_key=True)
    
    type_ = Column("type", String, nullable=False)

class Application(Base):
    __tablename__ = "application"
    
    id_ = Column("id", Integer, primary_key=True)
    
    city = Column("city", String, nullable=False)
    warehouse_id = Column("warehouse_id", Integer, ForeignKey("warehouse.id", ondelete="CASCADE"))
    addresss = Column("address", String, nullable=False)
    client_id = Column("client_id", ForeignKey("user.id", ondelete="CASCADE"))
    distance = Column("distance", Integer, nullable=False)
    ship_date = Column("ship_date", Date, nullable=False)
    ship_time = Column("ship_time", Time, nullable=False)
    comment = Column("comment", String, nullable=True)
    package_type_id = Column("package_type_id", Integer, ForeignKey("package_type.id", ondelete="CASCADE"))
    load_date = Column("load_date", DateTime, default=datetime.now())
    
    
class ApplicationStatusCurrent(Base):
    __tablename__ = "application_status_current"
    
    application_id = Column("application_id", ForeignKey("application.id", ondelete="CASCADE"), primary_key=True)
    status = Column("status", String, nullable=False)
    load_date = Column("load_date", DateTime, onupdate=datetime.now())
    
class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"
    
    application_id = Column("application_id", ForeignKey("application.id", ondelete="CASCADE"), primary_key=True)
    status = Column("status", String, nullable=False)
    load_date = Column("load_date", DateTime, default=datetime.now(), primary_key=True)
