from fastapi import APIRouter, Depends, HTTPException
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.warehouse import schemas
from app.warehouse.DAL import WarehouseDAL

from app.utils.dadata.funcs import get_valid_address_and_coords

warehouse_router = APIRouter()

async def _add_warehouse(
    body: schemas.AddWarehouse,
    db_session: AsyncSession
) -> schemas.ShowWarehouse:
    async with db_session.begin():
        # TODO: сделать так, чтобы при добавлении склада в новом городе, этот город автоматически добавлялся в список разрешенных городов
        warehouse_dal = WarehouseDAL(db_session)
        address, geo_lat, geo_lon = await get_valid_address_and_coords(address=body.address + "," + body.city)
        warehouse = await warehouse_dal.add_warehouse(
            city=body.city,
            address=address,
            geo_lat=geo_lat,
            geo_lon=geo_lon
        )
        return schemas.ShowWarehouse(
            id_=warehouse.id_,
            city=warehouse.city,
            address=warehouse.address
        )


@warehouse_router.post("", response_model=schemas.ShowWarehouse)
async def add_warehouse(
    body: schemas.AddWarehouse,
    db_session: AsyncSession = Depends(get_async_session)
) -> schemas.ShowWarehouse:
    await _add_warehouse(
        body=body,
        db_session=db_session
    )
    
        
