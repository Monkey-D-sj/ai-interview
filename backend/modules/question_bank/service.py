from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from backend.core import logger
from backend.infra.db.object_storage import ObjectStorage


class QuestionBankService:
    def __init__(self, obs: ObjectStorage):
        self.bucket = "uploads"
        self.obs = obs
    
    def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        content_type: str | None = None,
    ) -> str:
        data = file.read()
        size = len(data)
        logger.info("Uploading {} ({}) to bucket {}", filename, _fmt_size(size), self.bucket)
        
        if not self.obs.bucket_exists(self.bucket):
            self.obs.make_bucket(self.bucket)
            logger.info("Created bucket {}", self.bucket)
        
        ct = content_type or _guess_content_type(filename)
        self.obs.put(self.bucket, filename, BytesIO(data), size, content_type=ct)
        
        url = f"{self.bucket}/{filename}"
        logger.info("Upload complete: {}", url)
        return url
    
    def create_bank(
        self,
        files: list[str]
    ) -> str:
        logger.info("开始创建题库")
        for file in files:
            current_file = self.obs.get(self.bucket, file)
        
        return "创建成功"


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
