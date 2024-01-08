from datetime import datetime

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

from controller.models import Controller
from controller.schemas import ControllerCreateUpdate
from database import get_async_session


class ControllerService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_controller_by_id(self, controller_id: int):
        stmt = select(Controller).where(Controller.id == controller_id)
        result = await self.session.execute(stmt)
        controller = result.scalars().first()

        if controller is not None:
            controller = controller.to_dict()

        return controller

    async def read_controller_data(self, controller_id: int):
        controller = await self.get_controller_by_id(controller_id)

        if controller is None:
            return None

        client = AsyncModbusTcpClient(
            host=controller["ip_address"],
            port=controller["port"]
        )
        try:
            await client.connect()
            result = await client.read_holding_registers(0, 1)
        except ConnectionException:
            return None
        finally:
            client.close()
        return result.registers

    async def get_all_controllers(self):
        stmt = select(Controller)
        result = await self.session.execute(stmt)
        controllers = result.scalars().all()

        controllers = [controller.to_dict() for controller in controllers]

        return controllers

    async def create_controller(self, controller: ControllerCreateUpdate):
        controller = Controller(**controller.model_dump())
        controller.created_at = controller.updated_at = datetime.now()
        self.session.add(controller)

        await self.session.commit()
        await self.session.refresh(controller)

        return controller.to_dict()

    async def update_controller(self, controller_id: int, controller_schema: ControllerCreateUpdate):
        stmt = select(Controller).where(Controller.id == controller_id)
        result = await self.session.execute(stmt)
        controller = result.scalars().first()

        if controller is None:
            return None

        stmt = update(Controller).where(Controller.id == controller_id).values(
            **controller_schema.model_dump()
        )
        await self.session.execute(stmt)

        controller.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(controller)

        return controller.to_dict()

    async def delete_controller(self, controller_id: int) -> bool | None:
        stmt = select(Controller).where(Controller.id == controller_id)
        result = await self.session.execute(stmt)
        controller = result.scalars().first()

        if controller is None:
            return None

        await self.session.delete(controller)
        await self.session.commit()

        return True
