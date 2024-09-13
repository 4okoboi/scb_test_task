from app.auth.models import User as UserModel, Role
from app.database import DAL
from typing import Union
from uuid import UUID
from sqlalchemy import delete, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

class UserDAL(DAL):
    async def create_user(
        self,
        email: str,
        username: str,
        hashed_password: str,
        role: Role,
        actual_address: str=None
    ) -> UserModel:
        # если идет добавление клиента, также должен добавляться и фактический адрес 
        if role == Role.ROLE_CLIENT:
            new_user = UserModel(
                username=username,
                email=email,
                hashed_password=hashed_password,
                role=role,
                actual_address=actual_address
            )
        else:
            new_user = UserModel(
                username=username,
                email=email,
                hashed_password=hashed_password,
                role=role
            )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    
    async def delete_user(
        self,
        user_id: UUID
    ) -> Union[UUID, None]:
        query = (
            delete(UserModel)
            .where(and_(UserModel.id == user_id, UserModel.role == Role.ROLE_CLIENT))
            .returning(UserModel.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]
        
    async def get_user_by_id(
        self,
        user_id: UUID
    ) -> Union[UserModel, None]:
        query = (
            select(UserModel)
            .where(UserModel.id == user_id)
        )
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
    
    async def get_user_by_email(
        self,
        email: str
    ) -> Union[UserModel, None]:
        query = (
            select(UserModel)
            .where(UserModel.email == email)
        )
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]