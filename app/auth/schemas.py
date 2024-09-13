from pydantic import BaseModel, EmailStr, constr, validator, Field
from fastapi import HTTPException
from uuid import UUID
from typing import Optional


class CreateAdmin(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    # write password validator
    
class AddClient(BaseModel):
    username: str
    email: EmailStr
    password: str
    actual_address: str
    
    
class UpdateClientRequest(BaseModel):
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    actual_address: Optional[str] = Field(None)

class UpdateClientResponse(BaseModel):
    user_id: UUID

class ShowClient(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    actual_address: str
    
class ShowAdmin(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    

class CheckToken(BaseModel):
    access_token: str
    token_type: str
    
class DeleteUser(BaseModel):
    user_id: UUID
    