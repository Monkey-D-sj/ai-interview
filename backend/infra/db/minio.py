from __future__ import annotations

import re
from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO


def _clean_endpoint(endpoint: str) -> str:
    return re.sub(r"^https?://", "", endpoint.rstrip("/"))


class ObjectStorage(ABC):
    @abstractmethod
    def connect(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False): ...

    @abstractmethod
    def bucket_exists(self, bucket: str) -> bool: ...

    @abstractmethod
    def make_bucket(self, bucket: str): ...

    @abstractmethod
    def put(self, bucket: str, key: str, data: BinaryIO, size: int, content_type: str = "application/octet-stream"): ...

    @abstractmethod
    def get(self, bucket: str, key: str) -> BytesIO | None: ...

    @abstractmethod
    def delete(self, bucket: str, key: str): ...

    @abstractmethod
    def list(self, bucket: str, prefix: str = "") -> list[str]: ...

    @abstractmethod
    def close(self): ...


class Minio(ObjectStorage):
    def __init__(self):
        self._client = None

    def connect(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        from minio import Minio as _Minio
        if self._client:
            return
        self._client = _Minio(_clean_endpoint(endpoint), access_key=access_key, secret_key=secret_key, secure=secure)

    def bucket_exists(self, bucket: str) -> bool:
        return self._client.bucket_exists(bucket)

    def make_bucket(self, bucket: str):
        self._client.make_bucket(bucket)

    def put(self, bucket: str, key: str, data: BinaryIO, size: int, content_type: str = "application/octet-stream"):
        self._client.put_object(bucket, key, data, size, content_type=content_type)

    def get(self, bucket: str, key: str) -> BytesIO | None:
        try:
            resp = self._client.get_object(bucket, key)
            data = resp.read()
            resp.close()
            resp.release_conn()
            return BytesIO(data)
        except Exception:
            return None

    def delete(self, bucket: str, key: str):
        self._client.remove_object(bucket, key)

    def list(self, bucket: str, prefix: str = "") -> list[str]:
        objs = self._client.list_objects(bucket, prefix=prefix, recursive=True)
        return [o.object_name for o in objs]

    def close(self):
        self._client = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
