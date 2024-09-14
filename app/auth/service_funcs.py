from typing import Union
from uuid import UUID

from fastapi import HTTPException

from app.auth import schemas
from app.auth.DAL import UserDAL
from app.auth.models import Role, User as UserModel
from app.utils.auth.hashing import Hasher
from app.utils.dadata.funcs import get_valid_address_and_coords

async def _create_admin(
    body: schemas.CreateAdmin,
    session
) -> schemas.ShowAdmin:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            username=body.username,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            role=Role.ROLE_ADMIN
        )
        return schemas.ShowAdmin(
            username=user.username,
            email=user.email,
            user_id=user.id
        )
    
async def _get_user_by_id(
    user_id: UUID,
    session
) -> Union[UserModel, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None:
            return user
        
async def _add_client(
    body: schemas.AddClient,
    session
) -> schemas.ShowClient:
    async with session.begin():
        user_dal = UserDAL(session)
        address, _, _ = await get_valid_address_and_coords(address=body.actual_address)
        client = await user_dal.create_user(
            username=body.username,
            email=body.email,
            actual_address=address,
            hashed_password=Hasher.get_password_hash(body.password),
            role=Role.ROLE_CLIENT
        )
        return schemas.ShowClient(
            user_id=client.id,
            username=client.username,
            email=client.email,
            actual_address=client.actual_address
        )

async def _delete_user(
    user_id: UUID,
    session
) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id
        )
        return deleted_user_id

async def _update_client(
    user_id: UUID,
    updated_client_params: dict,
    session
) -> Union[UUID, None]:
    async with session.begin():
        if "actual_address" in updated_client_params.keys():
            updated_client_params["actual_address"], _, _ = await get_valid_address_and_coords(address=updated_client_params.get("actual_address"))
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(user_id=user_id, **updated_client_params)
        return updated_user_id
        

def _check_user_permissions(
    target_user: UserModel,
    current_user: UserModel
) -> bool:
    if current_user.role == Role.ROLE_ADMIN and target_user.role == Role.ROLE_ADMIN:
        return False
    if current_user.role == Role.ROLE_CLIENT:
        return False
    return True


            