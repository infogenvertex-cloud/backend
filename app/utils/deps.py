from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import SessionLocal
from app.models.admin import Admin
from app.services.auth_service import decode_token

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
) -> Admin:
    payload = decode_token(credentials.credentials)
    admin = db.query(Admin).filter(Admin.id == int(payload["sub"])).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin
