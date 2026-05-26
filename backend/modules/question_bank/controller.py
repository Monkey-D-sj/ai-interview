from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse

from backend.common import success
from backend.core.db import get_obs
from backend.infra.db.minio import ObjectStorage
from backend.modules.question_bank.service import QuestionBankService

bank_router = APIRouter(prefix="/question_bank", tags=["upload"])


@bank_router.post("/file")
async def upload(
    file: UploadFile,
    obs: ObjectStorage = Depends(get_obs)
) -> JSONResponse:
    service = QuestionBankService(obs=obs)
    url = service.upload_file(file.file, file.filename or "unknown", bucket="rag", content_type=file.content_type)
    return success({"url": url, "filename": file.filename})


@bank_router.post("/create")
async def create(
    files: list[str],
    obs: ObjectStorage = Depends(get_obs)
) -> JSONResponse:
    service = QuestionBankService(obs=obs)
    service.create_bank(files=files)
    return success("新建成功")
