import logging
from typing import Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.services.rate_limiter import get_rate_limiter

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ("/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)

        limiter = get_rate_limiter()
        key = limiter.get_key(request)
        allowed, info = limiter.check(key)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too many requests",
                    "detail": info,
                },
                headers={"Retry-After": str(info.get("retry_after_seconds", 5))},
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), interest-cohort=()"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self' ws://localhost:* wss://localhost:* http://localhost:*;"
        )

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    MAX_BODY_SIZE = 10 * 1024 * 1024

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_BODY_SIZE:
            return JSONResponse(
                status_code=413,
                content={"error": "Request body too large", "max_bytes": self.MAX_BODY_SIZE},
            )

        if request.url.path.startswith("/api"):
            content_type = request.headers.get("content-type", "")
            if request.method in ("POST", "PUT", "PATCH"):
                if content_type and "application/json" not in content_type and "multipart/form-data" not in content_type:
                    return JSONResponse(
                        status_code=415,
                        content={"error": "Unsupported Media Type. Use application/json"},
                    )

        return await call_next(request)
