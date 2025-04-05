import logging
from typing import Callable
from django.http import HttpRequest, HttpResponse


class RequestLoggerMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request: HttpRequest):
        # Only process if its an API request
        if request.path.startswith("/api/"):
            client_ip = self.get_client_ip(request)

            device = request.META.get("HTTP_USER_AGENT", "")

            path = request.path

            log_extra = {}
            if client_ip:
                log_extra["ip"] = client_ip
            if device:
                log_extra["device"] = device
            if path:
                log_extra["path"] = path

            # Log the request with the dynamically built extra fields
            self.logger.info("Request received", extra=log_extra)

        # Process the response
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request headers or fallback to request.META"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
