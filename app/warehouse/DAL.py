from sqlalchemy import select, update
from app.warehouse.models import Warehouse
from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DAL

class WarehouseDAL(DAL):
    async def add_warehouse(
        self,
        city: str,
        address: str,
        geo_lat: float,
        geo_lon: float
    ) -> Warehouse:
        new_warehouse = Warehouse(
            city=city,
            address=address,
            geo_lat=geo_lat,
            geo_lon=geo_lon
        )
        self.db_session.add(new_warehouse)
        await self.db_session.flush()
        return new_warehouse

    async def get_warehouses(
        self
    ) -> List[Warehouse]:
        query = select(Warehouse)
        res = await self.db_session.execute(query)
        warehouses = res.fetchall()
        return [warehouse[0] for warehouse in warehouses]
