from fastapi import APIRouter, status, Depends
from fastapi_cache.decorator import cache

from auth.dependencies import CurrentActiveUserDepends
from auth.base_config import current_superuser
from controller.dependencies import ControllerServiceDepends
from controller.schemas import (
    ControllerCreateUpdate,
    ControllerRead,
    ControllerUpdatePartial,
    ControllerSetDataValue
)

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_superuser)]
)
@cache(expire=60)
async def get_all_controllers(
        service: ControllerServiceDepends,
) -> list[ControllerRead]:
    controllers = await service.get_all_controllers()

    return controllers


@router.get("/me", status_code=status.HTTP_200_OK)
@cache(expire=60)
async def get_my_controllers(
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends
) -> list[ControllerRead]:
    controllers = await service.get_user_controllers(user.id)

    return controllers


@router.get("/{controller_id}", status_code=status.HTTP_200_OK)
@cache(expire=30)
async def get_controller_by_id(
        controller_id: int,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
) -> ControllerRead:
    controller = await service.get_controller_by_id(user.id, controller_id)
    return controller


@router.get("/{controller_id}/data", status_code=status.HTTP_200_OK)
async def read_controller_data(
        controller_id: int,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    data = await service.read_controller_data(
        user.id, controller_id
    )
    return {"data": data}


@router.post("/{controller_id}/data", status_code=status.HTTP_200_OK)
async def write_controller_data(
        controller_id: int,
        data: ControllerSetDataValue,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    data = await service.write_controller_data(
        user.id, controller_id, data.data_value
    )
    return {"data": data}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_controller(
        controller_schema: ControllerCreateUpdate,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
) -> ControllerRead:
    controller_dict = controller_schema.model_dump()
    controller = await service.create_controller(user.id, controller_dict)

    return controller


@router.put("/{controller_id}", status_code=status.HTTP_200_OK)
async def update_controller(
        controller_id: int,
        controller_schema: ControllerCreateUpdate,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
) -> ControllerRead:
    controller_dict = controller_schema.model_dump()
    controller = await service.update_controller(
        user.id, controller_id, controller_dict
    )
    return controller


@router.patch("/{controller_id}", status_code=status.HTTP_200_OK)
async def update_controller_partial(
        controller_id: int,
        controller_schema: ControllerUpdatePartial,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
) -> ControllerRead:
    controller_dict = controller_schema.model_dump(exclude_unset=True)
    controller = await service.update_controller(
        user.id, controller_id, controller_dict
    )
    return controller


@router.delete("/{controller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_controller(
        controller_id: int,
        service: ControllerServiceDepends,
        user: CurrentActiveUserDepends,
):
    await service.delete_controller(user.id, controller_id)
