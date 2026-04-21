import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shared import User
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead
from app.services.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    require_gp,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, db: Session = Depends(get_db)):
    """Crea el primer usuario GP (bootstrap). Si ya existen usuarios usa /auth/register/admin con token GP."""
    user_count = db.query(User).count()
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ya existen usuarios. Usa POST /auth/register/admin con token GP.",
        )
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ya registrado")
    user = User(
        id=uuid.uuid4(),
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/register/admin", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_by_gp(
    body: UserCreate,
    db: Session = Depends(get_db),
    caller: User = Depends(require_gp),
):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ya registrado")
    user = User(
        id=uuid.uuid4(),
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if user is None or not user.active or not verify_password(body.password, user.password_hash or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.email, "role": user.role.value})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _caller: User = Depends(require_gp),
):
    return db.query(User).order_by(User.created_at).all()


@router.put("/users/{user_id}/deactivate", response_model=UserRead)
def deactivate_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _caller: User = Depends(require_gp),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.active = False
    db.commit()
    db.refresh(user)
    return user
