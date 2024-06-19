import inspect
from typing import Union

from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    """This class will create custom response."""

    def __init__(self):
        self.caller_function = inspect.stack()[1].function

    def struct_response(
        self, data: dict, success: bool, message: str, errors=None
    ) -> dict:
        response = dict(success=success, message=message,
                        data=data)
        if errors:
            response.pop("data")
            response["errors"] = errors
        return response

    def listing_struct_response(
        self, data: dict, success: bool, message: str, count: int, errors=None
    ) -> dict:
        response = dict(success=success, message=message,
                        count=count, data=data)
        if errors:
            response.pop("data")
            response["errors"] = errors
        return response

    def success(self, data: dict = {}, message: str = None) -> dict:
        """This method will create custom response for success event with response status 200."""
        success_message = message if message else self.success_message()
        response_data = self.struct_response(
            data=data, success=True, message=success_message
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def fail(self, status, errors: dict, message: Union[str, dict]) -> dict:
        """This method will create custom response for failure event with custom response status."""
        error_message = (
            message[next(iter(message))][0] if isinstance(
                message, dict) else message
        )
        response_data = self.struct_response(
            data={}, success=False, message=error_message, errors=errors
        )
        return Response(response_data, status=status)

    def serializer_invalid(self, status, errors: Union[str, dict], message: str) -> dict:
        """
        This method will create custom response for serializer failure event with custom response status.
        This function takes status,errors,message as input and returns Response.
        """
        final_message = (
            message[next(iter(message))][0] if isinstance(
                message, dict) else message
        )
        error_message = (
            errors[next(iter(errors))][0] if isinstance(
                errors, dict) else errors
        )
        response_data = self.struct_response(
            data={}, success=False, message=final_message, errors="Error While Operation." + " " + error_message
        )
        return Response(response_data, status=status)

    def listing(self, data: dict = {}, message: str = None) -> dict:
        """This method will create custom response for success event with response status 200."""
        success_message = message if message else self.success_message()
        response_data = self.listing_struct_response(
            data=data, success=True, message=success_message, count=len(data)
        )
        return Response(response_data, status=status.HTTP_200_OK)
