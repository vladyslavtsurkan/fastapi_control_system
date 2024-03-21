from fastapi import HTTPException


class PermissionForControllerDenied(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Permission for controller denied by current user"
        )


class ControllerNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Controller not found")
