from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
