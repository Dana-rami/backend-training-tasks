import logging
import re
import time
import uuid

logger = logging.getLogger('requests')

# A request ID sent by a client is only trusted if it looks like a normal ID.
# This stops weird values (very long text, new lines) from ending up in the logs.
VALID_REQUEST_ID = re.compile(r'^[A-Za-z0-9._-]{1,64}$')


class RequestIDMiddleware:
    """
    Gives every request a unique ID.

    - Uses the X-Request-ID header if the client sent a valid one, else makes a new UUID.
    - Stores it on request.request_id so views and other middleware can use it.
    - Adds it to the response as the X-Request-ID header.
    """

    def __init__(self, get_response):
        # Runs once, when the server starts. get_response is the next layer in the chain.
        self.get_response = get_response

    def __call__(self, request):
        # Runs on every request, on the way IN (before the view).
        request_id = request.headers.get('X-Request-ID', '')
        if not VALID_REQUEST_ID.match(request_id):
            request_id = uuid.uuid4().hex
        request.request_id = request_id

        response = self.get_response(request)

        # Runs on the way OUT (after the view).
        response['X-Request-ID'] = request_id
        return response


class RequestLoggingMiddleware:
    """
    Logs one line for each request: request ID, method, path, status code and time.

    It must come after RequestIDMiddleware in MIDDLEWARE, because it reads
    request.request_id. Order matters: the request goes down the list, and the
    response comes back up in reverse order.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000
        logger.info(
            '[%s] %s %s -> %s (%.1f ms)',
            getattr(request, 'request_id', '-'),
            request.method,
            request.get_full_path(),
            response.status_code,
            duration_ms,
        )
        return response
