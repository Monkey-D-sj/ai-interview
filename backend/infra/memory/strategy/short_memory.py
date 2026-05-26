from dataclasses import asdict

from backend.infra.db import CacheDB
from backend.infra.memory.strategy.base import MemoryRecord


class ShortMemoryStrategy:
	"""
	Short Memory Strategy
	"""
	def __init__(self, cache_db: CacheDB, ttl: int = 60 * 60, max_records: int = 10):
		self.cache_db = cache_db
		self.ttl = ttl
		self.max_records = max_records

	def add_memory(self, memory: MemoryRecord):
		"""
		Add memory to short memory
		"""
		total_memory = self.cache_db.get(memory.session_id) or []
		total_memory.append(asdict(memory))
		if len(total_memory) > self.max_records:
			total_memory = total_memory[-self.max_records:]
		self.cache_db.insert(memory.session_id, total_memory, ttl=self.ttl)

	def get_memory(self, session_id: str) -> list[MemoryRecord]:
		"""
		Get short memory for a session
		"""
		raw = self.cache_db.get(session_id) or []
		return [MemoryRecord(**item) for item in raw]
