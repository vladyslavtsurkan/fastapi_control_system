from pydantic import ConfigDict
from fastapi_users import schemas

from schemas import CustomBaseModel


class UserRead(CustomBaseModel, schemas.BaseUser[int]):
    model_config = ConfigDict(
        **CustomBaseModel.model_config, from_attributes=True
    )

    id: int
    email: str
    first_name: str | None
    last_name: str | None
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(CustomBaseModel, schemas.CreateUpdateDictModel):
    email: str
    first_name: str | None
    last_name: str | None
    password: str
