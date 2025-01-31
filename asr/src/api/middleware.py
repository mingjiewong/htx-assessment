import uuid
import logging

from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

class UUIDMiddleware(BaseHTTPMiddleware):
    """Middleware to generate and attach a unique UUID to each request.
    
    The UUID is used to trace the request through the entire processing lifecycle.
    It is to be added to the request state and included in the response headers.
    """
    async def dispatch(
            self, 
            request: Request, 
            call_next: Callable[[Request], Response]
        ) -> Response:
        """Process the incoming request, generate a UUID, and attach it to the request state and response headers.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or request handler.

        Returns:
            Response: The HTTP response with the UUID included in the headers.        
        """
        # Generate a unique UUID for the request
        request_id = str(uuid.uuid4())
        
        # Attach the UUID to the request state for later access
        request.state.request_id = request_id
        logger.debug(f"Generated request ID {request_id} for incoming request.")
        
        # Process the request and get the response
        response = await call_next(request)
        
        # Add the UUID to the response headers
        response.headers["X-Request-ID"] = request_id
        logger.debug(f"Added X-Request-ID {request_id} to response headers.")
        
        return response