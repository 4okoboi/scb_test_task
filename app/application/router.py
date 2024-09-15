from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session

from app.application.DAL import ApplicationDAL
from app.warehouse.DAL import WarehouseDAL
from app.application import schemas

from app.auth.auth import get_current_user_from_token
from app.auth.models import User, Role

from app.utils.dadata.funcs import get_valid_address_and_coords
from app.utils.count_dictance import count_distance

application_router = APIRouter()

application_not_found_exception = HTTPException(
                status_code=404,
                detail="Не найдена заявка с таким номером"
            )

async def _create_application(
    body: schemas.CreateApplication,
    client_address: str,
    client_id: UUID,
    db_session: AsyncSession
) -> schemas.AfterApplicationCreated:
    async with db_session.begin():
        application_dal = ApplicationDAL(db_session=db_session)
        warehouse_dal = WarehouseDAL(db_session=db_session)
        ship_address, ship_lat, ship_lon = await get_valid_address_and_coords(address=body.ship_address + ", " + body.city)
        _, client_lat, client_lon = await get_valid_address_and_coords(address=client_address)
        nearest_warehouse = await warehouse_dal.get_nearest_warehouse_in_city(city=body.city, client_coords=(client_lat, client_lon))
        distance = await count_distance(
            point_a=(nearest_warehouse.Warehouse.geo_lat, nearest_warehouse.Warehouse.geo_lon),
            point_b=(ship_lat, ship_lon)
        )
        if nearest_warehouse is None:
            raise HTTPException(
                status_code=400,
                detail=f"Не найдены склады по вашему городу. Проверьте правильность написания (наш сервис действителен в городах Казань, Набережные Челны, Нижнекамск, Альметьевск, Зеленодольск)"
            )
        body.city = body.city.capitalize()
        if body.package_type_id == 3 and body.city != "Казань":
            raise HTTPException(
                status_code=400,
                details="Посылки типа 'Габаритный груз' доставляются только по Казани"
            )
        
        application = await application_dal.create_application(
            city=body.city,
            ship_address=ship_address,
            warehouse_id=nearest_warehouse.Warehouse.id_,
            client_id=client_id,
            distance=distance,
            ship_date=body.ship_date,
            ship_time=body.ship_time,
            package_type_id=body.package_type_id,
            comment=body.comment
        )
        
        return schemas.AfterApplicationCreated(
            application_id=application.id_
        )
        
async def _update_status(
    application_id: int,
    status: str,
    db_session: AsyncSession
) -> schemas.ShowApplicationStatus:
    async with db_session.begin():
        application_dal = ApplicationDAL(db_session)
        application_to_update = application_dal.get_application_by_id(
            application_id=application_id
        )
        if application_to_update is None:
            raise application_not_found_exception
        application_id = await application_dal.update_status(
            application_id=application_id,
            status=status
        )
        return schemas.ShowApplicationStatus(
            application_id=application_id,
            status=status
        )
    
async def _show_status(
    application_id: int,
    db_session: AsyncSession
) -> schemas.ShowApplicationStatus:
    async with db_session.begin():
        application_dal = ApplicationDAL(db_session)
        status = await application_dal.get_status(
            application_id=application_id
        )
        if status is None:
            raise application_not_found_exception
        return schemas.ShowApplicationStatus(
            application_id=application_id,
            status=status.status
        )
    
async def _show_application(
    application_id: int,
    db_session: AsyncSession
) -> schemas.ShowApplication:
    async with db_session.begin():
        application_dal = ApplicationDAL(db_session)
        application = await application_dal.get_application_by_id(
            application_id=application_id
        )
        if application is None:
            raise application_not_found_exception
        warehouse_dal = WarehouseDAL(db_session)
        warehouse_address = await warehouse_dal.get_warehouse_address_by_id(
            warehouse_id=application.warehouse_id
        )
        status = await application_dal.get_status(
            application_id=application_id
        )
        return schemas.ShowApplication(
            application_id=application.id_,
            city=application.city,
            ship_address=application.addresss,
            warehouse_address=warehouse_address,
            ship_date=application.ship_date,
            ship_time=application.ship_time,
            package_type_id=application.package_type_id,
            distance=application.distance,
            comment=application.comment,
            status=status.status
        )

@application_router.post("", response_model=schemas.AfterApplicationCreated)
async def create_application(
    body: schemas.CreateApplication,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token)
) -> schemas.AfterApplicationCreated:
    # try: 
    return await _create_application(
        body=body,
        client_address=current_user.actual_address,
        client_id=current_user.id,
        db_session=db_session
    )
    # except Exception as err:
    #     raise HTTPException(
    #         status_code=503,
    #         detail="Проблема на стороне сервера, попробуйте совершить запрос позже"
    #     )

@application_router.get("", response_model=schemas.ShowApplication)
async def show_application(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplication:
    return await _show_application(
        application_id=application_id,
        db_session=db_session
    )


@application_router.get("/status", response_model=schemas.ShowApplicationStatus)
async def show_application_status(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplicationStatus:
    return await _show_status(
        application_id=application_id,
        db_session=db_session
    )


@application_router.patch("", response_model=schemas.AfterApplicationCreated)
async def update_application(
    application_id: int,
    body: schemas.UpdateApplication,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.AfterApplicationCreated:
    pass

@application_router.patch("/status/mark_as_done", response_model=schemas.ShowApplicationStatus)
async def status_mark_as_done(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplicationStatus:
    return await _update_status(
        application_id=application_id,
        status="Done",
        db_session=db_session
    )


@application_router.patch("/status/mark_as_cancelled", response_model=schemas.ShowApplicationStatus)
async def status_mark_as_cancelled(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplicationStatus:
    return await _update_status(
        application_id=application_id,
        status="Cancelled",
        db_session=db_session
    )


@application_router.patch("/status/mark_as_handed_to_courier", response_model=schemas.ShowApplicationStatus)
async def status_mark_as_handed_to_courier(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplicationStatus:
    return await _update_status(
        application_id=application_id,
        status="Handed to courier",
        db_session=db_session
    )

@application_router.patch("/status/mark_as_in_progress", response_model=schemas.ShowApplicationStatus)
async def status_mark_as_in_progress(
    application_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowApplicationStatus:
    return await _update_status(
        application_id=application_id,
        status="In progress",
        db_session=db_session
    )
