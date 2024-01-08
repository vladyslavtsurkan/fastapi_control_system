from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from controller.service import ControllerService


ControllerServiceDepends = Annotated[ControllerService, Depends(ControllerService)]
