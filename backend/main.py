from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core import logger
from backend.core.setting import settings
from backend.modules.question_bank import bank_router

from backend.core.db import minio_client



@asynccontextmanager
async def lifespan(app: FastAPI):
	
	logger.info("minio 开始连接")
	minio_client.connect(
		endpoint=settings.MINIO_URL,
		access_key=settings.MINIO_ADMIN,
		secret_key=settings.MINIO_PASSWORD
	)
	logger.info("minio 连接成功")

app = FastAPI(lifespan=lifespan)
app.include_router(bank_router)

logger.info("Application started")
