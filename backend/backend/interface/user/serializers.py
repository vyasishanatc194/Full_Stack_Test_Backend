import logging
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers

from backend.application.user.services import UserAppServices

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


user_app_services = UserAppServices()


class UserSignupSerializer(serializers.Serializer):
    """
    Serializer class for user Signup.
    """
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_email(self, value):
        """
        Checks if email is valid or not
        """
        value = value.lower()
        regex = settings.EMAIL_REGEX
        if not (re.match(regex, value)):
            raise ValidationError("Email not matching with given criteria.")
        return value


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class for User login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_email(self, value):
        """
        Checks if email is exists or not
        """
        user = user_app_services.get_user_by_email(email=value)
        if user:
            return user.email
        else:
            return None
