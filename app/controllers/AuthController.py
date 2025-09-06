from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.config.Auth import create_access_token, verify_password, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.config.Database import get_session
from app.models.Models import ClientModel
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(ClientModel).filter(ClientModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": "user"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
