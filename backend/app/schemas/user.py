from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    institution_id: int | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    institution_id: int | None = None

    class Config:
        from_attribute = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
