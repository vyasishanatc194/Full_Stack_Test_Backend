from typing import Type

from django.db.models.manager import BaseManager

from .models import User, UserFactory


class UserServices:
    @staticmethod
    def get_user_factory() -> Type[UserFactory]:
        """
        This Method will return UserFactory.
        """
        return UserFactory

    @staticmethod
    def get_user_repo() -> BaseManager[User]:
        """
        This method will return database manager for the User model.
        """
        return User.objects
