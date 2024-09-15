from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional


class CreateApplication(BaseModel):
    city: str
    ship_address: str
    ship_date: date
    ship_time: time
    package_type_id: int
    comment: Optional[str] = Field(None)
    

class AfterApplicationCreated(BaseModel):
    application_id: int
    
    
class ShowApplication(BaseModel):
    application_id: int
    city: str
    ship_address: str
    warehouse_address: str
    ship_date: date
    ship_time: time
    package_type_id: int
    distance: int
    comment: Optional[str] = Field(None)
    status: str


class ShowApplicationStatus(BaseModel):
    application_id: int
    status: str

    
class UpdateApplication(BaseModel):
    city: str
    ship_address: Optional[str] = Field(None)
    package_type_id: Optional[str] = Field(None)
    ship_date: Optional[date] = Field(None)
    ship_time: Optional[time] = Field(None)
    comment: Optional[str] = Field(None)