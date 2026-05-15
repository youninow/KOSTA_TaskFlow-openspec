import re
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..auth_utils import hash_password, verify_password, create_token, err, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupIn(BaseModel):
    email: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


def user_out(user: models.User, token: str = None):
    data = {"id": user.id, "email": user.email, "team_id": user.team_id}
    if token:
        return {"token": token, "user": data}
    return {"user": data}


@router.post("/signup", status_code=201)
def signup(body: SignupIn, db: Session = Depends(get_db)):
    if not EMAIL_RE.match(body.email):
        err("VALIDATION_ERROR", "올바른 형식이 아닙니다")
    if len(body.password) < 8:
        err("VALIDATION_ERROR", "비밀번호는 8자 이상이어야 합니다")
    if db.query(models.User).filter(models.User.email == body.email).first():
        err("EMAIL_TAKEN", "이미 가입된 이메일입니다", 409)
    user = models.User(email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_out(user, create_token(user.id))


@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        err("INVALID_CREDENTIALS", "이메일 또는 비밀번호가 일치하지 않습니다", 401)
    return user_out(user, create_token(user.id))


@router.post("/logout")
def logout():
    return {}


@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "team_id": current_user.team_id}
