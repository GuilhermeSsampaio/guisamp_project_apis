from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
import bcrypt

class UserDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    email: EmailStr = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    
class UserLogin(BaseModel):
    email:str
    password:str
    
class UserIn(BaseModel):
    username: str
    email: EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr
    created_at: datetime
    
def hash_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password

def verify_password(password, hashed_password):
   password = password.encode("utf-8")
   if isinstance(hashed_password, str):
       hashed_password = hashed_password.encode("utf-8")
   return bcrypt.checkpw(password, hashed_password)
