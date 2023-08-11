from typing import List

from ninja.router import Router

from django.contrib.auth import login
from django.contrib.auth.models import User

from shortener.schemas import Users as U, TelegramUpdateSchema, Message, UserRegisterBody
from shortener.models import Users
from shortener.urls.decorators import admin_only

user = Router()


@user.get("", response=List[U])
@admin_only
def get_user(request):
    a = Users.objects.all()
    return list(a)


@user.post("", response={201: None})
def update_telegram_username(request, body: TelegramUpdateSchema):
    user = Users.objects.filter(user_id=request.users_id)

    if not user.exists():
        return 404, {"msg": "No user found"}

    user.update(telegram_username=body.username)
    return 201, None


@user.post("register", response={201: None, 409: Message})
def user_register(request, body: UserRegisterBody):
    email_check = User.objects.filter(email=body.email)

    if email_check.exists():
        return 409, {"msg": "이미 사용 중인 이메일 입니다."}

    user = body.register()
    login(request, user)

    return 201, None
