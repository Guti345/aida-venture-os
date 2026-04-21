import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shared import User, UserRole

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = 480) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    email: str | None = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin subject")
    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    return user


def require_gp(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.gp:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol GP")
    return user


def require_analyst(user: User = Depends(get_current_user)) -> User:
    if user.role not in (UserRole.gp, UserRole.analyst):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol analyst o superior")
    return user


def require_studio_operator(user: User = Depends(get_current_user)) -> User:
    if user.role not in (UserRole.gp, UserRole.studio_operator):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol studio_operator o superior")
    return user
