from typing import Any

from fastapi.responses import JSONResponse


def success(data: Any = None, message: str = "ok") -> JSONResponse:
    return JSONResponse(content={"code": 0, "message": message, "data": data})


def fail(message: str = "error", code: int = 1, data: Any = None) -> JSONResponse:
    return JSONResponse(content={"code": code, "message": message, "data": data}, status_code=400)
