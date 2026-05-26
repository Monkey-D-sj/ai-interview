from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# ---- MINIO配置 ----
	MINIO_URL: str
	MINIO_ADMIN: str
	MINIO_PASSWORD: str