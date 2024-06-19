from drf_spectacular.utils import extend_schema

from .serializers import UserLoginSerializer, UserSignupSerializer

user_tags = ['Auth_Module']

user_sign_up_extension = extend_schema(
    tags=user_tags, request=UserSignupSerializer, responses={
        200: UserSignupSerializer}
)
user_login_extension = extend_schema(
    tags=user_tags, request=UserLoginSerializer, responses={
        200: UserLoginSerializer}
)
