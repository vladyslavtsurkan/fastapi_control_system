from datetime import datetime
from typing import Any

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from controller.models import Controller
from controller.exceptions import (
    PermissionForControllerDenied,
    ControllerNotFound,
)
from database import get_async_session


class ControllerService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def _get_controller_instance_model_by_id(
        self, user_id: int, controller_id: int
    ) -> Controller:
        stmt = select(Controller).where(Controller.id == controller_id)
        result = await self.session.execute(stmt)
        controller = result.scalars().first()

        if controller is None:
            raise ControllerNotFound

        if controller.user_id != user_id:
            raise PermissionForControllerDenied

        return controller

    async def get_controller_by_id(
        self, user_id: int, controller_id: int
    ) -> dict[str, Any]:
        controller = await self._get_controller_instance_model_by_id(
            user_id, controller_id
        )
        return controller.to_dict()

    async def get_user_controllers(self, user_id: int) -> list[dict[str, Any]]:
        stmt = select(Controller).where(Controller.user_id == user_id)
        result = await self.session.execute(stmt)
        controllers = result.scalars().all()

        controllers = [controller.to_dict() for controller in controllers]

        return controllers

    async def read_controller_data(
            self,
            user_id: int,
            controller_id: int,
    ) -> list[int] | None:
        controller = await self._get_controller_instance_model_by_id(
            user_id, controller_id
        )

        client = AsyncModbusTcpClient(
            host=str(controller.ip_address),
            port=controller.port
        )
        try:
            await client.connect()
            result = await client.read_holding_registers(
                controller.read_address, 1
            )
        except ModbusException:
            return None
        finally:
            client.close()
        return result.registers

    async def write_controller_data(
            self,
            user_id: int,
            controller_id: int,
            data: int
    ) -> list[int] | None:
        controller = await self._get_controller_instance_model_by_id(
            user_id, controller_id
        )
        controller_dict = controller.to_dict()

        client = AsyncModbusTcpClient(
            host=str(controller_dict["ip_address"]),
            port=controller_dict["port"]
        )
        try:
            await client.connect()
            result = await client.write_register(controller_dict[
                "write_address"], data
            )
        except ModbusException:
            return None
        finally:
            client.close()
        return result.registers

    async def get_all_controllers(self) -> list[dict[str, Any]]:
        stmt = select(Controller)
        result = await self.session.execute(stmt)
        controllers = result.scalars().all()

        controllers = [controller.to_dict() for controller in controllers]

        return controllers

    async def create_controller(
        self, user_id: int, controller_dict: dict[str, Any]
    ) -> dict[str, Any]:
        controller = Controller(**controller_dict)
        controller.created_at = controller.updated_at = datetime.now()
        controller.user_id = user_id
        self.session.add(controller)

        await self.session.commit()
        await self.session.refresh(controller)

        return controller.to_dict()

    async def update_controller(
            self,
            user_id: int,
            controller_id: int,
            controller_dict: dict[str, Any]
    ) -> dict[str, Any] | None:
        controller = await self._get_controller_instance_model_by_id(
            user_id, controller_id
        )

        stmt = update(Controller).where(Controller.id == controller_id).values(
            **controller_dict
        )
        await self.session.execute(stmt)

        controller.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(controller)

        return controller.to_dict()

    async def delete_controller(
        self, user_id: int, controller_id: int
    ) -> None:
        controller = await self._get_controller_instance_model_by_id(
            user_id, controller_id
        )

        await self.session.delete(controller)
        await self.session.commit()
