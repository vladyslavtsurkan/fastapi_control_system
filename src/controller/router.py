from fastapi import APIRouter, status

from auth.dependencies import CurrentActiveUserDepends
from controller.dependencies import ControllerServiceDepends
from controller.schemas import (
    ControllerCreateUpdate,
    ControllerRead,
    ControllerUpdatePartial,
)

router = APIRouter()


@router.get("/", response_model=list[ControllerRead], status_code=status.HTTP_200_OK)
async def get_all_controllers(service: ControllerServiceDepends):
    controllers = await service.get_all_controllers()

    return controllers


@router.get("/{controller_id}", response_model=ControllerRead, status_code=status.HTTP_200_OK)
async def get_controller_by_id(controller_id: int, service: ControllerServiceDepends):
    controller = await service.get_controller_by_id(controller_id)
    return controller


@router.get("/{controller_id}/data", status_code=status.HTTP_200_OK)
async def read_controller_data(
        controller_id: int, service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
        address: int = 0,
        length: int = 1
):
    data = await service.read_controller_data(user.id, controller_id, address, length)
    return {"data": data}


@router.post(
    "/{controller_id}/data",
    status_code=status.HTTP_200_OK,
)
async def write_controller_data(
        controller_id: int, service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
        address: int = 0,
        data: int = 0
):
    data = await service.write_controller_data(user.id, controller_id, address, data)
    return {"data": data}


@router.post("/", response_model=ControllerRead, status_code=status.HTTP_201_CREATED)
async def create_controller(
        controller: ControllerCreateUpdate,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    controller = await service.create_controller(user.id, controller)

    return controller


@router.put("/{controller_id}", response_model=ControllerRead, status_code=status.HTTP_200_OK)
async def update_controller(
        controller_id: int,
        controller: ControllerCreateUpdate,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    controller = await service.update_controller(user.id, controller_id, controller)
    return controller


@router.patch("/{controller_id}", response_model=ControllerRead, status_code=status.HTTP_200_OK)
async def update_controller_partial(
        controller_id: int,
        controller: ControllerUpdatePartial,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    controller = await service.update_controller(user.id, controller_id, controller)
    return controller


@router.delete("/{controller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_controller(
        controller_id: int,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    await service.delete_controller(user.id, controller_id)
