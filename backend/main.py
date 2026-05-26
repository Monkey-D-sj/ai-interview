from fastapi import FastAPI

from backend.core import logger
from backend.modules.upload import upload_router

app = FastAPI()
app.include_router(upload_router)

logger.info("Application started")
