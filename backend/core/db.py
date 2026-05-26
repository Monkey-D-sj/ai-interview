from backend.infra import Minio

minio_client = Minio()

def get_minio():
	return minio_client