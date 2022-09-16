from ninja import Schema

from pydantic import EmailStr


class AccountInfoSchema(Schema):
    email: EmailStr
    password: str
    first_name: str
    phone: str
    address: str


class LoginSchema(Schema):
    email: EmailStr
    password: str


class AccountSignUpSchema(Schema):
    email: EmailStr
    password: str
    first_name: str
    phone: str
    address: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str
