import time
from abc import ABC, abstractmethod
from typing import Any


class CacheDB(ABC):
	"""
	In-Memory Cache Database
	"""
	@abstractmethod
	def connect(self): ...

	@abstractmethod
	def insert(self, key: str, value: Any, ttl: int | None = None): ...

	@abstractmethod
	def get(self, key: str): ...

	@abstractmethod
	def delete(self, key: str): ...

	@abstractmethod
	def close(self): ...


class InMemory(CacheDB):
	def __init__(self):
		self._store: dict[str, tuple[Any, float | None]] = {}
		self.connect()

	def connect(self):
		pass

	def insert(self, key: str, value: Any, ttl: int | None = None):
		expire_at = time.time() + ttl if ttl is not None else None
		self._store[key] = (value, expire_at)

	def get(self, key: str) -> Any | None:
		entry = self._store.get(key)
		if entry is None:
			return None
		value, expire_at = entry
		if expire_at is not None and time.time() > expire_at:
			del self._store[key]
			return None
		return value

	def delete(self, key: str):
		self._store.pop(key, None)

	def close(self):
		self._store.clear()
