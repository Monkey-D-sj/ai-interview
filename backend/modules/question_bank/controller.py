from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse

from backend.common import success
from backend.core import logger
from backend.core.db import get_minio
from backend.infra.db.minio import Minio
from backend.modules.question_bank.service import QuestionBankService

bank_router = APIRouter(prefix="/question_bank", tags=["upload"])


@bank_router.post("/file")
async def upload(
    file: UploadFile,
    minio: Minio = Depends(get_minio)
) -> JSONResponse:
    service = QuestionBankService(minio=minio)
    url = service.upload_file(file.file, file.filename or "unknown", bucket="rag", content_type=file.content_type)
    return success({"url": url, "filename": file.filename})


@bank_router.post("/create")
async def create(
    files: list[str],
    minio: Minio = Depends(get_minio)
) -> JSONResponse:
    service = QuestionBankService(minio=minio)
    return success("新建成功")
