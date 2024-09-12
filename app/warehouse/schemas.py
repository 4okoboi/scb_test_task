from pydantic import BaseModel

class AddWarehouse(BaseModel):
    city: str
    address: str
    
    
class ShowWarehouse(BaseModel):
    id_: int
    city: str
    address: str
    