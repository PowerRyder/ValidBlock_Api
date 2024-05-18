from typing import List
from fastapi import Depends, HTTPException
from src.business_layer.security.Jwt import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user = Depends(get_current_user)):
        if user['role'] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")