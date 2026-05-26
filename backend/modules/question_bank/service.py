from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from backend.core import logger
from backend.infra.db.minio import Minio

class QuestionBankService:
    def __init__(self, minio: Minio):
        self.minio = minio
    
    def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        bucket: str = "uploads",
        content_type: str | None = None,
    ) -> str:
        data = file.read()
        size = len(data)
        logger.info("Uploading {} ({}) to bucket {}", filename, _fmt_size(size), bucket)
        
        if not self.minio.bucket_exists(bucket):
            self.minio.make_bucket(bucket)
            logger.info("Created bucket {}", bucket)
        
        ct = content_type or _guess_content_type(filename)
        self.minio.put(bucket, filename, BytesIO(data), size, content_type=ct)
        
        url = f"{bucket}/{filename}"
        logger.info("Upload complete: {}", url)
        return url


def _fmt_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def _guess_content_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".mp3": "audio/mpeg",
        ".mp4": "video/mp4",
        ".txt": "text/plain",
        ".json": "application/json",
        ".csv": "text/csv",
    }.get(ext, "application/octet-stream")
