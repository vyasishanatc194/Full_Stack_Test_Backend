import logging
from typing import Any

from rest_framework import status

from utils.errors.custom_response import CustomResponse

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


class AuthMiddleWare:
    """
    This class will only return response if user is authenticated otherwise raises error.
    """

    def __init__(self, get_response, pk=None) -> None:
        self.get_response = get_response

    def __call__(self, request, pk=None) -> Any:
        if not request.user.is_authenticated:
            logger.error("Authentication not provided.")
            return CustomResponse().fail(
                errors={"error": "Authentication Failed."},
                message="Authentication Failed. Please login",
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not (request.user.is_superuser or request.user.is_staff):
            response = (
                self.get_response(
                    request, pk) if pk else self.get_response(request)
            )
            return response
        else:
            logger.error("You don't have access to the page.")
            return CustomResponse().fail(
                errors={"error": "Authentication Failed."},
                message="Access denied.",
                status=status.HTTP_403_FORBIDDEN
            )
