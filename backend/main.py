from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core import logger
from backend.core.setting import settings
from backend.modules.question_bank import bank_router

from backend.core.db import obs_client



@asynccontextmanager
async def lifespan(app: FastAPI):
	
	logger.info("对象存储 开始连接")
	obs_client.connect(
		endpoint=settings.MINIO_URL,
		access_key=settings.MINIO_ADMIN,
		secret_key=settings.MINIO_PASSWORD
	)
	logger.info("对象存储 连接成功")

app = FastAPI(lifespan=lifespan)
app.include_router(bank_router)

logger.info("Application started")
