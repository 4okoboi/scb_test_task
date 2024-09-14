from fastapi import APIRouter, Depends, HTTPException

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import get_current_user_from_token
from app.auth import service_funcs
from app.auth.models import User, Role
from app.database import get_async_session

from app.auth import schemas

user_router = APIRouter()

@user_router.post("/admin", response_model=schemas.ShowAdmin)
async def create_admin(
    body: schemas.CreateAdmin,
    db: AsyncSession = Depends(get_async_session)
) -> schemas.ShowAdmin:
    try:
        return await service_funcs._create_admin(body=body, session=db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )
        
@user_router.post("/client", response_model=schemas.ShowClient)
async def add_client(
    body: schemas.AddClient,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token)
) -> schemas.ShowClient:
    if current_user.role != Role.ROLE_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    try:
        return await service_funcs._add_client(body=body, session=db)
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail=f"Database error, {err}"
        )
    
    
@user_router.delete("", response_model=schemas.DeleteUser)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token)
) -> schemas.DeleteUser:
    user_for_deletion = await service_funcs._get_user_by_id(user_id=user_id, session=db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    if not service_funcs._check_user_permissions(
        target_user=user_id,
        current_user=current_user
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    deleted_user_id = await service_funcs._delete_user(user_id, session=db)
    return schemas.DeleteUser(user_id=deleted_user_id)

@user_router.get("/client", response_model=schemas.ShowClient)
async def get_client_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token)
) -> schemas.ShowClient:
    if current_user.role != Role.ROLE_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )
    user = await service_funcs._get_user_by_id(user_id, session=db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    return schemas.ShowClient(
        user_id=user.id,
        username=user.username,
        email=user.email,
        actual_address=user.actual_address
    )


@user_router.patch("/client", response_model=schemas.UpdateClientResponse)
async def update_client(
    user_id: UUID,
    body: schemas.UpdateClientRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token)
) -> schemas.UpdateClientResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided"
        )
    user_for_update = await service_funcs._get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if service_funcs._check_user_permissions(current_user=current_user, target_user=user_for_update):
        try:
            updated_user_id = await service_funcs._update_client(
                updated_user_params=updated_user_params, session=db, user_id=user_id
            )
        except Exception as err:
            raise HTTPException(status_code=503, detail=f"Database error: {err}")
        return schemas.UpdateClientResponse(user_id=updated_user_id)
    else:
        raise HTTPException(
            status_code=403,
            detail="Forbidden."
        )