from http import HTTPStatus
from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from acountinfo import *
from acountinfo.models import EmailAccount

from acountinfo.schema import AccountSignUpSchema, MessageOut, LoginSchema , AccountCreate
from petappbackend.utils import create_token , response

User = get_user_model()

account_controller = Router()


@account_controller.post('/signup',
                         response={200: AccountCreate, 403: MessageOut, 500: MessageOut, 201: AccountSignUpSchema})
def signup(request, account_in: AccountSignUpSchema):
    if account_in.password1 != account_in.password2:
        return MessageOut(message='Passwords do not match')
    try:
        EmailAccount.objects.get(email=account_in.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})
    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(email=account_in.email, password=account_in.password1,
                                                first_name=account_in.first_name, last_name=account_in.last_name,
                                                phone_number=account_in.phone_number)

        if user:
            token = create_token(user.id)
            return response(HTTPStatus.OK, {
                'profile': user,
                'token': token
            })
        else:
            return response(HTTPStatus.INTERNAL_SERVER_ERROR, {'message': 'An error occurred, please try again.'})


@account_controller.post('signin', response={
    200: AccountSignUpSchema,
    404: MessageOut,
})
def signin(request, signin_in: LoginSchema):
    user = authenticate(email=signin_in.email, password=signin_in.password)
    if user is not None:
        return response(HTTPStatus.OK, {
            'profile': user,
            'token': create_token(user)
        })

    return 404, MessageOut(message='User not found')



