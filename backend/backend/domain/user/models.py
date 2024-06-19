import uuid
from dataclasses import dataclass

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from utils.django.custom_models import ActivityTracking


@dataclass(frozen=True)
class UserID:
    """
    This will create UUID that will pass in UserFactory Method

    """
    value: uuid.UUID


class UserManagerAutoID(BaseUserManager):
    """
    A User Manager that sets the uuid on a model when calling the create_superuser function.
    """

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """
        This method will create user with username validation when calls CreateSuperuser command.
        """
        if not email:
            raise ValueError("Enter an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        """
        This method will call create user and creates superuser with is_superuser flag True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(first_name, last_name, email, password, **extra_fields)


# ---------
# UserModel
# ---------


class User(AbstractBaseUser, ActivityTracking, PermissionsMixin):
    """
    User class Defined with Roles and Module and email as username.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.CharField(
        max_length=30, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManagerAutoID()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self):
        return str(self.first_name + self.last_name)


class UserFactory:
    """This Class is used for building instance of User by their methods."""

    @staticmethod
    def build_entity(
        id: UserID,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> User:
        return User(
            id=id.value,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

    @classmethod
    def build_entity_with_id(
        cls,
        email: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> User:
        entity_id = UserID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
