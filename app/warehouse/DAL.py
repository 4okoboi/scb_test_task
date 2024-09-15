from sqlalchemy import func, select, update
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

    async def get_nearest_warehouse_in_city(
        self, 
        city: str,
        client_coords: tuple 
    ):
        query = select(
        Warehouse,
        func.sqrt(
            func.pow(Warehouse.geo_lat - client_coords[0], 2) + func.pow(Warehouse.geo_lon - client_coords[1], 2)
        ).label('distance')
    ).filter(Warehouse.city == city).order_by('distance').limit(1)
        res = await self.db_session.execute(query)
        nearest_warehouse = res.first()
        return nearest_warehouse
        
    async def get_warehouse_address_by_id(
        self,
        warehouse_id: int
    ) -> str:
        query = select(Warehouse.address).where(Warehouse.id_ == warehouse_id)
        res = await self.db_session.execute(query)
        warehouse_address = res.fetchone()
        if warehouse_address is not None:
            return warehouse_address[0]
        
    async def get_warehouse_by_id(
        self,
        warehouse_id: int
    ) -> Warehouse:
        query = select(Warehouse).where(Warehouse.id_ == warehouse_id)
        res = await self.db_session.execute(query)
        warehouse = res.fetchone()
        if warehouse is not None:
            return warehouse[0]