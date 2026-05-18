from infra import Chroma, InMemory
from infra.embedding import embedding_func
from infra.memory.strategy.base import MemoryRecord
from infra.memory.strategy.long_memory import LongMemoryStrategy
from infra.memory.strategy.short_memory import ShortMemoryStrategy


class MemoryManager:
	"""
	Memory Manager
	"""
	def __init__(
		self,
		short_memory: ShortMemoryStrategy,
		long_memory: LongMemoryStrategy,
	):
		self.short_memory = short_memory
		self.long_memory = long_memory
		
	def add_memory(self, memory: MemoryRecord):
		self.short_memory.add_memory(memory)
		if memory.importance > 0.5:
			self.long_memory.add_memory(memory)
		
	def get_memory(self, session_id: str) -> list[MemoryRecord]:
		return self.short_memory.get_memory(session_id)
	
	def query_memory(self, query_text: str) -> list[MemoryRecord]:
		return self.long_memory.query_memory(query_text)
		

def create_memory_manager() -> MemoryManager:
	cache_db = InMemory()
	short_memory = ShortMemoryStrategy(cache_db)
	
	vector_db = Chroma()
	long_memory = LongMemoryStrategy(vector_db, collection_name="long_memory", embedding_func=embedding_func)
	
	return MemoryManager(short_memory, long_memory)
