from pydantic import BaseModel, EmailStr


class Userschema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class Loginschema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True