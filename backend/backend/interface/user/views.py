import logging
import os
import sys

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import transaction
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.application.user.services import UserAppServices
from backend.domain.user.services import UserServices
from backend.interface.user import open_api
from utils.django.exceptions import UserException
from utils.errors.custom_response import CustomResponse

from .serializers import UserLoginSerializer, UserSignupSerializer

# Logger setup
logger = logging.getLogger("django")


@extend_schema_view(
    signup=open_api.user_sign_up_extension,
    login=open_api.user_login_extension,
)
class UserViewSet(viewsets.ViewSet):
    """
    This ViewSet consist of User's Action.
    """
    authentication_class = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "signup":
            return UserSignupSerializer
        if self.action == "login":
            return UserLoginSerializer

    user_services = UserServices()

    @action(detail=False, methods=['POST'], name="signup")
    def signup(self, request) -> Response:
        """
        User signup method.
        """
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                with transaction.atomic():
                    user_data = UserAppServices().create_user_from_dict(
                        data=serializer_obj.validated_data)
                    return CustomResponse().success(
                        data=user_data,
                        message=f"User {user_data['full_name']} has been saved."
                    )
            except UserException as se:
                return CustomResponse().fail(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=f"Error Occurred while Signup. {se.args[0]}",
                    message=f"Unable to add user. {se.args[0]}."
                )
        return CustomResponse().serializer_invalid(
            status=status.HTTP_400_BAD_REQUEST,
            errors=(serializer_obj.errors),
            message="Unable to add user. Please contact administrator.",
        )

    @action(detail=False, methods=['POST'], name='login')
    def login(self, request) -> Response:
        """
        User Login Method
        """
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            email = serializer_obj.validated_data.get("email", None)
            password = serializer_obj.validated_data.get("password", None)
            try:
                with transaction.atomic():
                    user = authenticate(
                        email=email, password=password)
                    update_last_login(None, user)
                    response_data = UserAppServices().get_user_token(user=user)
                    message = "You have logged in successfully"
                    logger.info("Login SuccessFully")
                    return CustomResponse().success(data=response_data, message=message)
            except UserException as le:
                exc_type, exe_tb = sys.exc_info()
                email = os.path.split(exe_tb.tb_frame.f_code.co_filename)[1]
                logger.error(exc_type, email, exe_tb.tb_lineno, str(le))
                message = "Email or Password is invalid."
                return CustomResponse().fail(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=le.error_data(),
                    message=message,
                )
            except Exception as e:
                logger.error("Error While Login")
                return CustomResponse().fail(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=f"An error occurred while Log-in. {e.args[0]}",
                    message="Incorrect Email or Password."
                )
        logger.error("Error in Serializer data")
        return CustomResponse().serializer_invalid(
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer_obj.errors,
            message="Unable to login. Please contact administrator."
        )
