from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from main import becrypt_context
from dependencies import  get_session, user_verify, user_authenticate, creat_token, verify_token
from schema import Userschema, Loginschema
from models import User
from datetime import datetime, timedelta

auth_router = APIRouter(tags=["auth"], prefix="/auth")

@auth_router.post("/create_account")
async def create_account(user_schema:Userschema,session:Session = Depends(get_session)):
    if not user_verify(user_schema.email,session):
        return HTTPException(status_code=400,detail="Email already registered")
    password= becrypt_context.encrypt(user_schema.password)
    new_user = User(name=user_schema.name.title(), email=user_schema.email, password=password,created_at=datetime.now())
    session.add(new_user)
    session.flush()
    user = session.query(User).filter(User.id == 1).first()
    if user:
        user.admin = True
    session.commit()
    return {
        'message':'Account created successfully',
        'user':user_schema.name,
        'email':user_schema.email,
    }

@auth_router.post("/login")
async def login(login_schema:Loginschema, session: Session = Depends(get_session)):
    user = user_authenticate(Loginschema.email, Loginschema.password,session)
    if not user:
        return HTTPException(status_code=400,detail="Incorrect email or password")

    acess_token = creat_token(user.id)
    refresh_token = creat_token(user.id,token_time=timedelta(days=7))
    return {
        "acess_token":acess_token,
        "refresh_token":refresh_token,
        "token_type": "bearer",
    }

@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(get_session)):
    user = user_authenticate(form_data.username, form_data.password, session)
    if not user:
        return HTTPException(status_code=400,detail="Incorrect username or password")
    access_token = creat_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.get("/refresh")
async def refresh(user:User=Depends(verify_token)):
    access_token = creat_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
