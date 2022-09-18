from ninja import Schema
from pydantic import EmailStr, Field

class AccountCreate(Schema):
    email: EmailStr = None
    password: str = None
    first_name: str = None
    phone_number: str = None
    address: str = None

class AccountInfoSchema(Schema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number : int
    address: str


class LoginSchema(Schema):
    email: EmailStr
    password: str


class AccountSignUpSchema(Schema):
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    first_name: str
    last_name: str
    phone_number: int = None


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str

class MessageOut(Schema):
    message: str