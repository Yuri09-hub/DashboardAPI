import os

from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPRIRE_MINUTE_TOKEN = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE")

app = FastAPI()

becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
from auth_route import auth_router
app.include_router(auth_router)