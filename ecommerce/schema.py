from ninja import Schema
from pydantic import EmailStr, Field, UUID4


class ProductSchema(Schema):
    id: UUID4
    name: str
    description: str
    price: float
    image: str
    category: str
    quantity: int
    is_active: bool


class CategorySchema(Schema):
    id: UUID4
    name: str
    image: str
    is_active: bool


class OrderSchema(Schema):
    id: UUID4
    user: str
    status: str
    items: str
    created: str
    updated: str


class ItemSchema(Schema):
    id: UUID4
    user: str
    product: str
    item_qty: int
    ordered: bool


class OrderStatusSchema(Schema):
    status: str
    description: str


class CategoryUpdateSchema(CategorySchema):
    pass


class UserLoginSchema(Schema):
    username: str
    password: str


class UserChangePasswordSchema(Schema):
    old_password: str
    new_password: str


class UserProfileSchema(Schema):
    user: str
    first_name: str
    last_name: str
    phone_number: str
    address: str


class ArticleSchema(Schema):
    id: UUID4
    title: str
    body: str
    image: str


class AmagesSchema(Schema):
    id: UUID4
    image: str
    alt_text: str = None
    is_default_image: bool
