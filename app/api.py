from fastapi import APIRouter
from pydantic import BaseModel
from app.checker import check_password

router = APIRouter()


class PasswordRequest(BaseModel):
    password: str


@router.post("/password/check")
def check(req: PasswordRequest):
    return check_password(req.password)