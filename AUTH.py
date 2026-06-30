from DATABASE import engine,User
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import HTTPException, Depends

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_account(name,password):
    with Session(engine) as session:
        if len(name) <= 4:
            raise ValueError("NAME MUST BE ABOVE 4 CHARACTERS")
        name_validation = session.query(User).filter(User.Username == name).first()
        if name_validation is not None:
            raise ValueError("NAME ALREADY TAKEN")
        if len(password) <= 8:
            raise ValueError("PASSWORD LENGTH MUST BE ABOVE 8 CHARACTERS")
        hash = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        hashed_pw = hash.decode("utf-8")
        new_user = User(
            Username = name,
            Password = hashed_pw
        )
        session.add(new_user)
        session.commit()
        session.close()
        return {"MESSAGE":"ACCOUNT CREATED"}

def login(name,password):
    with Session(engine) as session:
        user_search = session.query(User).filter(User.Username == name).first()
        if user_search is None:
            raise ValueError("USER NOT FOUND")
        stored_hash = user_search.Password.encode("utf-8")
        password = password.encode("utf-8")
        if not bcrypt.checkpw(password,stored_hash):
            raise ValueError("INCORRECT PASSWORD")
        payload = {
                "sub": str(user_search.UserID),
                "exp":datetime.now(timezone.utc) + timedelta(minutes=30)
            }
        token = jwt.encode(payload,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALGORITHM"))
        return {"TOKEN":token}
        
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")]
    )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="USER NOT FOUND"
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="INVALID TOKEN"
        )
    with Session(engine) as session:
        user = session.query(User).filter(User.UserID == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="USER NOT FOUND"
            )
        return user