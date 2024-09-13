from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import uuid
from enum import Enum

Base = declarative_base()


class Role(str, Enum):
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_CLIENT = "ROLE_CLIENT"

class User(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column("username", String, nullable=False)
    email = Column("email", String, nullable=False)
    actual_address = Column("actual_address", String, nullable=True)
    hashed_password = Column("hashed_password", String, nullable=False)
    role = Column("role", String, nullable=False)
    
    @property
    def is_admin(self) -> bool:
        return Role.ROLE_ADMIN in self.role

    # def __init__(self, username, hashed_password, roles, actual_address=None):
    #     self.username = username
    #     self.hashed_password = hashed_password
    #     self.roles = roles
    #     if 'client' in roles:
    #         self.actual_address = actual_address
