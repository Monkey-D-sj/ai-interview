from __future__ import annotations

from fastapi import APIRouter, UploadFile

from backend.common import success
from backend.core import logger
from backend.modules.upload.service import upload_file

upload_router = APIRouter(prefix="/upload", tags=["upload"])


@upload_router.post("/file")
async def upload(file: UploadFile):
    logger.info("Received file: {} ({}), bucket=rag", file.filename, file.content_type)
    url = upload_file(file.file, file.filename or "unknown", bucket="rag", content_type=file.content_type)
    logger.info("File uploaded successfully: {}", url)
    return success({"url": url, "filename": file.filename})
