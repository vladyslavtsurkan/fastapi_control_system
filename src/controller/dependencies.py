from typing import Annotated

from fastapi import Depends

from controller.service import ControllerService


ControllerServiceDepends = Annotated[
    ControllerService, Depends(ControllerService)
]
