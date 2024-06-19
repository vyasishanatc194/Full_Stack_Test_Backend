import logging
from typing import Union

from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken

from backend.domain.user.models import User
from backend.domain.user.services import UserServices
from utils.django.exceptions import InvalidUserException, UserException

logger = logging.getLogger("django")


class UserAppServices:
    def __init__(self):
        self.user_services = UserServices()

    def get_user_by_id(self, id: str) -> Union[User, None]:
        """
        This method will return User object if obtained by ID else return None.
        """
        try:
            return self.user_services.get_user_repo().get(id=id)
        except User.DoesNotExist as e:
            logger.error("Error while Getting User by Id: %s", e)
            return None

    def get_user_by_email(self, email: str) -> Union[User, None]:
        """
        This method will return User object obtained by Email.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist as e:
            logger.error("Error while Getting User by Email: %s", e)
            return None

    def get_list_of_users(self) -> QuerySet[User]:
        """
        This Method will give list of all Users.
        """
        return self.user_services.get_user_repo().all()

    def get_user_token(self, user: User) -> dict:
        """
        This Method will return dictionary of user with access Token and Refresh Token.
        """
        try:
            token = RefreshToken.for_user(user)
            data = dict(
                id=user.id,
                email=user.email,
                full_name=user.first_name + " " + user.last_name,
                created_at=user.created_at,
                modified_at=user.modified_at,
                access=str(token.access_token),
                refresh=str(token)
            )
            logger.info(msg="Token Generated")
            return data
        except Exception as tokenError:
            logger.error("Invalid Input %s", tokenError.args[0])
            raise InvalidUserException("Invalid Credentials", str(tokenError))

    def create_user_from_dict(self, data: dict,) -> dict:
        """This method will create user from dict."""
        email = data.get("email", None)
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        password = data.get("password", None)
        user_factory_method = self.user_services.get_user_factory()
        if len(self.user_services.get_user_repo().filter(
                email=email)) > 0:
            raise UserException("Email already exists", "")
        user = user_factory_method.build_entity_with_id(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)
        )
        user.save()
        logger.info("User Created Successfully with Name: %s", user.first_name)
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "full_name": user.first_name + " " + user.last_name
        }
