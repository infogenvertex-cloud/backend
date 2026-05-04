from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_admin, create_token
from app.utils.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, data.email, data.password)
    token = create_token(admin.id, admin.email)
    return TokenResponse(access_token=token, name=admin.name, email=admin.email)
