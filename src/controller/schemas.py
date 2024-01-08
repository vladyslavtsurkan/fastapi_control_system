from datetime import datetime

from pydantic import BaseModel, Field, IPvAnyAddress


class ControllerCreateUpdate(BaseModel):
    name: str = Field(..., example="Controller 1")
    description: str | None = Field(..., example="Description 1")
    ip_address: IPvAnyAddress = Field(..., example="127.0.0.1")
    port: int = Field(..., example=502)
    is_active: bool = Field(..., example=True)


class ControllerUpdatePartial(BaseModel):
    name: str = None
    description: str | None = None
    ip_address: IPvAnyAddress = None
    port: int = None
    is_active: bool = None


class ControllerRead(ControllerCreateUpdate):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2021-06-01 00:00:00")
    updated_at: datetime = Field(..., example="2021-06-01 00:00:00")
