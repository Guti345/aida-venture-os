"""Script de bootstrap: crea el usuario GP inicial si no existe."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models.shared import User, UserRole
from app.services.auth import hash_password
import uuid

ADMIN_EMAIL = "admin@aidaventures.co"
ADMIN_PASSWORD = "AidaVC2025!"
ADMIN_NAME = "Admin AIDA"


def create_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing:
            print(f"[OK] Usuario admin ya existe: {ADMIN_EMAIL}")
            return
        admin = User(
            id=uuid.uuid4(),
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role=UserRole.gp,
            active=True,
        )
        db.add(admin)
        db.commit()
        print(f"[CREADO] Usuario GP: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
