"""
Custom middleware for logging requests and handling exceptions in tasks_module
"""

import logging
import traceback
from django.http import HttpResponse, HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.wsgi import WSGIRequest 

logger = logging.getLogger('gunicorn.error')

class TasksMiddleware(MiddlewareMixin):
    """
    Middleware to log requests and responses, and handle exceptions in tasks_module
    """

    def process_exception(self, request: HttpRequest, exception: Exception):
        """
        Override defult behavior to log exceptions
        """

        logger.error(f"Unknown error: {''.join(traceback.format_exception(exception))}")
        return HttpResponse(status=500)

    def process_response(self, request: HttpRequest, response: HttpResponse):
        """
        Override default behavior to log requests and responses
        """

        logger.info(f"{request.method} {request.get_full_path()} {response.status_code}")
        return response
