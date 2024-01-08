from typing import Annotated

from fastapi import Depends

from auth.manager import get_user_manager, UserManager
from auth.base_config import current_user, current_active_user, current_superuser
from auth.models import User

UserManagerDepends = Annotated[UserManager, Depends(get_user_manager)]

CurrentUserDepends = Annotated[User, Depends(current_user)]
CurrentActiveUserDepends = Annotated[User, Depends(current_active_user)]
CurrentSuperUserDepends = Annotated[User, Depends(current_superuser)]
