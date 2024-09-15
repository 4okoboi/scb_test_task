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