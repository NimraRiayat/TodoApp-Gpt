# middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class HostCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Add allowed hosts, including the Cloudflared URL
        allowed_hosts = {"localhost:8001", "127.0.0.1:8001", "patients-thompson-father-ford.trycloudflare.com"}
        
        # Get the host from the request headers
        host = request.headers.get("host")
        
        # Check if the host is in the allowed list
        if host not in allowed_hosts:
            # Return 403 if the host is not allowed
            return JSONResponse({"detail": "Host not allowed"}, status_code=403)
        
        # Proceed with the request if the host is valid
        response = await call_next(request)
        return response
