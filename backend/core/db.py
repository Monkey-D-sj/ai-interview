from backend.infra import Minio

obs_client = Minio()

def get_obs():
	return obs_client