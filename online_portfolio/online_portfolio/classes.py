from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout

from storages.backends.s3boto3 import S3Boto3Storage
from http import HTTPStatus


class MediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class ErrorHandlingMiddleware:
    """
    The purpose of this middleware is to handle unexpected errors in the requests and
    provide a user friendly error response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        if settings.DEBUG:
            return None

        # TODO add logging here
        print(exception)

        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            return JsonResponse(
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                reason="Something Went Wrong!!",
            )

        # handling other (synchronous) requests
        messages.error(request, "Something Went Wrong!!")
        logout(request)
        return redirect("accounts:login")
