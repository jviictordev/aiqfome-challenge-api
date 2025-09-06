from http import HTTPStatus
from datetime import timedelta
from sqlalchemy.orm import Session
from app.config.Config import Config
from app.models.Models import ClientModel
from app.config.Database import get_session
from app.schemas.AuthSchema import AuthSchema
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.config.Auth import create_access_token, verify_password

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", status_code=HTTPStatus.OK, response_model=AuthSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(ClientModel).filter(ClientModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": "user"},
        expires_delta=timedelta(minutes=Config().ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return AuthSchema(access_token=access_token, token_type="Bearer")
