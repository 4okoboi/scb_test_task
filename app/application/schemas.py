from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, validator
from datetime import date, datetime, time
from typing import Optional


class CreateApplication(BaseModel):
    city: str
    ship_address: str
    ship_date: date
    ship_time: time
    package_type_id: int
    comment: Optional[str] = Field(None)
    
    @field_validator('ship_time')
    def validate_ship_datetime(cls, v, info):
        ship_date = info.data.get('ship_date')
        ship_datetime = datetime.combine(ship_date, v)
        current_datetime = datetime.now()
        if ship_datetime < current_datetime:
            raise ValueError('Shipping date and time cannot be in the past.')
        return v

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
    city: Optional[str] = Field(None)
    ship_address: Optional[str] = Field(None)
    package_type_id: Optional[str] = Field(None)
    ship_date: Optional[date] = Field(None)
    ship_time: Optional[time] = Field(None)
    comment: Optional[str] = Field(None)
    
    @field_validator('ship_time')
    def validate_ship_datetime(cls, v, values):
        ship_date = values.get('ship_date')
        ship_datetime = datetime.combine(ship_date, v)
        current_datetime = datetime.now()
        if ship_datetime < current_datetime:
            raise ValueError('Shipping date and time cannot be in the past.')
        return v
    
    @field_validator('city', 'ship_address', pre=True, always=True)
    def validate_city_address(cls, v, values, field):
        city = values.get('city')
        ship_address = values.get('ship_address')

        if field.name == 'city' and v and not ship_address:
            raise ValueError('City can only be changed along with the address.')

        return v
