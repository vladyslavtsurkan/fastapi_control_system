from fastapi import FastAPI, APIRouter

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from controller.router import router as controllers_router

app = FastAPI(
    title="Control system API",
    description="API for controlling the object",
    version="0.1.0",
)

router = APIRouter(prefix="/api/v1")

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(controllers_router, prefix="/controllers", tags=["controllers"])

app.include_router(router)
