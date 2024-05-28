from datetime import datetime

from pydantic import Field, IPvAnyAddress

from schemas import CustomBaseModel


class ControllerCreateUpdate(CustomBaseModel):
    name: str = Field(..., example="Controller 1")
    description: str | None = Field(..., example="Description 1")
    ip_address: IPvAnyAddress = Field(..., example="127.0.0.1")
    port: int = Field(..., example=502)
    read_address: int = Field(..., example=0)
    write_address: int = Field(..., example=1)
    is_active: bool = Field(..., example=True)


class ControllerUpdatePartial(CustomBaseModel):
    name: str = None
    description: str | None = None
    ip_address: IPvAnyAddress = None
    port: int = None
    read_address: int = None
    write_address: int = None
    is_active: bool = None


class ControllerRead(ControllerCreateUpdate):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2021-06-01 00:00:00")
    updated_at: datetime = Field(..., example="2021-06-01 00:00:00")


class ControllerSetDataValue(CustomBaseModel):
    data_value: int = Field(..., example=1, ge=0, le=65535)
