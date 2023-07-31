from django.contrib.auth.models import User as U

from rest_framework.permissions import OR

from ninja import Schema
from ninja.orm import create_schema

from shortener.models import Organization


OrganizationSchema = create_schema(Organization)


class Users(Schema):
    id: int
    full_name: str = None
    organization: OrganizationSchema = None


class TelegramUpdateSchema(Schema):
    username: str
