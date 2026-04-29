from fastapi import Depends,HTTPException
from main import Oauth2_schema
from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from main import becrypt_context
from main import SECRET_KEY, EXPRIRE_MINUTE_TOKEN, ALGORITHM
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def user_verify(email,session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return True
    return False

def user_authenticate(email,password,session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    if becrypt_context.verify(password,user.password):
        return user
    return False

def creat_token(id, token_time=timedelta(minutes=int(EXPRIRE_MINUTE_TOKEN))):
    expiretion_date = token_time + datetime.now(timezone.utc)
    dict_info = {'sub': str(id), 'exp':expiretion_date.timestamp()}
    encode_jwt = jwt.encode(dict_info, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token:str=Depends(Oauth2_schema),session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dict_info["sub"])
    except JWTError as e:
        print(e)
        return HTTPException(status_code=400,detail="Error")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return HTTPException(status_code=400,detail="Access Denied")
    return user





