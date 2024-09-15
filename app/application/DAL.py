from typing import Union
from app.database import DAL
from uuid import UUID
from datetime import date, datetime, time
from app.application.models import Application, ApplicationStatusCurrent
from sqlalchemy import select, update, delete


class ApplicationDAL(DAL):
    async def create_application(
        self,
        city: str,
        ship_address: str,
        warehouse_id: int,
        client_id: UUID,
        distance: int,
        ship_date: date,
        ship_time: time,
        package_type_id: int,
        comment: str = None,
    ) -> Application:
        new_application = Application(
            city=city,
            ship_address=ship_address,
            warehouse_id=warehouse_id,
            client_id=client_id,
            distance=distance,
            ship_date=ship_date,
            ship_time=ship_time,
            package_type_id=package_type_id,
            comment=comment
        )
        self.db_session.add(new_application)
        application_status = ApplicationStatusCurrent(
            application_id=new_application.id_,
            status="New"
        )
        self.db_session.add(application_status)
        await self.db_session.flush()
        return new_application

    async def get_application_by_id(
        self,
        application_id: int
    ) -> Application:
        query = select(Application).where(Application.id_ == application_id)
        res = await self.db_session.execute(query)
        application = res.fetchone()
        if application is not None:
            return application[0]
    
    async def update_application(
        self,
        application_id: int,
        **kwargs
    ) -> Union[int, None]:
        query = update(Application).where(Application.id_ == application_id).returning(Application.id_)
        res = await self.db_session.execute(query)
        updated_application_id = res.fetchone()
        if updated_application_id is not None:
            return updated_application_id[0]
    
    async def get_application_by_id(
        self,
        application_id: int
    ) -> Union[Application, None]:
        query = select(Application).where(Application.id_ == application_id)
        res = await self.db_session.execute(query)
        application = res.fetchone()
        if application is not None:
            return application[0]
        
    async def update_status(
        self,
        application_id: int,
        status: str
    ) -> Union[int, None]:
        query = (update(ApplicationStatusCurrent)
                 .where(ApplicationStatusCurrent.application_id)
                 .values(status=status)
                 .returning(ApplicationStatusCurrent.application_id))
        res = await self.db_session.execute(query)
        application_id = res.fetchone()
        if application_id is not None:
            return application_id[0]
        