from starlette.requests import Request
from starlette.responses import Response
async def log_middleware(request: Request, call_next):
    print(f"➡️  Request: {request.method} {request.url}")
    response: Response = await call_next(request)
    print(f"⬅️  Response status: {response.status_code}")
    return response
