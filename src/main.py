from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as async_redis

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from controller.router import router as controllers_router
from config import AppSettings

settings = AppSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = async_redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await FastAPICache.clear()
    FastAPICache.reset()


def create_api_router():
    router = APIRouter(prefix="/api/v1")

    router.include_router(
        fastapi_users.get_auth_router(
            auth_backend,
            requires_verification=True
        ),
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

    router.include_router(
        fastapi_users.get_users_router(UserRead, UserCreate),
        prefix="/users",
        tags=["users"],
    )

    router.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )

    router.include_router(
        controllers_router, prefix="/controllers", tags=["controllers"]
    )

    return router


def create_app():
    app = FastAPI(
        title="Control system API",
        description="API for controlling the object",
        version="0.1.0",
        lifespan=lifespan
    )

    app.include_router(create_api_router())

    return app
