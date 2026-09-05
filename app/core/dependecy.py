from fastapi import status as http_status, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.message import ErrorMessage
from app.core.jwt import verify_token
from app.repository.role_repository import RoleRepository


def validate_token(request: Request):
    headers = request.headers
    bearer_token = headers.get("authorization")

    if bearer_token is None or len(bearer_token.split(" ")) < 2:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.INVALID_TOKEN,
        )

    token = bearer_token.split(" ")[1]
    return verify_token(token)


def current_user(request: Request, db: Session = Depends(get_db)):
    return validate_token(request)


class RoleCheck:
    def __init__(self, roles: list[str], db: Session = Depends(get_db)):
        self.allowed_roles = roles
        self.db = db

    def __call__(self, request: Request):
        payload = validate_token(request)
        role_id = payload.get("role_id", None)

        if not role_id:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.UNAUTHORIZED_ACCESS,
            )

        role_repo = RoleRepository(self.db)
        role_detail = role_repo.get(role_id)
        if not role_detail:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.UNAUTHORIZED_ACCESS,
            )

        role_name = role_detail.role_name.strip()
        if role_name not in self.allowed_roles:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.UNAUTHORIZED_ACCESS,
            )

        return payload
